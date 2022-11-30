import argparse
import pathlib
import sys

from gopro_overlay import geo


def gopro_dashboard_arguments(args=None):
    parser = argparse.ArgumentParser(
        description="Overlay gadgets on to GoPro MP4",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("input", type=pathlib.Path, nargs="?", help="Input MP4 file - Optional with --use-gpx-only")
    parser.add_argument("output", type=pathlib.Path, help="Output Video File - MP4/MOV/WEBM all supported, see Profiles documentation")

    parser.add_argument("--font", help="Selects a font", default="Roboto-Medium.ttf")
    parser.add_argument("--gpx", "--fit", type=pathlib.Path, help="Use GPX/FIT file for location / alt / hr / cadence / temp ...")
    parser.add_argument("--privacy", help="Set privacy zone (lat,lon,km)")

    parser.add_argument("--generate", choices=["default", "overlay", "none"], default="default", help="Type of output to generate")
    parser.add_argument("--overlay-size",
                        help="<XxY> e.g. 1920x1080 Force size of overlay. "
                             "Use if video differs from supported bundled overlay sizes (1920x1080, 3840x2160), Required if --use-gpx-only")
    parser.add_argument("--output-size", default="1080", type=int, help="Vertical size of output movie")
    parser.add_argument("--profile", help="Use ffmpeg options profile <name> from ~/gopro-graphics/ffmpeg-profiles.json")

    only = parser.add_argument_group("GPX Only", "Creating Movies from GPX File only")

    only.add_argument("--use-gpx-only", "--use-fit-only", action="store_true", help="Use only the GPX/FIT file - no GoPro location data")
    only.add_argument("--video-time-start", choices=["file-created", "file-modified", "file-accessed"], help="Use file dates for aligning video and GPS information, only when --use-gpx-only - EXPERIMENTAL! - may be changed/removed")
    only.add_argument("--video-time-end", choices=["file-created", "file-modified", "file-accessed"], help="Use file dates for aligning video and GPS information, only when --use-gpx-only - EXPERIMENTAL! - may be changed/removed")

    maps = parser.add_argument_group("Mapping", "Display of Maps")

    maps.add_argument("--map-style", choices=geo.map_styles, default="osm", help="Style of map to render")
    maps.add_argument("--map-api-key", help="API Key for map provider, if required (default OSM doesn't need one)")

    layout = parser.add_argument_group("Layout", "Controlling layout")

    layout.add_argument("--layout", choices=["default", "speed-awareness", "xml"], default="default",
                        help="Choose graphics layout")

    layout.add_argument("--layout-xml", type=pathlib.Path, help="Use XML File for layout")

    layout.add_argument("--exclude", nargs="+", help="exclude named component (will include all others")
    layout.add_argument("--include", nargs="+", help="include named component (will exclude all others)")

    debugging = parser.add_argument_group("Debugging", "Controlling debugging outputs")

    debugging.add_argument("--show-ffmpeg", action="store_true", help="Show FFMPEG output (not usually useful)")
    debugging.add_argument("--debug-metadata", action="store_true", default=False, help="Show detailed information when parsing GoPro Metadata")
    debugging.add_argument("--profiler", action="store_true", help="Do some basic profiling of the widgets to find ones that may be slow")
    debugging.add_argument("--frames", choices=["simple", "direct", "null"], default="simple", help="HIGHLY EXPERIMENTAL: Schemes for creating and rendering image frames")

    args = parser.parse_args(args)

    def quit(reason):
        print(f"Invalid arguments: {reason}", file=sys.stderr)
        parser.print_help()
        exit(1)

    if (args.video_time_start or args.video_time_end) and not args.use_gpx_only:
        quit("--video-time-start/--video-time-end only applies when --use-gpx-only")

    if args.use_gpx_only and not args.gpx:
        quit("--gpx is required with --use-gpx-only")

    if args.use_gpx_only and not args.overlay_size:
        quit("--overlay-size is required with --use-gpx-only")

    if args.use_gpx_only and args.generate != "default":
        quit("--generate cannot be combined with --use-gpx-only")

    return args
