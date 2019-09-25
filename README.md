# p1-search-engine
Demonstrate your understanding of core IR concepts along with your ability to translate IR theory into
practice. Develop and apply techniques required to handle large text collections.
## Some Guidelines for Success
This is not a trivial project that can be completed in time if you start working on it a few days before it is
due. To avoid panicking, below are some suggestions that can help:
• Meet with your team early to discuss foundational aspects: programming language and interface.
• Work on each of the SE functionalities outlined for the project in order, i.e., as we cover them in
class. For example, we have discussed (and worked on) the practical aspects of text processing,
which is why you can already start implementing and testing the corresponding functionality.
• For each SE functionality, start with a simple baseline to make sure it can be properly integrated
into your SE. Once that is working, improve the initial implementation so that responds to
requirements. For example, for query suggestions you can start by always suggesting the same
query, and then build up towards proper suggestions based on query logs, for ranking you can
simply start with binary weights (i.e., whether a query term is on a document or not) and then
build up the use of the TF-IDF weighting scheme, and for snippet generation, you can start with
resource title and then build up to proper sentence selection.
• Write your report as you go along (at least the basic ideas), otherwise there is a chance you will
forget the reasons why you made certain design decisions.
## Detailed Specifications
In groups of up to 3 students, you will combine methodologies we have discussed in class and use them
as a foundation to build your own general-purpose SE. In fulfilling each of the requirements below, you 
can use any programming language, in addition to any available libraries. You will use a number of data
sources in completing this Project. A brief description of each of these sources, as well as the URLs to
download them can be found under the heading Resources (page 3 of the project description). 
