# p1-search-engine
## How to Create
The gui for this project uses tkinter, make sure the environment is set up properly for tkinter

1. Download the wikipedia 1.6 million file collection wikipedia_text_files.json from https://drive.google.com/file/d/1T_HFDEB2vGCZDyKrKNZYEKZJTnAHASgp/view?usp=sharing. 
2. Then run formatWikiFile.py to turn this into a json lines file, wikipedia_data_lines.json.
3. Then run hashIndex.py to generate the index in 8 pickle files. Move into the hashed-index directory.
4. Then run readHashedIndex.py to generate all the hashmaxTermFrequency and hashTFIDF files, 8 of each. Move into the hashed-max-term and hashed-tfidf directories.
5. In the querylogs directory run combine_clean_data.py to get one full querylog file.
6. Return to the project directory.
7. Then go one directory level up from the project and create a directory called wiki-files-separated.
8. Then navigate into this new directory and create 9 folders file1, file2,...,file9.
9. Then navigate back into your project directory and run splitUpFiles.py, this will break the wikipedia files up into individual documents, 
to allow for faster searching
10. To run the project you can either run gui.py or justins_gui.py. justins_gui.py requires > 27 GB memory, but is faster
11. when the gui is running you can enter a search term, hitting the spacebar will generate query suggestions you can select from. Hitting
enter will begin the search. Relevant, ranked results will appear along with a 2 sentence snippet.
