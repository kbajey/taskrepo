The service can be integrated with any text based chat service. 
As an example it is integrated with whats app based service, which allows home delivery orders from your local vendors. 

For eg: There is wine store whi does delivery at home and his number is added as a contact on my phone as "Othernumber". 
90% percent of store owners don't use computers for online order management, they prefer a phone. 
And with whatsapp penetration this becomes easy.
   
This is how it works:
1) Send a search message. In the attached search.jpg, i sent a message "search carls" as i'm interested to buy carlsberg beers.
So i get a response from server which is integrated with elastic search for full text search, completion suggester,
spell correction and it returns list of beers with matching as well as corrected spelling.

2) Now i order 2 650 ml and 2 500ml tin using their ids. I could use their names too, but typing long names in whatsapp will be painful,
so lesser the key strokes the better is i believe. The order details are sent back by server everytime an item is added to the cart.
It is shown in order.jpg attachment.

3) I confirm the order, which is like a checkout in the e-commerce world. I had stored my address in my earlier order. 
I can change the address by updating my address. This is shown in the deliverorder.jpg file.

The responses goes to the user, but the confirmed order data goes to a group which contains a store representative who will deliver the order.
There are lot of features like a vendor can add items, change prices, update availability, promotions etc.

I'm planning to add Natural language processing( using python nltk) to this system, that is work in progress.
