# ndhuwebs

Tool to see who hasn't changed their password in NDHU's elearning portal.
There's some hidden utilities, but they are explained in comments in code.
Have fun.

## To install:
1. Clone this repository
  ```
  git clone https://github.com/melpeln/ndhuwebs.git
  ```
2. Create a virtual environment
  ```
  python -m venv ndhuwebs/
  ```
3. Activate the virtual environment.
5. Install a browser and it's corresponding driver (only chrome/chromedriver and firefox/geckodriver supported).
6. Install selenium using pip. Experiment with different versions according to your browser/driver.
  ```
  pip install selenium
  ```

## Tested setups
* Google Chrome 101.0.4951.41 (Official Build) (64-bit) with ChromeDriver 2.41.578700 and selenium version 3.141.0
* (Not anymore, probably broken) Mozilla Firefox for Parrot OS 91.7.0esr (64-bit) with geckodriver 0.31.0 and selenium version 4.0.0a1

## TODO
* CLI argument logic sucks.
* Support Firefox again, should probably stop using Chrome.
* Again, arguments suck. Maybe explain usage, give examples, or think of a better way to use the program.
