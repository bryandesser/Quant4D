% Wrapper for `OnOffSwitchState()`
function out = switchOnOff(s)
  out = string(matlab.lang.OnOffSwitchState(s));
end