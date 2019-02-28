# Time-Zone-Finder


This is a cloud function that will enable you to determine the local timezone of a given location using the UNLocode.

The UNLocode gets passed through the mySQL database and retrieves the corresponding latitude and longitude details.
Those details are then processed through the timezonefinder package that will then return the local time in iso8601 format. 
