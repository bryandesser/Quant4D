% Rotation matrix, for degree input
function R = rotMatD(d)
  R = [cosd(d), sind(d); -sind(d), cosd(d)];
end