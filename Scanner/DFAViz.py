from pyvis.network import Network
end_clr="#146C94"
middle_clr="#19A7CE"
strt_clr="#AFD3E2"
dead_clr="#a70000"

net=Network(directed=True)
nodes=['start','comment',
       '.','.t','.tr','.tru','.true','.true.\n.false.',
       '.f','.fa','.fal','.fals','.false',
       '\'\n\"','enteringChar','character\nvalue',
        'identifierStart','identifier','identifier2','identifier3','identifier4','identifier5','identifier6','identifier7','identifier8','identifier9','identifier10',
        'identifier12',
       '+\n-','Int\nValue',
       'Real\nValue','+.\n-.',

       'i','if',
        'im','imp','impl','impli','implic','implici','implicit',
        'in','int','inte','integ','integ','intege','integer',

         'p','pr','pro','prog','progr','progra','program',
         'pa','par','para','param','parame','paramet','paramete','parameter',
          'pri','prin','print',

        'n','no','non','none',

       'e','el','els','else',
       'en','end',

       'r','re','rea','read',
       'real',

       'c','co','com','comp','compl','comple','complex',
       'ch','cha','char','chara','charac','charact','characte','character',

       'l','lo','log','logi','logic','logica','logical',

        't','th','the','then',

       'd','do',

       'v','va','var',

       '=','==',

       '/','/=',

       '>\n<','>=\n<=',

       '*\t,\n(\t)',

       ':','::',

        'Dead\nState1','Dead\nState2','Dead\nState3','Dead\nState4','Dead\nState5','Dead\nState6','Dead\nState7','Dead\nState8','Dead\nState9','Dead\nState10',
         'Dead\nState11','Dead\nState12','Dead\nState13','Dead\nState14','Dead\nState15','Dead\nState16','Dead\nState18','Dead\nState19','Dead\nState20',
         'Dead\nState22'
          ]
colors=[strt_clr,end_clr
        ,middle_clr,middle_clr,middle_clr,middle_clr,middle_clr,end_clr
        ,middle_clr,middle_clr,middle_clr,middle_clr,middle_clr
        ,middle_clr,middle_clr,end_clr
        ,middle_clr,end_clr,end_clr,end_clr,end_clr,end_clr,end_clr,end_clr,end_clr,end_clr,end_clr,end_clr###identifiers
        ,end_clr,end_clr
        ,end_clr,middle_clr

        ,middle_clr,end_clr
        ,middle_clr,middle_clr,middle_clr,middle_clr,middle_clr,middle_clr,end_clr
        ,middle_clr,middle_clr,middle_clr,middle_clr,middle_clr,middle_clr,end_clr

        ,middle_clr,middle_clr,middle_clr,middle_clr,middle_clr,middle_clr,end_clr
        ,middle_clr,middle_clr,middle_clr,middle_clr,middle_clr,middle_clr,middle_clr,end_clr
        ,middle_clr,middle_clr,end_clr

        ,middle_clr,middle_clr,middle_clr,end_clr

        ,middle_clr,middle_clr,middle_clr,end_clr
        ,middle_clr,end_clr

        ,middle_clr,middle_clr,middle_clr,end_clr
        ,end_clr

        ,middle_clr,middle_clr,middle_clr,middle_clr,middle_clr,middle_clr,end_clr
        ,middle_clr,middle_clr,middle_clr,middle_clr,middle_clr,middle_clr,middle_clr,end_clr

        ,middle_clr, middle_clr, middle_clr, middle_clr, middle_clr, middle_clr, end_clr
        ,middle_clr, middle_clr, middle_clr, end_clr

        ,middle_clr, end_clr
        ,middle_clr, middle_clr, end_clr

        ,end_clr,end_clr
        , end_clr, end_clr

        ,end_clr, end_clr

        ,end_clr

        , middle_clr, end_clr

        ,dead_clr,dead_clr,dead_clr,dead_clr,dead_clr,dead_clr,dead_clr,dead_clr,dead_clr,dead_clr
        , dead_clr, dead_clr, dead_clr, dead_clr, dead_clr, dead_clr, dead_clr, dead_clr, dead_clr,dead_clr ,

        ]
