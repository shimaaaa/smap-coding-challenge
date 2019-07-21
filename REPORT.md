# Report of SMAP Python Developer Challenge

## Challenge implemented

`Challenge 1 - The Full Stack Challenge`

## Technology Stacks 

- python (3.6.8)
- Django (1.11.21)
- Django REST Framework (3.9.1)
- Vue.js
- Bootstrap Vue
- vue-chartjs 
- Node.js (10.16.0)
- npm (6.9.0)
- webpack

## How To Setup Application 

- install python
- install Node.js and npm
- `pip install -r requirements.txt`
- `cd dashboard`
- `npm install`
- `python manage.py migrate`
- `python manage.py import`
- `python manage.py runserver 0.0.0.0:8000`

## Backend (Import Command) Description

### Technical Decisions 

- Unit test could be implemented easily by separating the part that reads and writes data from the business logic using the Dependency Inversion Principle.
    - Easy to create dummy classes when creating unit test by making them abstract classes.
- Use type hinting.
    - Static analytics becomes possible.
    - Specifying types in method arguments improves readability.
- Separate daily summary data is created to graph daily data.

### Problems

- On Windows WSL, I/O Error occurred at the time of data registration and registration processing failed on the way.
    - It did not occur on EC2 instance.

### Trade-Off

- Handling of duplicate data
    - For the same user, consumption data of the same datetime, bulk insert is performed as it is without checking in advance, and one consumption data is registered in case of an error. (using database unique key constraint)
    - Prioritizing the performance.
    - I think database unique key constraint must be check in before.

## Frontend Description

### Check Browsers

- Google Chrome (Latest: 75.0.3770.142)
- Firefox (Latest: 68.0.1)

### Technical Decisions

- To display graphs and pageable tables, I created a frontend view using simple Vue.js.

### Problems

- Need optimize in application bundle size with webpack.
    - Using webpack externals, I reduced bundle Javascript size.

## Other functions to be implemented

- Summary data compared to the previous year
- Daily electricity charges(Consumption × Unit price that matches the tariff category?)
