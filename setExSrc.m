% Set properties of objects that are not `src` if it is a changing event
function setExSrc(evt, obj, varargin)
  src = evt.Source;
  % If not a changing event, set source as well
  if isStaticEvt(evt) || isempty(src), src = {[]}; end 
  if ischar(src), src = string(src); end
  obj = obj(:);
  logi = obj ~= src;
  for i=1:numel(varargin)/2
    prop = varargin{2*i-1};  val = varargin{2*i};
    if iscell(prop) && all(numel(obj) == numel(prop)), prop = prop(logi); end
    if iscell(val) && all(numel(obj) == numel(val)), val = val(logi); end
    set(obj(logi),prop,val);
  end
end