net.add_nodes(nodes,color=colors)
net.add_edge('start','comment',label='❗')
net.add_edge('comment','comment',label='⚫')
##################################################
net.add_edge('start','.',label='.')
net.add_edge('.','.t',label='t\nT')
net.add_edge('.t','.tr',label='r\nR')
net.add_edge('.tr','.tru',label='u\nU')
net.add_edge('.tru','.true',label='e\nE')
net.add_edge('.true','.true.\n.false.',label='.')




net.add_edge('.','.f',label='f\nF')
net.add_edge('.f','.fa',label='a\nA')
net.add_edge('.fa','.fal',label='l\nL')
net.add_edge('.fal','.fals',label='s\nS')
net.add_edge('.fals','.false',label='e\nE')
net.add_edge('.false','.true.\n.false.',label='.')

net.add_edge('.','Dead\nState1',label='[^tTfF\d]')
net.add_edge('.t','Dead\nState1',label='[^rR]')
net.add_edge('.tr','Dead\nState1',label='[^uU]')
net.add_edge('.tru','Dead\nState1',label='[^eE]')
net.add_edge('.true','Dead\nState1',label='[^.]')
net.add_edge('.f','Dead\nState1',label='[^aA]')
net.add_edge('.fa','Dead\nState1',label='[^lL]')
net.add_edge('.fal','Dead\nState1',label='[^sS]')
net.add_edge('.fals','Dead\nState1',label='[^eE]')
net.add_edge('.false','Dead\nState1',label='[^.]')

net.add_edge('.true.\n.false.','Dead\nState1',label='⚫')
net.add_edge('Dead\nState1','Dead\nState1',label='⚫')
##################################################
net.add_edge('start','\'\n\"',label='\'\n\"')
net.add_edge('\'\n\"','enteringChar',label='[^\'\"]')
net.add_edge('enteringChar','enteringChar',label='[^\'\"]')
net.add_edge('enteringChar','character\nvalue',label='\'\n\"')
net.add_edge('character\nvalue','Dead\nState20',label='⚫')
net.add_edge('\'\n\"','character\nvalue',label='\'\n\"')
net.add_edge('Dead\nState20','Dead\nState20',label='⚫')
##################################################
net.add_edge('start','identifierStart',label='[abf-hjkmoqsuw-zABF-HJKMOQSUW-Z]')
net.add_edge('identifierStart','identifier',label='[\w_]')
net.add_edge('identifier','identifier',label='[\w_]')

net.add_edge('identifierStart','Dead\nState15',label='[^\w_]')
net.add_edge('identifier','Dead\nState15',label='[^\w_]')

net.add_edge('Dead\nState15','Dead\nState15',label='⚫')

#'+\n-','Int\nValue'
net.add_edge('start','Int\nValue',label='\d')
net.add_edge('start','+\n-',label='+\n-')
net.add_edge('+\n-','Int\nValue',label='\d')
net.add_edge('Int\nValue','Int\nValue',label='\d')

net.add_edge('Dead\nState2','Dead\nState2',label='⚫')
net.add_edge('Int\nValue','Dead\nState2',label='[^\d.]')
net.add_edge('+\n-','Dead\nState2',label='[^.\d]')
##################################################

#{intValPtrn.pattern}\.\d*)|([+-].\d+)
net.add_edge('.','Real\nValue',label='\d')
net.add_edge('Real\nValue','Real\nValue',label='\d')
net.add_edge('Real\nValue','Dead\nState2',label='[^\d]')

net.add_edge('+\n-','+.\n-.',label='.')
net.add_edge('+.\n-.','Real\nValue',label='\d')
net.add_edge('+.\n-.','Dead\nState2',label='[^\d]')
##################################################
#start with I
#'i\nI','iI\nfF'

net.add_edge('start','i',label='i\nI')
net.add_edge('i','if',label='f\nF')
net.add_edge('i','Dead\nState19',label='[^\d_]')
net.add_edge('if','Dead\nState19',label='[^\d_]')
net.add_edge('Dead\nState19','Dead\nState19',label='⚫')

