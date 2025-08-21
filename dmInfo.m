% Can read DM3/4 images.

% http://phyweb.physics.nus.edu.sg/~phybcb/info/dmformat/index.html#dm4
% https://imagej.nih.gov/ij/plugins/DM3Format.gj.html
% https://openncem.readthedocs.io/en/latest/ncempy.io.html
% https://bitbucket.org/ercius/openncem/src/master/dm4Reader.m

% msg_opt:  0) no message;
%           1) print TagGroups in console;
%           2) print to TXT suffixed with '_tags.txt'.
%
% info_opt: 0) skip array reading, read only `ImageList` & `ImageSourceList`, return only image info;
%           1) skip array reading, return whole Root TagGroup;
%           2) read array (for debug purpose; very slow), return whole Root TagGroup.
%
% Default: dmInfo('path') = dmInfo('path',0,0)

function DMinfo = dmInfo(file, msg_opt, info_opt)
arguments
    file
    msg_opt = 0
    info_opt = 0
end

ff = [];
ff.io = info_opt;

[ff.id, errmsg] = fopen(file, 'rb');
if ff.id == -1, DMinfo = errmsg; return; end

% Message printing options
ff.m = 0;
if msg_opt == 2
    [ff.m, errmsg] = fopen(strcat(file, '_tags.txt'), 'w');
    if ff.m == -1, DMinfo = errmsg; return; end
elseif msg_opt == 1
    ff.m = 1;
end

% Setup DM3 & 4 differences
ff.v = fread(ff.id, 1, 'uint32', 'b');
switch ff.v
    case 3
        ff.w = 'uint32';
    case 4
        ff.w = 'uint64';
    otherwise
        DMinfo = 'Not a DM3/4 file.';
        return
end

% Size of the root tag group, i.e. 24/16 bytes for DM4/3 (header + footer) smaller than the file size
ff.size = fread(ff.id, 1, ff.w, 'b');

% Data endianness; probably only little ff.bo for DM4
endian = fread(ff.id, 1, 'uint32', 'b');

foprintf(ff.m, '"%s"\nDM version=%d, Little Endian=%d\nRoot Tag Group size=%d bytes ', ...
    file, ff.v, endian, ff.size)

if endian
    ff.bo = 'l';
else
    ff.bo = 'b';
end

% Read TagGroup
Tg = readTagGp(ff, 0);

% Finished file reading
fclose(ff.id);
if ff.m > 2, fclose(ff.m); end

% Deal with `ImageSourceList`
nImgs = length(Tg.ImageSourceList);
R = zeros(nImgs, 1);
for i = 1:nImgs
    R(i) = Tg.ImageSourceList{i}.ImageRef + 1;
end

% Deal with  `ImageList[i]:ImageData:DataType` & `ImageList[i].Name`
for i = 1:nImgs
    dt = Tg.ImageList{R(i)}.ImageData.DataType;
    Tg.ImageList{R(i)}.ImageData.ImageDataType = imgDataType(dt);
    Tg.ImageList{R(i)}.ImageData.Name = sprintf('%s', Tg.ImageList{R(i)}.Name{:});
end

% Setup return
if ff.v == 4
    d.fileSize = ff.size + 24;
else
    d.fileSize = ff.size + 20;
end
d.version = ff.v;
d.liEndian = endian;

if ff.io == 0
    DMinfo = cell(nImgs, 1);
    for i = 1:nImgs
        DMinfo{i} = Tg.ImageList{R(i)}.ImageData;
    end
    DMinfo{end + 1} = d;
else
    DMinfo = Tg;
    DMinfo.file = d;
end

% End of main()

