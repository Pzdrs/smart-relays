def get_progress_bar_color(progress_percentage):
    if progress_percentage < .5:
        return "is-primary"
    elif .5 <= progress_percentage < .75:
        return "is-warning"
    else:
        return "is-danger"