net.add_edge('i','identifier6',label='[a-eg-lo-zA-EG-LOZ0-9_]') #not f m n
net.add_edge('if','identifier6',label='[\d_]')

net.add_edge('identifier6','identifier6',label='[\d_]')
net.add_edge('identifier6','Dead\nState19',label='[^\d_]')


net.add_edge('im','Dead\nState19',label='[^\d_]')
net.add_edge('imp','Dead\nState19',label='[^\d_]')
net.add_edge('impl','Dead\nState19',label='[^\d_]')
net.add_edge('impli','Dead\nState19',label='[^\d_]')
net.add_edge('implic','Dead\nState19',label='[^\d_]')
net.add_edge('implici','Dead\nState19',label='[^\d_]')
net.add_edge('implicit','Dead\nState19',label='[^\d_]')
net.add_edge('i','im',label='m\nM')
net.add_edge('im','imp',label='p\nP')
net.add_edge('imp','impl',label='l\nL')
net.add_edge('impl','impli',label='i\nI')
net.add_edge('impli','implic',label='c\nC')
net.add_edge('implic','implici',label='i\nI')
net.add_edge('implici','implicit',label='t\nT')

net.add_edge('im','identifier6',label='[a-oq-zA-OQ-Z0-9_]')
net.add_edge('imp','identifier6',label='[a-km-zA-KM-Z0-9_]')
net.add_edge('impl','identifier6',label='[a-hj-zA-HJ-Z0-9_]')
net.add_edge('impli','identifier6',label='[a-bd-zA-BD-Z0-9_]')
net.add_edge('implic','identifier6',label='[a-hj-zA-HJ-Z0-9_]')
net.add_edge('implici','identifier6',label='[a-su-zA-SU-Z0-9_]')
net.add_edge('implicit','identifier6',label='[\d_]')

net.add_edge('i','in',label='n\nN')
net.add_edge('in','int',label='t\nT')
net.add_edge('int','inte',label='e\nE')
net.add_edge('inte','integ',label='g\nG')
net.add_edge('integ','intege',label='e\nE')
net.add_edge('intege','integer',label='r\nR')
net.add_edge('in','identifier6',label='[a-su-zA-SU-Z0-9_]')
net.add_edge('int','identifier6',label='[a-df-zA-DF-Z0-9_]')
net.add_edge('inte','identifier6',label='[a-fh-zA-FH-Z0-9_]')
net.add_edge('integ','identifier6',label='[a-df-zA-DF-Z0-9_]')
net.add_edge('intege','identifier6',label='[a-qs-zA-QS-Z0-9_]')
net.add_edge('integer','identifier6',label='[\d_]')
net.add_edge('in','Dead\nState19',label='[^\d_]')
net.add_edge('int','Dead\nState19',label='[^\d_]')
net.add_edge('inte','Dead\nState19',label='[^\d_]')
net.add_edge('integ','Dead\nState19',label='[^\d_]')
net.add_edge('intege','Dead\nState19',label='[^\d_]')
net.add_edge('integer','Dead\nState19',label='[^\d_]')
##################################################
#start with p
# p','pr','pro','prog','progr','progra','program',
#          'pa','par','para','param','parame','paramet','paramete','parameter',
#           'pri','prin','print

net.add_edge('start','p',label='p\nP')
net.add_edge('p','pr',label='r\nR')
net.add_edge('pr','pro',label='o\nO')
net.add_edge('pro','prog',label='g\nG')
net.add_edge('prog','progr',label='r\nR')
net.add_edge('progr','progra',label='a\nA')
net.add_edge('progra','program',label='m\nM')

net.add_edge('pr','pri',label='i\nI')
net.add_edge('pri','prin',label='n\nN')
net.add_edge('prin','print',label='t\nT')

net.add_edge('p','pa',label='a\nA')
net.add_edge('pa','par',label='r\nR')
net.add_edge('par','para',label='a\nA')
net.add_edge('para','param',label='m\nM')
net.add_edge('param','parame',label='e\nE')
net.add_edge('parame','paramet',label='t\nT')
net.add_edge('paramet','paramete',label='e\nE')
net.add_edge('paramete','parameter',label='r\nR')

