# A clean toy

This is a toy FastApi app. Explore the Makefile goals. You need a running container service with docker CLI
and python module `aiohttp` to run the stress-test. By default `make` will build a testing container and run unit tests for everything.

## Overview of the Project

This project setup is for a FastAPI-based web application that includes unit tests, in-memory caching, and Docker integration. Below is an overview of how the various files work together to form the complete project.

## Project Structure

### Main Application Files

- main.py: FastAPI application definition and endpoints.
- user.py: Defines the User and UserService classes for user information and in-memory caching.
- cache.py: Implements an asynchronous LRU cache decorator.

### Testing and Benchmarking

- stress.py: A script to perform stress testing on the application, measuring response times and collecting statistics.

### Docker Integration

- Makefile: Provides make targets to build, run, and clean Docker images, as well as to launch stress tests.
- Dockerfile: Dockerfile to build the Docker images for the application and tests.

### Utility Scripts

- entrypoint.sh: A shell script to run unit tests and measure code coverage.

## Why clean?

```bash
───────────────────────────────────────────── 🐙 complexipy 0.3.3 ─────────────────────────────────────────────
 [00:00:00] ########################################       8/8       Done!                                                                                        Summary                                                     
     ┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓      
     ┃ Path                  ┃ File          ┃ Function                                    ┃ Complexity ┃      
     ┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩      
     │ ./app/cache.py        │ cache.py      │ async_lru_cache                             │ 0          │      
     ├───────────────────────┼───────────────┼─────────────────────────────────────────────┼────────────┤      
     │ ./app/main.py         │ main.py       │ read_root                                   │ 0          │      
     ├───────────────────────┼───────────────┼─────────────────────────────────────────────┼────────────┤      
     │ ./app/user.py         │ user.py       │ UserService::__hash__                       │ 0          │      
     ├───────────────────────┼───────────────┼─────────────────────────────────────────────┼────────────┤      
     │ ./app/user.py         │ user.py       │ UserService::__post_init__                  │ 0          │      
     ├───────────────────────┼───────────────┼─────────────────────────────────────────────┼────────────┤      
     │ ./app/user.py         │ user.py       │ UserService::hits                           │ 0          │      
     ├───────────────────────┼───────────────┼─────────────────────────────────────────────┼────────────┤      
     │ ./stress.py           │ stress.py     │ main                                        │ 0          │      
     ├───────────────────────┼───────────────┼─────────────────────────────────────────────┼────────────┤      
     │ ./tests/test_cache.py │ test_cache.py │ test_decorator_should_cache_async_func      │ 0          │      
     ├───────────────────────┼───────────────┼─────────────────────────────────────────────┼────────────┤      
     │ ./tests/test_main.py  │ test_main.py  │ test_root_read                              │ 0          │      
     ├───────────────────────┼───────────────┼─────────────────────────────────────────────┼────────────┤      
     │ ./tests/test_main.py  │ test_main.py  │ test_root_read_fail_with_bad_token          │ 0          │      
     ├───────────────────────┼───────────────┼─────────────────────────────────────────────┼────────────┤      
     │ ./tests/test_main.py  │ test_main.py  │ test_user_read_fail_with_bad_token          │ 0          │      
     ├───────────────────────┼───────────────┼─────────────────────────────────────────────┼────────────┤      
     │ ./tests/test_main.py  │ test_main.py  │ test_user_read_single                       │ 0          │      
     ├───────────────────────┼───────────────┼─────────────────────────────────────────────┼────────────┤      
     │ ./tests/test_user.py  │ test_user.py  │ test_new_user                               │ 0          │      
     ├───────────────────────┼───────────────┼─────────────────────────────────────────────┼────────────┤      
     │ ./tests/test_user.py  │ test_user.py  │ test_new_user_service                       │ 0          │      
     ├───────────────────────┼───────────────┼─────────────────────────────────────────────┼────────────┤      
     │ ./tests/test_user.py  │ test_user.py  │ test_new_user_validates_args_or_fails       │ 0          │      
     ├───────────────────────┼───────────────┼─────────────────────────────────────────────┼────────────┤      
     │ ./tests/test_user.py  │ test_user.py  │ test_new_user_with_valid_args               │ 0          │      
     ├───────────────────────┼───────────────┼─────────────────────────────────────────────┼────────────┤      
     │ ./tests/test_user.py  │ test_user.py  │ test_user_service_expected_user             │ 0          │      
     ├───────────────────────┼───────────────┼─────────────────────────────────────────────┼────────────┤      
     │ ./tests/test_user.py  │ test_user.py  │ test_user_service_initial_hit_count_is_zero │ 0          │      
     ├───────────────────────┼───────────────┼─────────────────────────────────────────────┼────────────┤      
     │ ./tests/test_user.py  │ test_user.py  │ test_user_service_raise_valuerror           │ 0          │      
     ├───────────────────────┼───────────────┼─────────────────────────────────────────────┼────────────┤      
     │ ./app/main.py         │ main.py       │ check_token                                 │ 1          │      
     ├───────────────────────┼───────────────┼─────────────────────────────────────────────┼────────────┤      
     │ ./app/main.py         │ main.py       │ read_user                                   │ 1          │      
     ├───────────────────────┼───────────────┼─────────────────────────────────────────────┼────────────┤      
     │ ./stress.py           │ stress.py     │ get                                         │ 1          │      
     ├───────────────────────┼───────────────┼─────────────────────────────────────────────┼────────────┤      
     │ ./tests/test_cache.py │ test_cache.py │ _positive                                   │ 1          │      
     ├───────────────────────┼───────────────┼─────────────────────────────────────────────┼────────────┤      
     │ ./tests/test_main.py  │ test_main.py  │ test_user_read_all                          │ 1          │      
     ├───────────────────────┼───────────────┼─────────────────────────────────────────────┼────────────┤      
     │ ./tests/test_main.py  │ test_main.py  │ test_user_read_fail_invalid_user            │ 1          │      
     ├───────────────────────┼───────────────┼─────────────────────────────────────────────┼────────────┤      
     │ ./app/user.py         │ user.py       │ UserService::user                           │ 2          │      
     ├───────────────────────┼───────────────┼─────────────────────────────────────────────┼────────────┤      
     │ ./tests/test_main.py  │ test_main.py  │ test_user_read_cache_db_replies             │ 3          │      
     └───────────────────────┴───────────────┴─────────────────────────────────────────────┴────────────┘      
🧠 Total Cognitive Complexity in .: 13
8 files analyzed in 0.0109 seconds
────────────────────────────────────────── 🎉 Analysis completed! 🎉 ──────────────────────────────────────────