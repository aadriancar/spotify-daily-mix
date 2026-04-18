def fetch_pages(sp, api_call, *args, limit=50, **kwargs):
    """
    Fetch every item from a paginated Spotify endpoint.
    """
    page = api_call(*args, limit=limit, offset=0, **kwargs)
    items = []

    while page:
        items.extend(page.get("items", []))
        page = sp.next(page) if page.get("next") else None

    return items

def display_numbered(items, label_fn):
    for i, item in enumerate(items, 1):
        print(f"  {i:>2}. {label_fn(item)}")

def pick_indices(items, prompt="Enter numbers (comma-separated): "):
    raw = input(prompt).strip()
    if not raw:
        return []
    try:
        indices = [int(x.strip()) - 1 for x in raw.split(",")]
        return [items[i] for i in indices if 0 <= i < len(items)]
    except ValueError:
        print("    Invalid input — skipping.")
        return []
    