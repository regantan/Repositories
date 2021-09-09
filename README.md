# ratemyuni
#### Video Demo:  <URL HERE>
#### Description:
ratemyuni is a website that takes in reviews from real students about their universities for my country in Malaysia. One of the hardest decisions I had to made was deciding which 
univeristy to attend after my A-level Exams thus I search everywhere on the internet to find reviews of universities but was either disappointed by only the 2 reviews displayed or 
couldn't find any information at all. In the end I had to ask my local subreddit for their opinions on the university they attended, therefore, I'd liked to make a web app to take in 
anonymous reviews from students to allow a platform for young teenagers just like me to see which university best aligned with their needs and expectations.

This web application is in many ways similar to a known website called ratemyprofessors.com and indeed its where my inspiration came from as that website provided a much needed
solution for students in America and this was my solution for students in my home country, Malaysia.

First, I started with the implimentation of a login and register route for students to save their preferences of what universities they attended but decided to leave that out of the 
user side and instead allow staff members to log in to the webapp to look at contact forms and reports in my final web application. Next, I implemented the index route and decided to 
add an AJAX call to the server to allow user to type out a university name and receive instant results on the university available and links to their ratings page instead of a 
regular list of universities as to allow for a cleaner look to the home page.

Once users are taken to the ratings page they will be able to see the overall grade of the university from the ratings and view each rating in tables. I decided to display each
ratings in the form of tables as tables are able to display information in the most concise way while considering my skill level at the moment of programming. User will also be able 
to submit ratings on the ratings page as well as a rate link on navbar where both forms go through the same route. Beside each rating, user can also report ratings through a button
that sends user to fill in a form regarding the rating that called for the report.

Lastly, users can contribute to the universities and view all the supported universities on the universities page. Do note that reports and contribution of universities require users
to type in their email but is solely to run through and email checker API. This acts as a barrier for unwanted and trolling attitudes from users. The contact page on the footer
however will store user's email to contact back.

Staff members will be able to log in to the website and can view contact forms and reports submitted by users that had not been processed and are able to press a button named "Seen" 
to mark that the form has been processed. After logging in staff members can also register other members to the page to log in next time.