net.add_edge('p','identifier12',label='[b-qs-zB-QS-Z0-9_]')
net.add_edge('pr','identifier12',label='[a-hj-np-zA-HJ-NP-Z0-9_]')
net.add_edge('pro','identifier12',label='[a-fh-zA-FH-Z0-9_]')
net.add_edge('prog','identifier12',label='[a-qs-zA-QS-Z0-9_]')
net.add_edge('progr','identifier12',label='[b-zB-Z0-9_]')
net.add_edge('progra','identifier12',label='[a-ln-zA-LN-Z0-9_]')
net.add_edge('program','identifier12',label='[\w_]')

net.add_edge('pri','identifier12',label='[a-mo-zA-MO-Z0-9_]')
net.add_edge('prin','identifier12',label='[a-su-zA-SU-Z0-9_]')
net.add_edge('print','identifier12',label='[\w_]')

net.add_edge('pa','identifier12',label='[a-qs-zA-QS-Z0-9_]')
net.add_edge('par','identifier12',label='[b-zB-Z0-9_]')
net.add_edge('para','identifier12',label='[a-ln-zA-LN-Z0-9_]')
net.add_edge('param','identifier12',label='[a-df-zA-DF-Z0-9_]')
net.add_edge('parame','identifier12',label='[a-su-zA-SU-Z0-9_]')
net.add_edge('paramet','identifier12',label='[a-df-zA-DF-Z0-9_]')
net.add_edge('paramete','identifier12',label='[a-qs-zA-QS-Z0-9_]')
net.add_edge('parameter','identifier12',label='[\w_]')

net.add_edge('p','Dead\nState22',label='[^\w_]')
net.add_edge('pr','Dead\nState22',label='[^\w_]')
net.add_edge('pro','Dead\nState22',label='[^\w_]')
net.add_edge('prog','Dead\nState22',label='[^\w_]')
net.add_edge('progr','Dead\nState22',label='[^\w_]')
net.add_edge('progra','Dead\nState22',label='[^\w_]')
net.add_edge('program','Dead\nState22',label='[^\w_]')

net.add_edge('pr','Dead\nState22',label='[^\w_]')
net.add_edge('pri','Dead\nState22',label='[^\w_]')
net.add_edge('prin','Dead\nState22',label='[^\w_]')
net.add_edge('print','Dead\nState22',label='[^\w_]')

net.add_edge('pa','Dead\nState22',label='[^\w_]')
net.add_edge('par','Dead\nState22',label='[^\w_]')
net.add_edge('para','Dead\nState22',label='[^\w_]')
net.add_edge('param','Dead\nState22',label='[^\w_]')
net.add_edge('parame','Dead\nState22',label='[^\w_]')
net.add_edge('paramet','Dead\nState22',label='[^\w_]')
net.add_edge('paramete','Dead\nState22',label='[^\w_]')
net.add_edge('parameter','Dead\nState22',label='[^\w_]')

net.add_edge('identifier12','identifier12',label='[\w_]')
net.add_edge('identifier12','Dead\nState22',label='[^\w_]')

net.add_edge('Dead\nState22','Dead\nState22',label='⚫')
##################################################
net.add_edge('start','n',label='n\nN')
net.add_edge('n','no',label='o\nO')
net.add_edge('no','non',label='n\nN')
net.add_edge('non','none',label='e\nE')

net.add_edge('n','identifier8',label='[a-np-zA-NP-Z0-9_]')
net.add_edge('no','identifier8',label='[a-mo-zA-MO-Z0-9_]')
net.add_edge('non','identifier8',label='[a-df-zA-DF-Z0-9_]')
net.add_edge('none','identifier8',label='[\w_]')

net.add_edge('n','Dead\nState16',label='[^\w_]')
net.add_edge('no','Dead\nState16',label='[^\w_]')
net.add_edge('non','Dead\nState16',label='[^\w_]')
net.add_edge('none','Dead\nState16',label='[^\w_]')

