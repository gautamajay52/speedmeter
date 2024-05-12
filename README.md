# ⚡speedmeter [![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fgautamajay52%2Fspeedmeter&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://github.com/gautamajay52/speedmeter)

> A program to check internet speed and exhaust unlimited bandwidth

## ⚡Benefits:
`speedmeter` offers `-u` flag to exhaust unlimited bandwidth.

## ⚡Installation:

Available on [PyPI](https://pypi.org/project/speedmeter/)

```
pip install speedmeter
```

## ⚡Usage:

To test using `fast.com`

```
speedmeter 
```

To test using `fast.com` for `infinite` time.

```
speedmeter -u
```

To test using `different direct URL`.

```
speedmeter -t https://somelink.com/hosting/directfile.ext
```

Full help is available with `$ speedmeter --help`

## ⚡Flags:
-  `--unlimited, -u`       test for infinite time
-  `--test-url TEST_URL, -t TEST_URL` add different url to start testing [this url should host a direct file]
-  `--simple, -s`         Only display the result, no dynamic progress bar
-  `--version`             Display the version number and exit
-  `--count COUNT, -c COUNT` number of urls to request from fast.com [default 3, Max 5]
- `-h, --help`            show this help message and exit

## ⚡ToDos:
- [x] Use unlimited bandwidth
- [x] Use custom direct URL to test
- [ ] Multi-threaded testing
- [ ] Add more ToDos



## ⚡Credits:
* [GautamKumar(me)](https://github.com/gautamajay52) for [Something](https://github.com/gautamajay52/speedmeter)
* It is a python port of [fast-cli](https://github.com/gesquive/fast-cli) with some modification.