% Read Tag directory
    function Gp = readTagGp(ff, lv)
        f = ff.id;
        m = ff.m;
        Gp = [];

        % Tag Group or Tag List
        notList = fread(f, 1, 'uint8'); % 0 = Tag List, 1 = Tag Group
        tOpen = fread(f, 1, 'uint8');
        nChd = fread(f, 1, ff.w, 'b');

        if notList
            foprintf(m, '(Tag Group, ');
        else
            foprintf(m, '(Tag List, ')
            Gp = cell(nChd, 1);
        end

        foprintf(m, 'open=%d, nTags=%d)\n', tOpen, nChd)

        for iC = 1:nChd
            fprintf("ff.offset = %d\n",ftell(ff.id))
            if ftell(ff.id)==2549568
                999
            elseif ftell(ff.id)==18474
                999
            end
            tPos = ftell(f);
            tagType = fread(f, 1, 'uint8');
            labelSize = fread(f, 1, 'uint16', 'b');
            foprintf(m, '%*s', lv * 4, "")
            label = "";

            if notList
                label0 = fread(f, [1, labelSize], 'uint8=>char', 'b');
                foprintf(m, '"%s" ', label0)
                label = regexprep(regexprep(label0, '[^a-zA-Z_0-9]+', '_'), '^[_0-9]+', '');
                if isempty(label), label = 'LABEL_FORMATTED_'; end

                %iL = 1;
                %while isfield(Gp, label)
                %    label = strcat(label, num2str(iL));
                %    iL = iL +1;
                %end

                if isfield(Gp,label)
                    iL = 1;
                    while isfield(Gp,[label,num2str(iL)])
                        iL = iL+1;
                    end
                    label = [label,num2str(iL)];
                end


                if ~strcmp(label, label0)
                    foprintf(m, '(formatted as "%s") ', label)
                end
            else
                foprintf(m, '%d. ', iC)
            end

            foprintf(m, '@%d ', tPos);

            if ff.v == 4
                tagSize = fread(f, 1, ff.w, 'b');
                % Skip other Tags for `info_opt == 0`
                if lv == 0 && ff.io == 0 && (~ismember(label, ["ImageList", "ImageSourceList"]))
                    if fseek(f, tagSize, 'cof') < 0
                        foprintf(m, '\n`fseek()` error encountered.');
                    end
                    %foprintf(m, '\n%*sTagGroup skipped\n', (lv +1) * 4, "")
                    continue
                end
            end

            switch tagType
                case 20
                    chd = readTagGp(ff, lv + 1);
                case 21
                    chd = readTag(ff, lv + 1, label);
                case 0
                    foprintf(m, 'EOF_OR_WRONG_POSITION\n');
                otherwise
                    foprintf(m, '\nUnknown object encountered; not a Tag nor a Tag Group: %d.', tagType);
            end

            if notList
                Gp.(label) = chd;
            else
                Gp{iC} = chd;
            end
        end

        % Read Tag that is not directory
        function Tg = readTag(ff, lv, label)
            f = ff.id;
            m = ff.m;
            tmp = fread(f, [1, 4], 'uint8=>char'); % "%%%%" for Tag
            nTagType = fread(f, 1, ff.w, 'b');
            tagType = fread(f, nTagType, ff.w, 'b');
            offset = ftell(f);
            foprintf(m, '(offset@%d, nTagType=%d, ', offset, nTagType)

            nA = 1;
            nM = 1;
            isArray = 0;
            isMultiItem = 0;

            if tagType(1) == 20
                isArray = 1;
                nA = tagType(nTagType);
                foprintf(m, 'an array of %d ', nA)
            end

            if tagType(1 + isArray) == 15
                nM = tagType(3 + isArray);
                foprintf(m, 'multiItem of [ ')
                isMultiItem = 1;
            end

            sTypes = zeros(nM, 1);
            sTypes_s = cell(nM, 1);
            sTypes_b = zeros(nM, 1);
            for iM = 1:nM
                sTypes(iM) = tagType(isArray + 3 * isMultiItem + iM * (1 + isMultiItem));
                sTypes_s{iM} = dbgDMBin(sTypes(iM));
                sTypes_b(iM) = dmBin(sTypes(iM), 'b');
            end

            foprintf(m, '%s ', sTypes_s{:})
            if isMultiItem, foprintf(m, ']'); end
            foprintf(m, ')\n%*s= ', (lv + 1) * 4, "")
            if isArray, foprintf(m, '[ '); end

            if ff.io < 2 && isArray && (~endsWith(label, "Name"))
                % Skip data reading if selected not to read array
                Tg.offset = offset;
                foprintf(m, 'Array reading skipped ')

                if isMultiItem
                    Tg.dim = [nM, nA];
                    Tg.tagType = "array of multiItems";
                else
                    Tg.dim = nA;
                    Tg.tagType = "array of scalars";
                end

                Tg.dataType = sTypes_s{:};
                aSize = sum(sTypes_b) * nA;
                Tg.size = aSize;
                if fseek(f, aSize, 'cof') < 0
                    foprintf(m, '\n`fseek()` error encountered.');
                end

            else
                % Read data in tag
                aTg = cell(nA, 1);
                for iA = 1:nA
                    if isMultiItem, foprintf(m, '[ '); end

                    mTg = cell(nM, 1);
                    for iM = 1:nM
                        mTg{iM} = fread(f, 1, dmBin(sTypes(iM), 'p'), ff.bo);
                        foprintf(m, '%g ', mTg{iM})
                    end

                    if isMultiItem
                        aTg{iA} = mTg;
                        foprintf(m, '] ')
                    else
                        aTg{iA} = mTg{1};
                    end
                end

                if isArray
                    Tg = aTg;
                    if sTypes(1) == 4 && (~isMultiItem)
                        foprintf(m, ']\n%*s= [ "', (lv + 1) * 4, "")
                        foprintf(m, '%s', aTg{:})
                        foprintf(m, '" ')
                    end
                else
                    Tg = aTg{1};
                end
            end

            if isArray, foprintf(m, ']'); end
            foprintf(m, '\n')

        end
    end

% Message fprintf() with option
    function foprintf(m, varargin)
        if m, fprintf(m, varargin{:}); end
    end

    function dbt = dbgDMBin(btype)
        if btype == 8
            dbt = "int8 (boolean)";
        else
            dbt = dmBin(btype, 'p');
        end
    end