net.add_edge('identifier8','identifier8',label='[\w_]')
net.add_edge('identifier8','Dead\nState16',label='[^\w_]')

net.add_edge('Dead\nState16','Dead\nState16',label='⚫')
#####################################
net.add_edge('start','e',label='e\nE')
net.add_edge('e','en',label='n\nN')
net.add_edge('en','end',label='d\nD')

net.add_edge('e','el',label='l\nL')
net.add_edge('el','els',label='s\nS')
net.add_edge('els','else',label='e\nE')

net.add_edge('e','identifier7',label='[a-kmo-zA-KMO-Z0-9_]')
net.add_edge('en','identifier7',label='[a-ce-zA-CE-Z0-9_]')
net.add_edge('end','identifier7',label='[\w_]')
net.add_edge('el','identifier7',label='[a-rt-zA-RT-Z0-9_]')
net.add_edge('els','identifier7',label='[a-df-zA-DF-Z0-9_]')
net.add_edge('else','identifier7',label='[\w_]')

net.add_edge('e','Dead\nState13',label='[^\w_]')
net.add_edge('en','Dead\nState13',label='[^\w_]')
net.add_edge('end','Dead\nState13',label='[^\w_]')
net.add_edge('el','Dead\nState13',label='[^\w_]')
net.add_edge('els','Dead\nState13',label='[^\w_]')
net.add_edge('else','Dead\nState13',label='[^\w_]')

net.add_edge('identifier7','identifier7',label='[\w_]')
net.add_edge('identifier7','Dead\nState13',label='[^\w_]')

net.add_edge('Dead\nState13','Dead\nState13',label='⚫')
#####################################
net.add_edge('start','r',label='r\nR')
net.add_edge('r','re',label='e\nE')
net.add_edge('re','rea',label='a\A')
net.add_edge('rea','read',label='d\nD')
net.add_edge('rea','real',label='l\nL')

net.add_edge('r','identifier9',label='[a-df-zA-DF-Z0-9_]')
net.add_edge('re','identifier9',label='[b-zA-B-Z0-9_]')
net.add_edge('rea','identifier9',label='[a-ce-km-zA-CE-KM-Z0-9_]')
net.add_edge('read','identifier9',label='[\w_]')
net.add_edge('real','identifier9',label='[\w_]')

net.add_edge('r','Dead\nState14',label='[^eE\w_]')
net.add_edge('re','Dead\nState14',label='[^aA\w_]')
net.add_edge('rea','Dead\nState14',label='[^lL\w_]')
net.add_edge('read','Dead\nState14',label='[^\w_]')
net.add_edge('real','Dead\nState14',label='[^\w_]')

net.add_edge('identifier9','identifier9',label='[\w_]')
net.add_edge('identifier9','Dead\nState14',label='[^\w_]')

net.add_edge('Dead\nState14','Dead\nState14',label='⚫')
#####################################
net.add_edge('start','c',label='c\nC')
net.add_edge('c','co',label='o\nO')
net.add_edge('co','com',label='m\nM')
net.add_edge('com','comp',label='p\P')
net.add_edge('comp','compl',label='l\nL')
net.add_edge('compl','comple',label='e\nE')
net.add_edge('comple','complex',label='x\X')

net.add_edge('c','ch',label='h\nH')
net.add_edge('ch','cha',label='a\nA')
net.add_edge('cha','char',label='r\R')
net.add_edge('char','chara',label='a\nA')
net.add_edge('chara','charac',label='c\nC')
net.add_edge('charac','charact',label='t\nT')
net.add_edge('charact','characte',label='e\nE')
net.add_edge('characte','character',label='r\nR')

net.add_edge('c','Dead\nState11',label='[^hHoO\w_]')
net.add_edge('ch','Dead\nState11',label='[^aA\w_]')
net.add_edge('cha','Dead\nState11',label='[^rR\w_]')
net.add_edge('char','Dead\nState11',label='[^aA\w_]')
net.add_edge('chara','Dead\nState11',label='[^cC\w_]')
net.add_edge('charac','Dead\nState11',label='[^tT\w_]')
net.add_edge('charact','Dead\nState11',label='[^eE\w_]')
net.add_edge('characte','Dead\nState11',label='[^rR\w_]')
net.add_edge('character','Dead\nState11',label='[\w_]')

