unlocode = "USHOU"
row_from_db = get_row(unlocode) #<- we'll get rows from mysql
timezone = get_timezone(row_from_db) #<- write this
row_from_db["timezone"] = timezone
row_from_db["current_time"] = get_iso8601(timezone) #<- write this
print(row_from_db["current_time"] ) ## 2019-02-20T10:54:26+00:00
return row_from_db


