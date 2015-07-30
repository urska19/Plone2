# -*- coding: utf-8 -*-
"""A Folder view that lists Todo Items."""

from Products.ATContentTypes.interface import IATFolder
from five import grok
from plone import api
from plone.dexterity.content import Container

import json

# Search for templates in the "templates" directory.
# Hopefully this line won't be needed in the future as I hope that we can tell
# grok to look there by default.
grok.templatedir('templates')


class Todo(grok.View):
    """A BrowserView to display the Todo listing on a Folder."""

    grok.context(IATFolder)  # type of object on which this View is available
    grok.require('zope2.View')  # what permission is needed for access


class WorkflowTransition(grok.View):
    """Change the state of an item.
    The context is implied by the url. Returns state of the object after the
    transition, and possible transitions in that state.
    """

    grok.context(Container)  # type of object on which this View is available
    grok.require('zope2.View')  # what permission is needed for access
    grok.name('update_workflow')  # on what URL will this view be available

    def render(self):
        """Render the @@update_workflow view response."""

        # the submitted form variables are stored in the request object
        transition = self.request.form.get('transition', '')
        results = {
            'results': None,
            'success': False,
            'message': ''
        }

        if transition:
            try:
                # set the new state by running a transition
                api.content.transition(self.context, transition=transition)
                results['success'] = True
            except api.exc.InvalidParameterError, e:
                results['message'] = "%s" % e

            results['results'] = {
                'state': api.content.get_state(self.context),
                'transitions': self.get_possible_transitions(self.context),
            }

        # set the right header for sending a JSON response
        self.request.response.setHeader(
            'Content-Type', 'application/json; charset=utf-8')
        return json.dumps(results)

    def get_possible_transitions(self, item):
        """Return available transitions for an item."""
        workflow_tool = api.portal.get_tool('portal_workflow')
        items = workflow_tool.getTransitionsFor(item)
        return [i['id'] for i in items]
