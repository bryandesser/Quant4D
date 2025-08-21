% Function to get the text of selected items in list/dropdown objects
function nm = getSelectTxt(obj)
  if ismember(obj.Type, "uibuttongroup")
    nm = string(obj.SelectedObject.Text);
  elseif isempty(obj.ItemsData)
    nm = string(obj.Value);
  else
    nm = string(obj.Items(ismember(obj.ItemsData, obj.Value)));
  end
end
