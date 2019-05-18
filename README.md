PhotoSorter is a tool to arrange mediafiles according their creation date.

sorter.py <source> <destination>

Source folder contains unordered data, let's say, that's media device like smartphone or camera.
Destination folder is a place where files should be stored according their creation date.
Following destination structure preserved:

<pre>

Destination\
  |
  +----- YYYY_MM_DD\
  |            |
  |            + --- File 1
  |            |    ...
  |            + --- File n
  +
 ...
  +----- NOT_DATED
               |
               + --- Files without metadata
     
</pre>
YYYY, MM and DD are Year Month and Day of file creation.
Creation date extracted from file's metadata, like EXIF, QuickTime timestamp of MTS subtitle stream.

Supported file formats
   <li> JPEG
   <li> MOV
   <li> MP4
   <li> AVI
   <li> MTS
   
Files with empty metadata are copied to NOT_DATED subfolder of Destionation.
