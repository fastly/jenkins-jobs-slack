import xml.etree.ElementTree as XML


def slack_properties(parser, xml_parent, data):
    """yaml: slack

    Example::

      properties:
        - slack:
            notify-start: true
            notify-success: true
            notify-aborted: true
            notify-notbuilt: true
            notify-unstable: true
            notify-failure: true
            notify-backtonormal: true
            room: '#jenkins'
    """
    if data is None:
        data = dict()

    notifier = XML.SubElement(
        xml_parent, 'jenkins.plugins.slack.SlackNotifier_-SlackJobProperty')
    notifier.set('plugin', 'slack@1.2')

    if 'room' in data :
        XML.SubElement(notifier, 'room').text = data['room']

    for opt, attr in (('notify-start', 'startNotification'),
                      ('notify-success', 'notifySuccess'),
                      ('notify-aborted', 'notifyAborted'),
                      ('notify-notbuilt', 'notifyNotBuilt'),
                      ('notify-unstable', 'notifyUnstable'),
                      ('notify-failure', 'notifyFailure'),
                      ('notify-backtonormal', 'notifyBackToNormal')):
        (XML.SubElement(notifier, attr)
         .text) = data.get(opt, True) and 'true' or 'false'


def slack_publisher(parser, xml_parent, data):
    """yaml: slack

    Example::

      publishers:
        - slack:
            team-domain: example.com
            auth-token: secret
            build-server-url: https://jenkins.example.com
            room: '#jenkins'
    """

    # extract defaults from the plugin configuration,
    # just like the UI does
    defaults = {}
    try:
        et = XML.parse('/var/lib/jenkins/jenkins.plugins.slack.SlackNotifier.xml')
        for (nn, opt) in (('teamDomain', 'team-domain'),
                          ('token', 'auth-token'),
                          ('room', 'room'),
                          ('buildServerUrl', 'build-server-url')):
            node = et.find(nn)
            if node is not None :
                defaults[opt] = node.text
    except IOError:
        pass

    notifier = XML.SubElement(
        xml_parent, 'jenkins.plugins.slack.SlackNotifier')
    notifier.set('plugin', 'slack@1.2')

    for (opt, attr) in (('team-domain', 'teamDomain'),
                        ('auth-token', 'authToken'),
                        ('build-server-url', 'buildServerUrl'),
                        ('room', 'room')):
        if opt in data :
            XML.SubElement(notifier, attr).text = data[opt]
        elif opt in defaults :
            XML.SubElement(notifier, attr).text = defaults[opt]
