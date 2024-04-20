#!/bin/bash
find redirects -type d -exec chmod -c 755 {} \;
find redirects -type f -exec chmod -c 644 {} \;
rsync -avzP -e 'ssh -l turulomio,devicesinlan' redirects/devicesinlan/ web.sourceforge.net:/home/groups/d/de/devicesinlan/htdocs/ --delete-after



