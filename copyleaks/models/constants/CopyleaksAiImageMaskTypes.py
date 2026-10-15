class CopyleaksAiImageMaskTypes:
    """Detection mask types of AI Image Detection (`mask_type`)."""
    BINARY = "binary"
    """Default. RLE mask of the regions flagged as AI-generated, in `result.starts` and `result.lengths`."""

    HEATMAP = "heatmap"
    """Like BINARY, plus `result.labels`: one confidence band (0 to 4) per RLE run, for a gradient overlay."""

    NONE = "none"
    """No mask: the response has no `result`. Synchronous detection only."""
