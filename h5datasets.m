% Return all  DataSets with some key info

function h = h5datasets(file)

  h5i = h5info(file);
  h = struct('Name', {}, 'Dataspace', {}, 'Datatype', {}, 'offset', {}, ...
    'size', {}, 'byte_order', {}, 'type', {});
  groups(h5i);
  typedetails();

  % End of main function

  function groups(g)
    for i = 1:length(g)
      datasets(g(i).Name, g(i).Datasets);
      groups(g(i).Groups);
    end
  end

  function datasets(p, d)
    if p(end) ~= '/', p(end + 1) = '/'; end
    for i = 1:length(d)
      h(end + 1).Name = strcat(p, d(i).Name);
      h(end).Dataspace = d(i).Dataspace;
      h(end).Datatype = d(i).Datatype;
    end
  end

  function typedetails()
    fid = H5F.open(file);
    for j = 1:length(h)
      dset_id = H5D.open(fid, h(j).Name);
      h(j).size = H5D.get_storage_size(dset_id);
      try
        h(j).offset = H5D.get_offset(dset_id);
      catch
        h(j).offset = -1;
      end

      type_id = H5D.get_type(dset_id);

      bo = H5T.get_order(type_id);
      % Byte order
      switch bo
        case 0
          h(j).byte_order = 'H5T_ORDER_LE';
        case 1
          h(j).byte_order = 'H5T_ORDER_BE';
        case 2
          h(j).byte_order = 'H5T_ORDER_VAX';
        case 3
          % Not yet exists in MatLab
          h(j).byte_order = 'H5T_ORDER_MIXED';
        case 4
          h(j).byte_order = 'H5T_ORDER_NONE';
        case (-1)
          h(j).byte_order = 'H5T_ORDER_ERROR';
      end

      dt = h(j).Datatype;
      switch dt.Class
        case 'H5T_FLOAT'
          if dt.Size == 4
            h(j).type = 'single';
          elseif dt.Size == 8
            h(j).type = 'double';
          end

        case 'H5T_INTEGER'
          h(j).type = sprintf('int%d', dt.Size * 8);
          if ~H5T.get_sign(type_id)
            h(j).type = strcat('u', h(j).type);
          end
      end
      H5T.close(type_id);
      H5D.close(dset_id);
    end
    h(end + 1).Name = '/';
    h(end).offset = 0;
    h(end).size = H5F.get_filesize(fid);
    H5F.close(fid);
  end
end
