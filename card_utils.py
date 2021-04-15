def add_card(app, page_number, y):
    t = [y for x, y in app.cards[page_number]]
    max_y = max(t) if len(t) > 0 else 0
    if max_y < y:
        app.cards[page_number].append([max_y+1, y])
    app.canvas.pack_forget()
    app.put_image()
