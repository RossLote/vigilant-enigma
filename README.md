## Dependencies

Requires python 3.6

## Usage

1. Clone the repo
2. cd into the repo directory
3. `pip install -r requirements.txt`
4. `python3 manage.py test`

### Postman tests

Included in this repo is a postman file. To run the postman e2e tests first import `postman.json` into your postman installation the run the following commands:

1. `python3 manage.py loaddata products` to seed your database
2. `python3 manage.py runserver`

You can now run the postman tests.

## Design decisions

I had two main constraints when designing this.
1. Keep it simple (no complicated libraries or dependencies)
2. No GUI (I tend to get caught up in the tiny details when I do GUIs)

This led me to a basic REST API design. If I was doing this in production I would likely use `djangorestframework` to build a robust REST API. If it was for a large distributed system then I would probably build it using an event sourcing architecture.

## Notes

This is obviously missing basic security and authentication to keep it as simple as possible.