% Identify DM scalar type for byte reading
    function prc_bytes = dmBin(btype, out_type)
        switch btype
            case 2, p = "int16"; b = 2;
            case 3, p = "int32"; b = 4;
            case 4, p = "uint16"; b = 2; % OR Unicode string
            case 5, p = "uint32"; b = 4;
            case 6, p = "single"; b = 4;
            case 7, p = "double"; b = 8;
            case 8, p = "int8"; b = 1; % Boolean
            case 9, p = "int8"; b = 1;
            case 10, p = "uint8"; b = 1;
            case 11, p = "int64"; b = 8;
            case 12, p = "uint64"; b = 8;
            case 15, p = "TagGroup"; b = NaN;
            case 18, p = "String"; b = NaN;
            case 20, p = "Array"; b = NaN;
            otherwise, p = "Unknown type"; b = NaN;
        end

        if out_type == 'p'
            prc_bytes = p;
        elseif out_type == 'b'
            prc_bytes = b;
        end
    end

% Pack Image Data Type info
    function imgInfo = imgDataType(dt)
        imgInfo.full = dmImageType(dt, 'full');
        imgInfo.pixel = dmImageType(dt, 'pixel');
        imgInfo.scalar = dmImageType(dt, 'scalar');
        imgInfo.variant = dmImageType(dt, 'variant');
        imgInfo.bit = dmImageType(dt, 'bit');
    end

% DM Image Data Type
    function d = dmImageType(iT, oo)
        switch iT
            case 1, px = "scalar"; sc = "int"; vt = 0; bit = 16;
            case 2, px = "scalar"; sc = "float"; vt = 0; bit = 32;
            case 3, px = "complex"; sc = "float"; vt = 0; bit = 32;
            case 5, px = "complex"; sc = "float"; vt = 0; bit = 32;
            case 6, px = "scalar"; sc = "uint"; vt = 0; bit = 8;
            case 7, px = "scalar"; sc = "int"; vt = 0; bit = 32;
            case 8, px = "rgba"; sc = "uint"; vt = 3; bit = 8;
            case 9, px = "scalar"; sc = "int"; vt = 0; bit = 8;
            case 10, px = "scalar"; sc = "uint"; vt = 0; bit = 16;
            case 11, px = "scalar"; sc = "uint"; vt = 0; bit = 32;
            case 12, px = "scalar"; sc = "float"; vt = 0; bit = 64;
            case 13, px = "complex"; sc = "float"; vt = 0; bit = 64;
            case 14, px = "scalar"; sc = "binary"; vt = 0; bit = 8;
            case 15, px = "rgb"; sc = "uint"; vt = 0; bit = 8;
            case 16, px = "rgb"; sc = "uint"; vt = 1; bit = 8;
            case 17, px = "rgb"; sc = "uint"; vt = 0; bit = 16;
            case 18, px = "rgb"; sc = "float"; vt = 0; bit = 32;
            case 19, px = "rgb"; sc = "float"; vt = 0; bit = 64;
            case 20, px = "rgba"; sc = "uint"; vt = 0; bit = 8;
            case 21, px = "rgba"; sc = "uint"; vt = 1; bit = 8;
            case 22, px = "rgba"; sc = "uint"; vt = 2; bit = 8;
            case 23, px = "rgba"; sc = "uint"; vt = 3; bit = 8;
            case 24, px = "rgba"; sc = "uint"; vt = 0; bit = 16;
            case 25, px = "rgba"; sc = "float"; vt = 0; bit = 32;
            case 26, px = "rgba"; sc = "float"; vt = 0; bit = 64;
            case 27, px = "complex"; sc = "float"; vt = 0; bit = 32;
            case 28, px = "complex"; sc = "float"; vt = 0; bit = 64;
            case 29, px = "point2"; sc = "int"; vt = 0; bit = 16;
            case 30, px = "point2"; sc = "int"; vt = 1; bit = 16;
            case 31, px = "point2"; sc = "int"; vt = 0; bit = 64;
            case 32, px = "point2"; sc = "float"; vt = 0; bit = 32;
            case 33, px = "point2"; sc = "float"; vt = 0; bit = 64;
            case 34, px = "rect"; sc = "int"; vt = 1; bit = 16;
            case 35, px = "rect"; sc = "int"; vt = 1; bit = 64;
            case 36, px = "rect"; sc = "float"; vt = 1; bit = 32;
            case 37, px = "rect"; sc = "float"; vt = 0; bit = 32;
            case 38, px = "rect"; sc = "float"; vt = 0; bit = 64;
            case 39, px = "scalar"; sc = "int"; vt = 0; bit = 64;
            case 40, px = "scalar"; sc = "uint"; vt = 0; bit = 64;
            otherwise, px = ""; sc = ""; vt = NaN; bit = NaN;
        end
        switch oo
            case 'pixel'
                d = px;
            case 'scalar'
                d = sc;
            case 'variant'
                d = vt;
            case 'bit'
                d = bit;
            otherwise
                d = strtrim(sprintf('%s %s%d', px, sc, bit));
        end
    end
end
