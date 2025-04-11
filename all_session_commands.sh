echo '[NOTE] Multi-line Python parser was explained above; not suitable for one-liner format.'
df_sorted.to_csv('/mnt/data/logins_parsed.csv', index=False)
wc -l logins_parsed.csv
cut -d',' -f1 logins_parsed.csv | tail -n +2 | sort | uniq | wc -l
cut -d',' -f2 logins_parsed.csv | tail -n +2 | sort | uniq | wc -l
cut -d',' -f3 logins_parsed.csv | tail -n +2 | sort -n | head -1 | xargs -I{} date -u -d @{}
awk -F',' '{if(NR>1){key=$1; ip[$1","$2]++; if($5=="False") fail[key]++}} END {for (k in fail) print k, fail[k], "failures"; print "---"; for (k in ip) { split(k, arr, ","); user=arr[1]; ipuniq[user]++ } for (u in ipuniq) print u, ipuniq[u], "unique_ips"}' logins_parsed.csv
awk -F',' '{if(NR>1 && $5=="False") fail[$1]++} END {for (u in fail) if (fail[u] >= 5) print u, fail[u]}' logins_parsed.csv
awk -F',' '{if(NR>1) combo[$1","$2]++} END {for (c in combo) { split(c, a, ","); user = a[1]; ipset[user]++ } for (u in ipset) if (ipset[u] > 1) print u, ipset[u]}' logins_parsed.csv
awk -F',' '{if(NR>1 && $5=="False") fail[$1]++} END {for (u in fail) print u, fail[u]}' logins_parsed.csv > fail.txt
awk -F',' '{if(NR>1) uip[$1","$2]++} END {for (k in uip) { split(k, a, ","); ip[a[1]]++ } for (u in ip) print u, ip[u]}' logins_parsed.csv > ips.txt
join fail.txt ips.txt | awk '{print $1, $2+$3, $2, $3}' | sort -k2 -nr | head
awk -F',' 'NR>1 {u=$1; ip[u","$2]; if($5=="False") fail[u]++} END {for (k in ip) split(k, a, ",") ipcount[a[1]]++ for (u in fail) print u, fail[u]+ipcount[u], fail[u], ipcount[u]}' logins_parsed.csv | sort -k2 -nr | head
