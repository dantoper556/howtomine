<h1>Вячеслав Козицкий - "HowToMine.ru"</h1>
<h3>Группа 10И4</h3>
<h3>Электронная почта: vyacheslav.kozickij@gmail.com</h3>
<h3>VK: https://vk.com/vkozickiy</h3>

<h3> [Сценарий 1: Подбор оборудования] </h3>
<ol>
  <li>Открывается страница "Подбор оборудования" </li>
  <li>Пользователь заполняет обязательное поле "Бюджет" и необязательные поля "Максимальный расход электроэнергии", "Цена электроэнергии", "Количество видеокарт"</li>
  <li>Пользователь нажимает кнопку "Подобрать"</li>
  <li>Страница выдает пользователю информацию о подобранной конфигурации - количество и модели карт, модель материнской платы, модель блоков питания и т.д. и 1 наиболее выгодную модель асика</li>
  <li>Запускается сценарий 5 для расчета доходности конфигурации </li>
  <li>Для каждого компонента пользователь получает ссылку на магазин, где его можно приобрести </li>
  <li>Пользователю показывается карта, на которой отмечен самый выгодный майнинг-отель </li>
  <li>Пользователь может экспортировать конфигурацию в pdf нажав соответствующую кнопку, тогда запускается сценарий 6 </li>
</ol>

<h3> [Сценарий 2: Расчет доходности фермы на видеокартах] </h3>
<ol>
  <li>Открывается страница "Расчет доходности фермы на видеокартах" </li>
  <li>Пользователю показывается динамическая форма ввода видеокарт </li>
  <li>По нажатию на кнопку "Добавить видеокарту" добавляется форма ввода еще 1 модели видеокарт </li>
  <li>Форма представляет из себя поле выбора модели видеокарт и количество карт этих моделей </li>
  <li>Пользователь заполняет поле "Стоимость электроэнергии" </li>
  <li>Пользователь нажимает кнопку "Рассчитать доходность" </li>
  <li>Запускается сценарий "Расчет доходности"</li>
</ol>

<h3> [Сценарий 3: Расчет доходности фермы из асиков] </h3>
<ol>
  <li>Открывается страница "Расчет фермы из асиков" </li>
  <li>Пользователю показывается динамическая форма ввода асиков </li>
  <li>По нажатию на кнопку "Добавить асик" добавляется форма ввода еще 1 модели асика </li>
  <li>Форма представляет из себя поле выбора модели асика и количество асиков этой модели </li>
  <li>Пользователь заполняет поле "Стоимость электроэнергии" </li>
  <li>Пользователь нажимает кнопку "Рассчитать доходность" </li>
  <li>Запускается сценарий "Расчет доходности"</li>
</ol>

<h3> [Сценарий 4: Расчет доходности] </h3>
<ol>
  <li>Сценарий получает конфигурацию, введенную пользователем или подобранную системой и отображает результаты расчета на той же странице </li>
  <li>Программа парсит данные о каждой карте из конфигурации </li>
  <li>Программа парсит данные о криптовалютах </li>
  <li>Для каждой монеты рассчитывается доходность майнинга этой монеты </li>
  <li>Для каждой монеты программа находит оптимальные настройки Power Limit для каждой карты и исходя из них считает расход электроэнергии конфигурации </li>
  <li>Для видеокарт: подбираются наиболее выгодные пары/тройки валют для дуал-/трипл- майнинга соответственно и рассчитывается соотношение этих валют при майнинге </li>
  <li>Считаются окупаемость конфигурации, "точки 0" на основе спарсенных цен оборудования </li>
  <li>Результаты отображаются на странице в виде таблицы </li>
</ol>

<h3> [Сценарий 5: Показ майнинг-отелей] (не будет реализован) </h3>
<ol>
  <li>Открывается страница "Показ майнинг-отелей" </li>
  <li>Пользователю показывается карта России, на которой точками отмечены координаты отелей </li>
  <li>По нажатию на каждую точку пользователя перекидывает на сайт отеля</li>
  <li>Рядом с картой находится поле ввода адреса и кнопка "Найти ближайший отель" </li>
  <li>По нажатию на эту кнопку пользователю отображается несколько ближайших отелей к заданной точке</li>
  <li>Для каждого отеля показаны стоимость размещения фермы, адрес и расстояние до введенной точки </li>
  <li>По нажатию на карточку отеля открывается сайт отеля </li>
</ol>

<h3> [Сценарий 6: Экспорт конфигурации в pdf] </h3>
<ol>
  <li>Программе, формирующей файл передается нужная конфигурация </li>
  <li>Программа заполняет в файле компоненты конфигурации и их стоимость </li>
  <li>Программа считает доходность конфигурации согласно сценарию 4 </li>
  <li>Программа прикрепляет к файлу таблицу с доходностью конфигурации на нескольких монетах </li>
  <li>Для конфигурации также будут приложены оптимальные настройки Power Limit, Core Clock Offset, Memory Clock </li>
  <li>Открывается страница скачивания pdf-файла</li>
  <li>Пользователь сохраняет файл на свое устройство</li>
</ol>

<h3> [Сценарий 7: Просмотр популярных магазинов с комплектующими] </h3>
<ol>
  <li>Открывается страница "Просмотр популярных магазинов с комплектующими" (это страница агрегатор магазинов) </li>
  <li>Страница представляет из себя список из товаров и ссылок на магазины, где эти товары можно купить </li>
  <li>Пользователь может фильтровать товары по типу, бренду, ценовому диапазону </li>
  <li>Пользрователю будет показан список магазинов где можно купить готовые конфигурации </li>
  <li>Список готовых конфигураций также можно будет фильтровать? </li>
  <li>Все товары будут представлены в виде карточек, на которых будут название товара, фото, краткое описание, цена и магазин, где выгодно купить данный товар</li>
  <li>По нажатию на карточку пользователя перебрасывает на страницу товара в указаном на карточке магазине</li>
</ol>
