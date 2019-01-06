# Fastlookup
Google instant like autocompletion for a 200000+ words dataset using suffix tree,

## Demo
[![Preview](fastlookup.gif)](http://159.65.77.177)


# Backend
App provides an api endpoint at 
```0.0.0.0:8000/search?word=< word to match>```
It returns top 25 matching results
e.g
```0.0.0.0:8000/search?word=proc``` will return 25 results matching proc according to conditions given below

# Ranking
Words are ranked as follows

-1.Matches can occur anywhere in the string, not just at the beginning. For example, eryx
should match archaeopteryx (among others).

-2. The ranking of results should satisfy the following:
	a. We assume that the user is typing the beginning of the word. Thus, matches at the start of a word should be ranked higher. 
	   For example, for the input pract, the result practical should be ranked higher than impractical.
	b. Common words (those with a higher usage count) should rank higher than rare
		words.
	c. Short words should rank higher than long words. For example, given the input environ, the result environment should rank higher than environmentalism.

-3. As a corollary to the above, an exact match should always be ranked as the
first result.

# Warning

You can modify the MAX variable in ```fastlookup/fastlookup/backend/constants.py``` to how much of the words you want to include,
Since this program is resource heavy, if you have <4GB RAM keep it <200000, otherwise you system may hang

A computer with 8GB Ram is IDEAL for this project

# Requirement

python3.6
minimum 4GB RAM
pipenv

# Usage
```
python3.6 -m pip install pipenv
git clone https://github.com/mahto56/fastlookup.git
cd fastlookup/
pipenv install
pipenv shell
cd fastlookup
python manage.py runserver 0.0.0.0:8000
```
Goto 0.0.0.0:8000

or

Goto 0.0.0.0:8000/search?word=proc
