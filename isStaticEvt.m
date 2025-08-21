% Function to test whether an event is NOT "MovingROI" or "ValueChanging"; return `true` for `[]` etc.
function nc = isStaticEvt(evt)
  nc = isempty(evt) || ~(isfield(evt,'EventName') || isprop(evt,'EventName')) || isempty(evt.EventName) ...
    || ~ismember(evt.EventName, ["MovingROI" "ValueChanging"]);
end