CREATE TABLE lobeliacosmetics(
    "Channel Title" VARCHAR(255),
	"Channel Username" VARCHAR(255),
	ID SERIAL PRIMARY KEY,
	Message TEXT,
	Date TIMESTAMP,
	"Media Path" VARCHAR(255),
	Product_Name VARCHAR(255),
	Weight VARCHAR(50),
	Price VARCHAR(255),
	"Telegram Address" VARCHAR(255),
	Address TEXT,
	"Phone Number" VARCHAR(50),
	Open_Day_And_Time TEXT,
	"Delivery Fee" VARCHAR(50)
);