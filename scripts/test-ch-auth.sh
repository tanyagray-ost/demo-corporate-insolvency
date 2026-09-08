export COMPANIES_HOUSE_API_KEY='3090ecdd-a578-430c-bdf3-64e15c4b8cf8'


if test -n "${COMPANIES_HOUSE_API_KEY:-}"; then
  printf 'API key is set; length: %s characters\n' \
    "$(printf %s "$COMPANIES_HOUSE_API_KEY" | wc -c | tr -d ' ')"
else
  echo 'API key is not set'
fi


curl --fail-with-body \
  --user "${COMPANIES_HOUSE_API_KEY}:" \
  "https://api.company-information.service.gov.uk/company/03782379"


curl --fail --silent --show-error \
  --user "${COMPANIES_HOUSE_API_KEY}:" \
  "https://api.company-information.service.gov.uk/company/03782379"
