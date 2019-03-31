# Download traffic data

<codeblock>
from traffic.traffic import download_data, clean_data, create_index, calc_growth_perc

with open('../data/data.xlsx', 'wb') as output:
​    output.write(download_data())
</codeblock>

# Clean data

<codeblock>
df = clean_data()
yearly = clean_data(subset='years')
monthly = clean_data(subset='months')
</codeblock>

# Recode data

<codeblock>
# index
monthly['index_europe'] = create_index(monthly.flights_Europe)

# growth perc
monthly['p_growth_europe'] = [calc_growth_perc(monthly.flights_Europe, i) for i in range(len(monthly))]
yearly['p_growth_europe'] = [calc_growth_perc(yearly.flights_Europe, i, 1) for i in range(len(yearly))]
</codeblock>