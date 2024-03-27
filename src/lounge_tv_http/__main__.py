import argparse

import uvicorn

import lounge_tv_http.app


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, default=8000)
    parser.add_argument('--lounge-tv-cmd',
                        default=lounge_tv_http.app._DEFAULT_COMMAND)
    parser.add_argument('--serial-device',
                        default=lounge_tv_http.app._DEFAULT_DEVICE)
    args = parser.parse_args()

    uvicorn.run(
        lounge_tv_http.app.create_app(args.lounge_tv_cmd, args.serial_device),
        host=args.host,
        port=args.port)


if __name__ == '__main__':
    main()
