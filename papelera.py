def scraper_create_matches(request):
    title = 'Crear partidos de la liga'
    leagues = League.objects.all()
    
    url = "https://www.resultados-futbol.com/"

    
    for league in leagues:
        print(league.name)
        if not Match.objects.filter(league=league):
            j = 1           
            teams = Team.objects.filter(league=league)
            soccer_days = (len(teams)*2)-2 # numero de jornadas que hay en esa liga
            while j<=soccer_days:
                url_league = '{}{}/grupo1/jornada{}'.format(url,league.slug,j)
                req = requests.get(url_league, headers = headers).text
                soup = BeautifulSoup(req, 'html.parser')
                
                etiq_table = soup.find('table', {'id': 'tabla1'})
                
                etiq_aes_jugado = etiq_table.find_all('a', {'class': 'url'})   # todas las etiquetas a de partido jugado
                etiq_aes_no_jugado = etiq_table.find_all('a', {'class': 'hour'})   # todas las etiquetas a de partido NO jugado
                
                
                td_dates = soup.find_all('td', {'class': 'fecha'})

                for td_date in td_dates:
                    date_scraped = datetime.strptime(td_date['data-date'], "%a, %d %b %Y %H:%M:%S %z")
                    date = date_scraped.strftime("%Y-%m-%d")
                    
                print('jornada {}'.format(j))
                print(len(etiq_aes_jugado))
                print(len(etiq_aes_no_jugado))
                print(len(td_dates))
                print('----------------')
                
                
                j+=1
                
                
    return render(request, 'feeder/scraper_create_matches.html', {
        'title': title,
        
    })