/* global require */

var SKIP_OVERLAY_ACTIONS = [
  'plone.actions.Delete'
];

require([
  'jquery',
  'mockup-patterns-modal'
], function($, Modal) {
  'use strict';
  function initforms(){
    $('#configure-conditions .rule-element input, #configure-actions .rule-element input').unbind('click').click(function(){
      var name = $(this).attr('name');
      if(name=='form.button.EditCondition' || name=='form.button.EditAction'){
        return true;
      }
      $('#spinner').show();
      var form = $(this).parents('form').first();
      var fieldset = form.parents('fieldset').first();
      var data = form.serialize() + '&' + name + '=1';
      var url = form.attr('action');
      $.post(url, data, function(html){
        var newfieldset = $(html).find('#' + fieldset.attr('id'));
        fieldset.replaceWith(newfieldset);
        initforms();
        $('#spinner').hide();
      });
      return false;
    });

    $('input[name="form.button.AddCondition"],input[name="form.button.AddAction"]').unbind('click').click(function(e){
      var form = $(this).parent().parent();
      var data = form.serialize();
      for(var i=0; i<SKIP_OVERLAY_ACTIONS.length; i++){
        if(data.indexOf(SKIP_OVERLAY_ACTIONS[i]) !== -1){
          return;
        }
      }
      e.preventDefault();
      var url = form.attr('action') + '?' + data;
      var conditionAnchor = $('<a href="' + url + '" />').css('display', 'none');
      conditionAnchor.insertAfter(this);
      new Modal(conditionAnchor);
      conditionAnchor.trigger('click');
    });
  }
  $(document).ready(function(){
    initforms();
  });
});
  /* To enable ajax overlay loading with the current widget
     used for the add button, we'll create a hidden anchor
     tag that'll we'll manually trigger clicks for.
     We'll add one for conditions and one for actions. */
