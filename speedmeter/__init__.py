#!/usr/bin/env python3

import argparse
import concurrent.futures
import sys
import time

import requests

from speedmeter.api.fast_api import FastSpeedTest
from speedmeter.format.format import human_size, progress
from speedmeter.meters.bandwidth_meter import BandwidthMeter, async_copy

__version__ = "0.0.3"


def calculate_bandwidth(urls, simple, unlimited=False):
    client = requests.Session()
    count = len(urls)

    primary_bandwidth_reader = BandwidthMeter()

    if unlimited:
        simple = False

    with concurrent.futures.ThreadPoolExecutor(max_workers=count) as executor:
        futures = []
        bytes_to_read = 0

        def add_to_executor():
            bytes_to_read = 0
            for i in range(count):
                response = client.get(urls[i], stream=True)
                response.raise_for_status()
                content_length = int(response.headers.get("Content-Length", 26214400))
                bytes_to_read += content_length
                futures.append(
                    executor.submit(
                        async_copy,
                        i,
                        primary_bandwidth_reader,
                        response.raw,
                    )
                )
            return bytes_to_read

        bytes_to_read += add_to_executor()

        if unlimited:
            progress.console.print(
                f"[bold red]\nInfiniteTesting:[/bold red] {unlimited}\n"
            )
        progress.start()
        try:
            old_bytes = 0
            task = progress.add_task(
                "[cyan]DownloadSpeed:", total=bytes_to_read, visible=not simple
            )
            while True:
                current_bytes = primary_bandwidth_reader.bytes_read
                progress.update(
                    task,
                    advance=current_bytes - old_bytes,
                    total=bytes_to_read,
                    visible=not simple,
                )
                old_bytes = current_bytes
                if primary_bandwidth_reader.bytes_read >= bytes_to_read:
                    if not unlimited:
                        progress.stop()
                        break
                    bytes_to_read += add_to_executor()

                time.sleep(0.1)
        except KeyboardInterrupt:
            progress.stop()
            mess = (
                "\n[green]Stopped Infinite Testing."
                if unlimited
                else "\n[green]Speedtest Interrupted."
            )
            progress.console.print(mess)
            primary_bandwidth_reader.cancelled = True
            executor.shutdown(wait=True, cancel_futures=True)

        for future in concurrent.futures.as_completed(futures):
            results = future.result()
            if results["err"] is not None:
                progress.console.print(results["err"])

        if not simple:
            progress.console.print(
                f"\n[bold magenta]Got Speed: [green]{human_size(primary_bandwidth_reader.bandwidth())}/s [bold magenta]After [green]{primary_bandwidth_reader.duration():.1f} seconds"
            )
        else:
            progress.console.print(
                f"\n[bold magenta]Got Speed: [green]{human_size(primary_bandwidth_reader.bandwidth())}/s"
            )


def main():
    parser = argparse.ArgumentParser(
        description="Estimates your current internet download speed"
    )

    parser.add_argument(
        "--simple",
        "-s",
        action="store_true",
        help="Only display the result, no dynamic progress bar",
    )
    parser.add_argument(
        "--unlimited",
        "-u",
        action="store_true",
        help="test for infinite time",
    )
    parser.add_argument(
        "--version", action="store_true", help="Display the version number and exit"
    )
    parser.add_argument(
        "--count",
        "-c",
        dest="count",
        help="number of urls to request from fast.com [default 3, Max 5]",
    )
    parser.add_argument(
        "--test-url",
        "-t",
        dest="test_url",
        action="append",
        help="add different url to start testing [this url should host a direct file]",
        default=[],
    )
    args = parser.parse_args()

    if args.version:
        progress.console.print(f"fast-cli [bold blue]v{__version__}")
        sys.exit(0)

    count = 3
    if args.count and int(args.count) < 5:
        count = int(args.count)

    if not args.test_url:
        urls, client = FastSpeedTest().get_dl_urls(count)
        location = client["location"]
        your_info = f"""
[bold magenta]Your IP: [bold green]{client['ip']}
[bold magenta]Your Location:
    [bold magenta]City: [bold green]{location['city']}
    [bold magenta]Country: [bold green]{location['country']}
"""
        progress.console.print(your_info)
    else:
        urls = args.test_url

    if not urls:
        progress.console.print("Not able to get test URL from fast.com, Use -t flag to provide your own test URL")
        sys.exit(0)

    try:
        calculate_bandwidth(urls, args.simple, args.unlimited)
    except Exception as e:
        progress.console.print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
