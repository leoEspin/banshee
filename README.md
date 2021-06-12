# Migration of Banshee's music database to Rhythmbox

(Instructions and script taken from [here](https://karl-voit.at/2020/05/08/Migration-Bashee-to-Rhythmbox/))

1. Locate Banshee's database which is usually at: ``~/.config/banshee-1/banshee.db`
2. It is crucial that you don't move or rename mp3 files after you stopped using Banshee and before you migrated to Rhythmbox. This is because the absolute file path is used to match meta-data between the two databases.
3. Start Rhythmbox.
4. Change its music library root to the mp3 library sub-hierarchy.
5. Wait until all the mp3 file were indexed and written to its XML file.
6. Quit Rhythmbox.
7. Locate Rhythmbox XML file which is located at: ``~/.local/share/rhythmbox/rhythmdb.xml`
8. Get the Python script and place it in a directory with the two music library files from above.
9. Invoke the meta-data migration with `python3 banshee2rhythmbox.py`
10. Move the modified rhythmdb.xml to `~/.local/share/rhythmbox/` and keep a backup of the previous version just to be sure.
11. Start Rhythmbox

The two notebooks are for exploring and understanding each database