net.add_edge('co','Dead\nState11',label='[^mM\w_]')
net.add_edge('com','Dead\nState11',label='[^pP\w_]')
net.add_edge('comp','Dead\nState11',label='[^lL\w_]')
net.add_edge('compl','Dead\nState11',label='[^eE\w_]')
net.add_edge('comple','Dead\nState11',label='[^xX\w_]')
net.add_edge('complex','Dead\nState11',label='[^\w_]')

net.add_edge('c','identifier10',label='[a-gi-np-zA-GI-NP-Z0-9_]')
net.add_edge('ch','identifier10',label='[b-zA-B-Z0-9_]')
net.add_edge('cha','identifier10',label='[a-qs-zA-QS-Z0-9_]')
net.add_edge('char','identifier10',label='[b-zA-B-Z0-9_]')
net.add_edge('chara','identifier10',label='[a-bd-zA-BD-Z0-9_]')
net.add_edge('charac','identifier10',label='[a-su-zA-SU-Z0-9_]')
net.add_edge('charact','identifier10',label='[a-df-zA-DF-Z0-9_]')
net.add_edge('characte','identifier10',label='[a-qs-zA-QS-Z0-9_]')
net.add_edge('character','identifier10',label='[\w_]')

net.add_edge('co','identifier10',label='[a-ln-zA-LN-Z0-9_]')
net.add_edge('com','identifier10',label='[a-oq-zA-OQ-Z0-9_]')
net.add_edge('comp','identifier10',label='[a-km-zA-KM-Z0-9_]')
net.add_edge('compl','identifier10',label='[a-df-zA-DF-Z0-9_]')
net.add_edge('comple','identifier10',label='[a-wy-zA-WY-Z0-9_]')
net.add_edge('complex','identifier10',label='[\w_]')

net.add_edge('identifier10','identifier10',label='[\w_]')
net.add_edge('identifier10','Dead\nState11',label='[^\w_]')

net.add_edge('Dead\nState11','Dead\nState11',label='⚫')
#####################################
net.add_edge('start','l',label='l\nL')
net.add_edge('l','lo',label='o\nO')
net.add_edge('lo','log',label='g\nG')
net.add_edge('log','logi',label='i\I')
net.add_edge('logi','logic',label='c\nC')
net.add_edge('logic','logica',label='a\nA')
net.add_edge('logica','logical',label='l\nL')

net.add_edge('l','identifier4',label='[a-np-zA-NP-Z0-9_]')
net.add_edge('lo','identifier4',label='[a-fh-zA-FH-Z0-9_]')
net.add_edge('log','identifier4',label='[a-hj-zA-HJ-Z0-9_]')
net.add_edge('logi','identifier4',label='[a-bd-zA-BD-Z0-9_]')
net.add_edge('logic','identifier4',label='[b-zB-Z0-9_]')
net.add_edge('logica','identifier4',label='[a-km-zA-KM-Z0-9_]')
net.add_edge('logical','identifier4',label='[\w_]')

net.add_edge('identifier4','Dead\nState10',label='[^\w_]')
net.add_edge('identifier4','identifier4',label='[\w_]')

net.add_edge('l','Dead\nState10',label='[^oO\w_]')
net.add_edge('lo','Dead\nState10',label='[^gG\w_]')
net.add_edge('log','Dead\nState10',label='[^iI\w_]')
net.add_edge('logi','Dead\nState10',label='[^cC\w_]')
net.add_edge('logic','Dead\nState10',label='[^aA\w_]')
net.add_edge('logica','Dead\nState10',label='[^lL\w_]')
net.add_edge('logical','Dead\nState10',label='[\w_]')


net.add_edge('Dead\nState10','Dead\nState10',label='⚫')
#####################################
net.add_edge('start','t',label='t\nT')
net.add_edge('t','th',label='h\nH')
net.add_edge('th','the',label='e\nE')
net.add_edge('the','then',label='n\nN')

