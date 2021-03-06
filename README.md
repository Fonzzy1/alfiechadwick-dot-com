# Fonzzy's Projects
A place that I store and share my stuff. A mix  of little ideas and evolving projects written in whatever language I'm feeling like

## Style Guide
Because of the interconecting nature of my projects, most of them are built from a series of modules which can then be called from a python run list which loosley follow the following format

```

         +--------------------------------+
         |                                |
+--------v-------+                        |
|Retrieve        +-------------+          |
+---+------------+      +------v------+   |
    |        |----------+Store        +---+
+---v--------v---+      +-------------+   |
|Manipulate      +-------------|          |
+---+------------+      +------v------+   |
    |        |----------+Store        +---+
+---v--------v---+      +-------------+   |
|Output          +-------------|          |
+----------------+      +------v------+   |
                        |Store        +---+
                        +-------------+
                        
```

These modules are placed in the modules folder in the root of the reposiory and have the folowing conventions:

#### Retrieve
Load;       From Stored Files or SQL  
Get;        From an external source   
Generate;   Create Data from scratch  

#### Manipulate
Sort;       reorder aray / Dataframe  
Calculate;  Generate new information from existing info  
reshape;    chage shape of the object 

#### Output
Send;       Send to an external source  
Draw;       Create a non text output  

#### Store
Save;       Create file to output to  
Insert;     Send to SQL with existing table  
Create;     Store in SQL as new table  
Update;     Update exiting SQL table  


