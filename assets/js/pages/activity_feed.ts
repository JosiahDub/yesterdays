/**
 * Activity Feed page JavaScript
 *
 * Handles the "Load More" infinite scroll functionality and filtering using Alpine.js.
 */
import "../../styles/pages/activity.css";

// Server page size (activity.views.ITEMS_PER_PAGE); a shorter page means the end.
const PAGE_SIZE = 20;

const ALL_TYPES = [
  "group",
  "comment",
  "milestone",
  "sitewide",
  "validation",
  "subject",
  "new_subject",
  "new_collection",
] as const;

type ActivityType = (typeof ALL_TYPES)[number];

type ActivityFilters = Record<ActivityType, boolean>;

// The server's selection when the URL has no `types` param.
const DEFAULT_TYPES: readonly ActivityType[] = [
  "group",
  "comment",
  "milestone",
  "sitewide",
  "new_subject",
  "new_collection",
];

interface FilterChangedDetail {
  types: ActivityType[];
}

interface ActivityFilter {
  filters: ActivityFilters;
  applyFilters(): void;
}

interface ActivityFeed {
  hasMore: boolean;
  loading: boolean;
  noneSelected: boolean;
  _pendingFetch: Promise<Response> | null;
  _loadingTimer: ReturnType<typeof setTimeout> | undefined;
  _isLoadingMore: boolean;
  _items(): HTMLElement;
  _moreUrl(): string;
  reloadFeed(event: CustomEvent<FilterChangedDetail>): Promise<void>;
  prefetchMore(): void;
  loadMore(): Promise<void>;
}

function fetchFeed(url: string): Promise<Response> {
  return fetch(url, {
    headers: { "X-Requested-With": "XMLHttpRequest" },
  });
}

function countItems(html: string): number {
  const doc = new DOMParser().parseFromString(html, "text/html");
  return doc.querySelectorAll(".activity-item").length;
}

/**
 * Alpine.js component for the activity type filter dropdown.
 *
 * @param initialFilters - Initial filter states from the server, keyed by type
 */
window.Alpine.data(
  "activityFilter",
  function (initialFilters?: Partial<ActivityFilters>): ActivityFilter {
    const filters = Object.fromEntries(
      ALL_TYPES.map((type) => [
        type,
        initialFilters?.[type] ?? DEFAULT_TYPES.includes(type),
      ]),
    ) as ActivityFilters;

    return {
      filters,

      applyFilters() {
        const selected = ALL_TYPES.filter((type) => this.filters[type]);

        // Update URL without reloading
        const url = new URL(window.location.href);
        url.searchParams.delete("before");

        // Omit types param only when selection matches the server default
        const isDefault =
          selected.length === DEFAULT_TYPES.length &&
          DEFAULT_TYPES.every((t) => selected.includes(t));
        if (selected.length === 0 || isDefault) {
          url.searchParams.delete("types");
        } else {
          url.searchParams.set("types", selected.join(","));
        }

        history.replaceState(null, "", url.toString());

        // Tell the feed (listening with @filter-changed.window) to reload
        window.dispatchEvent(
          new CustomEvent<FilterChangedDetail>("filter-changed", {
            detail: { types: selected },
          }),
        );
      },
    };
  },
);

/**
 * Alpine.js component for the activity feed with "Load More" functionality.
 *
 * @param initialHasMore - Whether there are more items to load
 * @param initialNoneSelected - Whether no filter types are selected
 */
window.Alpine.data(
  "activityFeed",
  function (initialHasMore: boolean, initialNoneSelected = false): ActivityFeed {
    return {
      hasMore: initialHasMore,
      loading: false, // Controls spinner visibility (debounced)
      noneSelected: initialNoneSelected,

      // Pending fetch promise from prefetch (mousedown)
      _pendingFetch: null,
      // Timer for debounced loading indicator
      _loadingTimer: undefined,
      // Flag to prevent concurrent requests (separate from loading indicator)
      _isLoadingMore: false,

      _items() {
        const items = document.getElementById("activity-feed-items");
        if (!items) throw new Error("Activity feed container not found");
        return items;
      },

      // URL of the page after the last rendered item
      _moreUrl() {
        const url = new URL(window.location.href);
        const items =
          this._items().querySelectorAll<HTMLElement>(".activity-item");
        const timestamp = items[items.length - 1]?.dataset.timestamp;
        if (timestamp) url.searchParams.set("before", timestamp);
        return url.toString();
      },

      async reloadFeed(event) {
        // A prefetch from an aborted Load More click targets the old filters
        this._pendingFetch = null;

        const types = event.detail?.types ?? [];
        this.noneSelected = types.length === 0;

        if (this.noneSelected) {
          this._items().innerHTML = "";
          this.hasMore = false;
          return;
        }

        this.loading = true;

        try {
          const url = new URL(window.location.href);
          url.searchParams.delete("before");

          const response = await fetchFeed(url.toString());
          if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
          }

          const html = await response.text();

          // Replace the feed content
          this._items().innerHTML = html;
          this.hasMore = countItems(html) >= PAGE_SIZE;
        } catch (error) {
          console.error("Error reloading activities:", error);
        } finally {
          this.loading = false;
        }
      },

      /**
       * Prefetch next page on mousedown for faster perceived loading.
       * Called via @mousedown on the Load More button.
       */
      prefetchMore() {
        if (this._isLoadingMore || !this.hasMore || this._pendingFetch) return;
        this._pendingFetch = fetchFeed(this._moreUrl());
      },

      /**
       * Load more activities via AJAX.
       * Uses prefetched response if available.
       */
      async loadMore() {
        if (this._isLoadingMore || !this.hasMore) return;
        this._isLoadingMore = true;

        // Debounce the loading indicator - only show after 200ms
        this._loadingTimer = setTimeout(() => {
          this.loading = true;
        }, 200);

        try {
          let response;
          if (this._pendingFetch) {
            // Use the prefetched request
            response = await this._pendingFetch;
            this._pendingFetch = null;
          } else {
            response = await fetchFeed(this._moreUrl());
          }

          if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
          }

          const html = await response.text();
          const count = html.trim() ? countItems(html) : 0;

          if (count > 0) {
            this._items().insertAdjacentHTML("beforeend", html);
          }
          // A short page (or an empty one) means we've reached the end
          if (count < PAGE_SIZE) {
            this.hasMore = false;
          }
        } catch (error) {
          console.error("Error loading more activities:", error);
          this._pendingFetch = null;
          // Don't set hasMore to false on error - let user retry
        } finally {
          clearTimeout(this._loadingTimer);
          this.loading = false;
          this._isLoadingMore = false;
        }
      },
    };
  },
);