net.add_edge('t','identifier3',label='[a-gi-zA-GI-Z0-9_]')
net.add_edge('th','identifier3',label='[a-df-zA-DF-Z0-9_]')
net.add_edge('the','identifier3',label='[a-mo-zA-MO-Z0-9_]')
net.add_edge('then','identifier3',label='[\w_]')

net.add_edge('identifier3','Dead\nState9',label='[^\w_]')
net.add_edge('identifier3','identifier3',label='[\w_]')

net.add_edge('t','Dead\nState9',label='[^hH\w_]')
net.add_edge('th','Dead\nState9',label='[^eE\w_]')
net.add_edge('the','Dead\nState9',label='[^nN\w_]')
net.add_edge('then','Dead\nState9',label='[^\w_]')

net.add_edge('Dead\nState9','Dead\nState9',label='⚫')
#####################################
net.add_edge('start','d',label='d\nD')
net.add_edge('d','do',label='o\nO')

net.add_edge('d','identifier2',label='[a-np-zA-NP-Z0-9_]')
net.add_edge('do','identifier2',label='[\w_]')
net.add_edge('identifier2','identifier2',label='[\w_]')
net.add_edge('identifier2','Dead\nState8',label='[^\w_]')

net.add_edge('d','Dead\nState8',label='[^oO\w_]')
net.add_edge('do','Dead\nState8',label='[^\w_]')
net.add_edge('Dead\nState8','Dead\nState8',label='⚫')
#####################################
net.add_edge('start','v',label='v\nV')
net.add_edge('v','va',label='a\nA')
net.add_edge('va','var',label='r\nR')
net.add_edge('v','identifier5',label='[b-zB-Z0-9_]')
net.add_edge('va','identifier5',label='[a-qs-zA-QS-Z0-9_]')
net.add_edge('var','identifier5',label='[\w_]')
net.add_edge('identifier5','identifier5',label='[\w_]')
net.add_edge('identifier5','Dead\nState7',label='[^\w_]')
net.add_edge('v','Dead\nState7',label='[^aA\w_]')
net.add_edge('va','Dead\nState7',label='[^rR\w_]')
net.add_edge('var','Dead\nState7',label='[^\w_]')
net.add_edge('Dead\nState7','Dead\nState7',label='⚫')
#####################################
net.add_edge('start','=',label='=')
net.add_edge('=','==',label='=')
net.add_edge('=','Dead\nState6',label='[^=]')
net.add_edge('==','Dead\nState6',label='⚫')
net.add_edge('Dead\nState6','Dead\nState6',label='⚫')
#####################################
net.add_edge('start','/',label='/')
net.add_edge('/','/=',label='=')
net.add_edge('/','Dead\nState5',label='[^=]')
net.add_edge('/=','Dead\nState5',label='⚫')
net.add_edge('Dead\nState5','Dead\nState5',label='⚫')
#####################################
net.add_edge('start','>\n<',label='>\n<')
net.add_edge('>\n<','>=\n<=',label='=')
net.add_edge('>\n<','Dead\nState4',label='[^=]')
net.add_edge('>=\n<=','Dead\nState4',label='⚫')
net.add_edge('Dead\nState4','Dead\nState4',label='⚫')
#####################################
net.add_edge('start','*\t,\n(\t)',label='*\t,\n(\t)')
net.add_edge('*\t,\n(\t)','Dead\nState12',label='⚫')
net.add_edge('Dead\nState12','Dead\nState12',label='⚫')
#####################################
net.add_edge('start',':',label=':')
net.add_edge(':','::',label='::')
net.add_edge(':','Dead\nState3',label='[^:]')
net.add_edge('::','Dead\nState3',label='⚫')
net.add_edge('Dead\nState3','Dead\nState3',label='⚫')
#####################################
net.add_edge('start','Dead\nState18',label='[^\w!.\"\'+-=></*,:()]')
net.add_edge('Dead\nState18','Dead\nState18',label='⚫')
net.add_edge('Int\nValue','Real\nValue',label='.')

net.repulsion(node_distance= 300,spring_length=10)
print()
net.write_html("Temp.html",)

