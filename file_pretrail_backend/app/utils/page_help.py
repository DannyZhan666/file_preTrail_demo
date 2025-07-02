def paginate(queryset, page: int, page_size: int):
    total = queryset.count()
    items = queryset.offset((page - 1) * page_size).limit(page_size).all()
    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "list": items
    }
