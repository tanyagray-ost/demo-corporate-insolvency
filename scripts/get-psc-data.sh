export COMPANIES_HOUSE_API_KEY='3090ecdd-a578-430c-bdf3-64e15c4b8cf8'

for company_number in 03782379 00077628 00594581 02684154
do
  curl  \
    --user "${COMPANIES_HOUSE_API_KEY}:" \
    "https://api.company-information.service.gov.uk/company/${company_number}/persons-with-significant-control?items_per_page=100&start_index=0" \
    --output "data/companies-house/psc/${company_number}.json"
done



