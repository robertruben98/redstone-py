# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-06-21

### Added

- Initial release.
- `RedStoneClient` — synchronous client for the RedStone oracle HTTP API.
- `AsyncRedStoneClient` — asynchronous client with the same surface.
- Methods: `get_price`, `get_latest_value`, `get_prices`, `get_historical_prices`.
- `PricePoint` pydantic v2 model and a `RedStoneError` exception hierarchy.
- `py.typed` marker for full typing support.

[Unreleased]: https://github.com/robertruben98/redstone-py/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/robertruben98/redstone-py/releases/tag/v0.1.0
