from rest_framework import renderers


class UserRenderer(renderers.JSONRenderer):
    """
    Custom renderer for JSON responses with success and error formatting.
    """

    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        # Avoid double-wrapping by checking if "success" is already present
        if isinstance(data, dict) and "success" in data:
            return super().render(data, accepted_media_type, renderer_context)

        # Check for errors in the response data
        if isinstance(data, dict) and data.get(
            "detail", None
        ):  # Handles DRF's default error key
            response = {"success": False, "errors": data}
        else:
            response = {"success": True, "data": data}

        return super().render(response, accepted_media_type, renderer_context)


class UserBrowsableAPIRenderer(renderers.BrowsableAPIRenderer):
    """
    Custom renderer for the Browsable API that uses the same global response format.
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        # Avoid double-wrapping by checking if "success" is already present
        if isinstance(data, dict) and "success" in data:
            return super().render(data, accepted_media_type, renderer_context)

        # Format the data for the browsable API
        if isinstance(data, dict) and data.get("detail", None):
            response = {"success": False, "errors": data}
        else:
            response = {"success": True, "data": data}

        return super().render(response, accepted_media_type, renderer_context)
