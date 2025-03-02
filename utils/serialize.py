

def serialize_form_data(form):
    """ Convert WTForms data to a JSON serializable format. """
    data = form.data.copy()  # Make a copy to avoid modifying the original
    for key, value in data.items():
        if isinstance(value, (set, tuple)):  # Convert sets/tuples to lists
            data[key] = list(value)
        elif hasattr(value, "isoformat"):  # Convert datetime objects
            data[key] = value.isoformat()
        elif isinstance(value, bytes):  # Convert bytes to string
            data[key] = value.decode("utf-8", errors="ignore")
        elif isinstance(value, object) and not isinstance(value, (str, int, float, dict, list, bool, type(None))):
            data[key] = str(value)  # Convert unrecognized objects to strings
    return data