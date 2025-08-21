function varargout = DPC_Quant(varargin)
% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
    'gui_Singleton',  gui_Singleton, ...
    'gui_OpeningFcn', @DPC_Quant_OpeningFcn, ...
    'gui_OutputFcn',  @DPC_Quant_OutputFcn, ...
    'gui_LayoutFcn',  [] , ...
    'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT

% --- Executes just before DPC_Quant is made visible.
function DPC_Quant_OpeningFcn(hObject, eventdata, handles, varargin)
% Choose default command line output for DPC_Quant
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

function varargout = DPC_Quant_OutputFcn(hObject, eventdata, handles)
% Get default command line output from handles structure
varargout{1} = handles.output;

%% Callback Functions
function save_images_Callback(hObject, eventdata, handles)
% Save as 32-bit Tiff images

tagstruct.ImageLength = handles.framesx; 
tagstruct.ImageWidth = handles.framesy;
tagstruct.Photometric = Tiff.Photometric.MinIsBlack;
tagstruct.BitsPerSample = 32;
tagstruct.SamplesPerPixel = 1;
tagstruct.PlanarConfiguration = Tiff.PlanarConfiguration.Chunky;

t=Tiff('image_a.tif','w');setTag(t,tagstruct);write(t,uint32(imrotate(handles.images.x1,-90)));
t=Tiff('image_b.tif','w');setTag(t,tagstruct);write(t,uint32(imrotate(handles.images.x2,-90)));
t=Tiff('image_c.tif','w');setTag(t,tagstruct);write(t,uint32(imrotate(handles.images.x3,-90)));
t=Tiff('image_d.tif','w');setTag(t,tagstruct);write(t,uint32(imrotate(handles.images.x4,-90)));
t=Tiff('image_ac.tif','w');setTag(t,tagstruct);write(t,uint32(imrotate(handles.images.ac,-90)));
t=Tiff('image_bd.tif','w');setTag(t,tagstruct);write(t,uint32(imrotate(handles.images.bd,-90)));
t=Tiff('image_vector_mag.tif','w');setTag(t,tagstruct);write(t,uint32(imrotate(handles.dpc_mag,-90)));

temp_image=uint8((handles.dpc_angle-min(min(handles.dpc_angle)))./(2*pi)*2^8);
imwrite(temp_image,jet(2^8),'image_vector_angle.tif');

function adf_inner_Callback(hObject, eventdata, handles)
delete(handles.inner_disk);
if strcmp(hObject.Style,'slider')
    handles.adf_inner_angle=get(hObject,'Value');
    set(handles.adf_inner_value,'Value',handles.adf_inner_angle,'String',handles.adf_inner_angle*handles.mrad_per_pix);
else
    handles.adf_inner_angle=str2double(get(hObject,'String'))/handles.mrad_per_pix;
    set(handles.adf_inner,'Value',handles.adf_inner_angle);
end
handles.inner_disk=viscircles(handles.center,handles.adf_inner_angle,'Color','g');

temp=fieldnames(handles.seg);
for ii=1:size(temp,1)
    delete(handles.seg.(temp{ii}));
end

handles.temp_angle=handles.det_angle.Value;
for i=1:handles.n_seg
    handles.seg.(strcat('x',num2str(i)))=plot(cos(handles.temp_angle)*[handles.adf_inner_angle handles.adf_outer_angle]+handles.center(1),sin(handles.temp_angle)*[handles.adf_inner_angle handles.adf_outer_angle]+handles.center(2),':b','LineWidth',4);
    handles.temp_angle=handles.temp_angle+2*pi/handles.n_seg;
end
set(handles.adf_inner_value,'String',handles.adf_inner_angle*handles.mrad_per_pix);
guidata(hObject,handles)

function adf_outer_Callback(hObject, eventdata, handles)
delete(handles.outer_disk);
if strcmp(hObject.Style,'slider')
    handles.adf_outer_angle=get(hObject,'Value');
    set(handles.adf_outer_value,'Value',handles.adf_outer_angle,'String',handles.adf_outer_angle*handles.mrad_per_pix);
else
    handles.adf_outer_angle=str2double(get(hObject,'String'))/handles.mrad_per_pix;
    set(handles.adf_outer,'Value',handles.adf_outer_angle);
end
handles.outer_disk=viscircles(handles.center,handles.adf_outer_angle,'Color','r');

temp=fieldnames(handles.seg);
for ii=1:size(temp,1)
    delete(handles.seg.(temp{ii}));
end

for i=1:handles.n_seg
    handles.seg.(strcat('x',num2str(i)))=plot(cos(handles.temp_angle)*[handles.adf_inner_angle handles.adf_outer_angle]+handles.center(1),sin(handles.temp_angle)*[handles.adf_inner_angle handles.adf_outer_angle]+handles.center(2),':b','LineWidth',4);
    handles.temp_angle=handles.temp_angle+2*pi/handles.n_seg;
end
set(handles.adf_outer_value,'String',handles.adf_outer_angle*handles.mrad_per_pix);
guidata(hObject,handles)

function det_angle_Callback(hObject, eventdata, handles)
if strcmp(hObject.Style,'slider')
    handles.det_angle.Value=get(hObject,'Value');
    set(handles.det_angle_value,'Value',handles.det_angle.Value,'String',handles.det_angle.Value*180/pi);
else
    handles.det_angle.Value=str2double(get(hObject,'String'))*pi/180;
    set(handles.det_angle,'Value',handles.det_angle.Value);
end

handles.temp_angle=handles.det_angle.Value;
temp=fieldnames(handles.seg);
for ii=1:size(temp,1)
    delete(handles.seg.(temp{ii}));
end

for i=1:handles.n_seg
    handles.seg.(strcat('x',num2str(i)))=plot(cos(handles.temp_angle)*[handles.adf_inner_angle handles.adf_outer_angle]+handles.center(1),sin(handles.temp_angle)*[handles.adf_inner_angle handles.adf_outer_angle]+handles.center(2),':b','LineWidth',4);
    handles.temp_angle=handles.temp_angle+2*pi/handles.n_seg;
end

%set(handles.det_angle_value,'String',handles.det_angle.Value*180/pi);
guidata(hObject,handles)

function import_data_Callback(hObject, eventdata, handles)
    % Clear any plots before importing or re-importing any data to clean up
    % the workspace
    clear handles.img handles.data 
    cla(handles.detector_layout);
    cla(handles.seg_a);
    cla(handles.seg_b);
    cla(handles.seg_c);
    cla(handles.seg_d);
    cla(handles.seg_ac);
    cla(handles.seg_bd);
    cla(handles.vect_angle);
    cla(handles.vect_mag);

    % Hide all of the plots, sliders, text, and buttons before importing or
    % re-importing data for cleanliness
    set(handles.trans_beam_radius,'Visible','off');set(handles.trans_beam_radius_text,'Visible','off');
    set(handles.trans_beam_x,'Visible','off');set(handles.trans_beam_x_text,'Visible','off');
    set(handles.trans_beam_y,'Visible','off');set(handles.trans_beam_y_text,'Visible','off');
    set(handles.align_trans_beam,'String','Finish Alignment');set(handles.align_trans_beam,'Visible','off');
    set(handles.adf_inner,'Visible','off');set(handles.adf_inner_text,'Visible','off');set(handles.adf_inner_value,'Visible','off');set(handles.adf_inner_unit,'Visible','off');
    set(handles.adf_outer,'Visible','off');set(handles.adf_outer_text,'Visible','off');set(handles.adf_outer_value,'Visible','off');set(handles.adf_outer_unit,'Visible','off');
    set(handles.det_angle,'Visible','off');set(handles.det_angle_text,'Visible','off');set(handles.det_angle_value,'Visible','off');set(handles.det_angle_unit,'Visible','off');
    set(handles.display_images,'Visible','off');
    set(handles.seg_a,'Visible','off');set(handles.seg_a_text,'Visible','off');set(get(handles.seg_a,'children'),'visible','off')
    set(handles.seg_b,'Visible','off');set(handles.seg_b_text,'Visible','off');set(get(handles.seg_b,'children'),'visible','off')
    set(handles.seg_c,'Visible','off');set(handles.seg_c_text,'Visible','off');set(get(handles.seg_c,'children'),'visible','off')
    set(handles.seg_d,'Visible','off');set(handles.seg_d_text,'Visible','off');set(get(handles.seg_d,'children'),'visible','off')
    set(handles.seg_ac,'Visible','off');set(handles.seg_ac_text,'Visible','off');set(get(handles.seg_ac,'children'),'visible','off')
    set(handles.seg_bd,'Visible','off');set(handles.seg_bd_text,'Visible','off');set(get(handles.seg_bd,'children'),'visible','off')
    set(handles.vect_mag,'Visible','off');set(handles.vect_mag_text,'Visible','off');set(get(handles.vect_mag,'children'),'visible','off')
    set(handles.vect_angle,'Visible','off');set(handles.vect_angle_text,'Visible','off');set(get(handles.vect_angle,'children'),'visible','off')
    set(handles.save_images,'Visible','off');
    
% Allow for importing binary files with extensions:
%   .mib	-   Medipix
%   .raw	-	ImageJ, Fiji, Matlab, etc.
[filename,pathname]=uigetfile({'*.mib';'*.raw'});
cd(pathname)
s=dir(strcat(pathname,filename));

% Ask the user for some basic parameters of the 4D data set and save them
% to the GUI structure (handles)
% nopiy, nopix      -	number of pixels in the diffraction pattern  
% framesy, framesx	-	number of probe positions in the image
% bitdepth          -   bitdepth of the dataset
% alpha             -   probe convergence semi-angle in mrad
[handles.nopiy,handles.nopix,handles.framesy,handles.framesx,handles.bitdepth,handles.alpha] = import_4dstem({filename});
handles.frames=handles.framesx*handles.framesy;

% Account for differences in the way Merlin (Medipix) and Fiji store data
% in binary format. The gap in .mib files all seem to be 384 bytes, though
% this could potentially be different for different versions of the
% detector and/or software
if strcmp(filename(end-2:end),'raw')
    gap=0;
else
    gap=384;
end

% List of the possible bit-depths, their precision in Matlab, and their
% size in bytes
bitdepth={'1-bit',  'ubit1',    1/8;
           '6-bit', 'uint8',    1;
           '8-bit', 'uint8',    1;
           '12-bit','uint16',   2;
           '16-bit','uint16',   2;
           '24-bit','uint32',   4;
           '32-bit','uint32',   4;
           '64-bit','uint64',   8};

% Set precision and the gap size before importing via bitdepth from user
% input dialog
gap=gap/bitdepth{strcmp(handles.bitdepth,bitdepth(:,1)),3};
bitdepth=bitdepth{strcmp(handles.bitdepth,bitdepth(:,1)),2};
filesize=s.bytes; framesize=filesize/handles.frames;

% Open the user-selected file for reading
fid=fopen(strcat(pathname,filename),'r');

% Pre-allocate the array for speed
handles.data.raw=zeros(handles.nopiy*handles.nopix,handles.frames,bitdepth);

% Read in the 4D dataset in bunches the size of one diffraction pattern and
% loop over the total number of diffraction patterns (# of probe positions)
import_bar=waitbar(0,'Importing Data...');
for j=1:handles.frames
    if mod(j,100)==0 tic; end
    fread(fid,gap,bitdepth,0,'b');
    handles.data.raw(1:handles.nopiy*handles.nopix,j)=fread(fid,handles.nopiy*handles.nopix,bitdepth,0,'b');
    if mod(j,100)==0 waitbar(j/handles.frames,import_bar,sprintf('%.1f%% Complete\n%.2f MB/s',100*j/handles.frames,framesize/toc/1e6)); end
end
fclose(fid);

% Create a summed image of all diffraction patterns simply for display
% purposes and alignment and calibration
handles.img=sum(reshape(handles.data.raw,[handles.nopiy handles.nopix handles.frames]),3);
imagesc(handles.img,'Parent', handles.detector_layout);
set(handles.detector_layout,'DataAspectRatio',[1 1 1],'Colormap',gray,'XTick',[],'Ytick',[],'XLim',[0 handles.nopix],'YLim',[0 handles.nopiy],'Tag','detector_layout');
delete(import_bar)

% Align transmitted beam
handles.center0=[handles.nopix/2 handles.nopiy/2];
handles.rmax=min(handles.nopiy-handles.center0(1),handles.nopix-handles.center0(2));
set(handles.trans_beam_x,'Visible','on');set(handles.trans_beam_x_text,'Visible','on');
set(handles.trans_beam_x,'Min',-handles.rmax,'Max',handles.rmax,'Value',0);
set(handles.trans_beam_y,'Visible','on');set(handles.trans_beam_y_text,'Visible','on');
set(handles.trans_beam_y,'Min',-handles.rmax,'Max',handles.rmax,'Value',0);
set(handles.trans_beam_radius,'Visible','on');set(handles.trans_beam_radius_text,'Visible','on');
set(handles.trans_beam_radius,'Min',0,'Max',handles.rmax,'Value',handles.rmax/3);
set(handles.align_trans_beam,'Visible','on');

handles.radius=min(handles.nopix/2,handles.nopiy/2);
axes(handles.detector_layout);
handles.disk_edge=viscircles(handles.center0,handles.radius/2,'Color','b');

% Save variable data so it can be accessed by all functions
guidata(hObject,handles)

function display_images_Callback(hObject, eventdata, handles)
diag_box=waitbar(0,'Forming images. Please wait...');

handles.angle=2*pi/handles.n_seg;

[xgrid, ygrid] = meshgrid(1:size(handles.img,2), 1:size(handles.img,1));
handles.temp_angle=handles.det_angle.Value;
temp=zeros(size(xgrid));

if handles.det_angle.Value>0
    start=1;finish=handles.n_seg-1;
elseif handles.det_angle.Value<0
    start=2;finish=handles.n_seg;
    handles.temp_angle=handles.temp_angle+2*pi/handles.n_seg;
else
    start=1;finish=handles.n_seg;
end

for i=start:finish
    a=atan2(ygrid-handles.center(2),xgrid-handles.center(1));
    a = a .* (a >= 0) + (a + 2 * pi) .* (a < 0);
    
    handles.mask.(strcat('x',num2str(i)))=((xgrid-handles.center(1)).^2 + (ygrid-handles.center(2)).^2) <= handles.adf_outer_angle^2 & ...
        ((xgrid-handles.center(1)).^2 + (ygrid-handles.center(2)).^2) >= handles.adf_inner_angle^2 & ...
        a > handles.temp_angle & ...
        a <= handles.temp_angle+handles.angle;
    
    temp=handles.mask.(strcat('x',num2str(i)))+temp;
    handles.temp_angle=handles.temp_angle+2*pi/handles.n_seg;
end

if handles.det_angle.Value>0
    handles.mask.(strcat('x',num2str(handles.n_seg)))=((xgrid-handles.center(1)).^2 + (ygrid-handles.center(2)).^2) <= handles.adf_outer_angle^2 & ...
        ((xgrid-handles.center(1)).^2 + (ygrid-handles.center(2)).^2) >= handles.adf_inner_angle^2 & ...
        ~temp;
elseif handles.det_angle.Value<0
    handles.mask.(strcat('x',num2str(1)))=((xgrid-handles.center(1)).^2 + (ygrid-handles.center(2)).^2) <= handles.adf_outer_angle^2 & ...
        ((xgrid-handles.center(1)).^2 + (ygrid-handles.center(2)).^2) >= handles.adf_inner_angle^2 & ...
        ~temp;
end

handles.names=fieldnames(handles.mask);

handles.mask_address.x1=find(handles.mask.x1==1);
handles.images.x1=reshape(sum(handles.data.raw(handles.mask.x1==1,:)),[handles.framesx handles.framesy]);
imagesc(imrotate(handles.images.x1,-90),'Parent', handles.seg_a);
set(handles.seg_a,'DataAspectRatio',[1 1 1],'Colormap',gray,'XTick',[],'Ytick',[],'Tag','seg_a');
set(handles.seg_a,'Visible','on');set(handles.seg_a_text,'Visible','on');

handles.mask_address.x2=find(handles.mask.x2==1);
handles.images.x2=reshape(sum(handles.data.raw(handles.mask.x2==1,:)),[handles.framesx handles.framesy]);
imagesc(imrotate(handles.images.x2,-90),'Parent', handles.seg_b);
set(handles.seg_b,'DataAspectRatio',[1 1 1],'Colormap',gray,'XTick',[],'Ytick',[],'Tag','seg_b');
set(handles.seg_b,'Visible','on');set(handles.seg_b_text,'Visible','on');

handles.mask_address.x3=find(handles.mask.x3==1);
handles.images.x3=reshape(sum(handles.data.raw(handles.mask.x3==1,:)),[handles.framesx handles.framesy]);
imagesc(imrotate(handles.images.x3,-90),'Parent', handles.seg_c);
set(handles.seg_c,'DataAspectRatio',[1 1 1],'Colormap',gray,'XTick',[],'Ytick',[],'Tag','seg_c');
set(handles.seg_c,'Visible','on');set(handles.seg_c_text,'Visible','on');

handles.mask_address.x4=find(handles.mask.x4==1);
handles.images.x4=reshape(sum(handles.data.raw(handles.mask.x4==1,:)),[handles.framesx handles.framesy]);
imagesc(imrotate(handles.images.x4,-90),'Parent', handles.seg_d);
set(handles.seg_d,'DataAspectRatio',[1 1 1],'Colormap',gray,'XTick',[],'Ytick',[],'Tag','seg_d');
set(handles.seg_d,'Visible','on');set(handles.seg_d_text,'Visible','on');

handles.images.ac=handles.images.x1-handles.images.x3;
imagesc(interp2(imrotate(handles.images.ac,-90),3),'Parent', handles.seg_ac);
set(handles.seg_ac,'DataAspectRatio',[1 1 1],'Colormap',gray,'XTick',[],'Ytick',[],'Tag','seg_ac');
set(handles.seg_ac,'Visible','on');set(handles.seg_ac_text,'Visible','on');

handles.images.bd=handles.images.x2-handles.images.x4;
imagesc(interp2(imrotate(handles.images.bd,-90),3),'Parent', handles.seg_bd);
set(handles.seg_bd,'DataAspectRatio',[1 1 1],'Colormap',gray,'XTick',[],'Ytick',[],'Tag','seg_bd');
set(handles.seg_bd,'Visible','on');set(handles.seg_bd_text,'Visible','on');

% Make DPC images
handles.dpc_angle=atan2(handles.images.bd,handles.images.ac);
handles.dpc_mag=sqrt(handles.images.ac.^2+handles.images.bd.^2);

imagesc(interp2(imrotate(handles.dpc_angle,-90),3),'Parent', handles.vect_angle);
set(handles.vect_angle,'DataAspectRatio',[1 1 1],'Colormap',jet,'XTick',[],'Ytick',[],'Tag','vect_angle');
set(handles.vect_angle,'Visible','on');set(handles.vect_angle_text,'Visible','on');

imagesc(interp2(imrotate(handles.dpc_mag,-90),3),'Parent', handles.vect_mag);
set(handles.vect_mag,'DataAspectRatio',[1 1 1],'Colormap',gray,'XTick',[],'Ytick',[],'Tag','vect_mag');
set(handles.vect_mag,'Visible','on');set(handles.vect_mag_text,'Visible','on');

delete(diag_box)

if strcmp(get(handles.save_images,'Visible'),'off')
    set(handles.save_images,'Visible','on');
end
guidata(hObject,handles)

function trans_beam_Callback(hObject, eventdata, handles)
if strcmp(get(hObject,'Tag'),'trans_beam_x')
        handles.center=handles.center0+[get(hObject,'Value') get(handles.trans_beam_y,'Value')];
        guidata(hObject, handles);
elseif strcmp(get(hObject,'Tag'),'trans_beam_y')
        handles.center=handles.center0+[get(handles.trans_beam_x,'Value') -get(hObject,'Value')];
        guidata(hObject, handles);
else
    handles.radius=get(hObject,'Value');
    if ~isfield(handles,'center')
        handles.center=handles.center0;
    end
    handles.mrad_per_pix=handles.alpha/handles.radius;
    guidata(hObject, handles);
end

delete(handles.disk_edge);
clear handles.disk_edge
axes(handles.detector_layout);
handles.disk_edge=viscircles(handles.center,handles.radius,'Color','b');

guidata(hObject, handles);

function align_trans_beam_Callback(hObject, eventdata, handles)

if strcmp(get(hObject,'String'),'Finish Alignment')
    set(hObject,'Value',0);
    set(hObject,'String','Align Transmitted Beam');
    
     delete(handles.disk_edge);
     handles.inner_disk=viscircles(handles.center,handles.radius/2,'Color','g');
     handles.outer_disk=viscircles(handles.center,handles.rmax,'Color','r');
     handles.n_seg=4;
     handles.det_angle.Value=pi/handles.n_seg;
     handles.adf_inner_angle=handles.radius/2;
     handles.adf_outer_angle=handles.rmax;
     handles.temp_angle=handles.det_angle.Value;
    
    hold on
    for i=1:handles.n_seg
        handles.seg.(strcat('x',num2str(i)))=plot(cos(handles.temp_angle)*[handles.adf_inner_angle handles.adf_outer_angle]+handles.center(1),sin(handles.temp_angle)*[handles.adf_inner_angle handles.adf_outer_angle]+handles.center(2),':b','LineWidth',4);
        handles.temp_angle=handles.temp_angle+2*pi/handles.n_seg;
    end
    
    set(handles.adf_inner,'Visible','on');set(handles.adf_inner_text,'Visible','on');set(handles.adf_inner_value,'Visible','on');set(handles.adf_inner_unit,'Visible','on');
    set(handles.adf_inner,'Min',0,'Max',handles.rmax,'Value',handles.radius/2);set(handles.adf_inner_value,'String',handles.adf_inner_angle*handles.mrad_per_pix);
    set(handles.adf_outer,'Visible','on');set(handles.adf_outer_text,'Visible','on');set(handles.adf_outer_value,'Visible','on');set(handles.adf_outer_unit,'Visible','on');
    set(handles.adf_outer,'Min',0,'Max',handles.rmax,'Value',handles.rmax);set(handles.adf_outer_value,'String',handles.adf_outer_angle*handles.mrad_per_pix);
    set(handles.det_angle,'Visible','on');set(handles.det_angle_text,'Visible','on');set(handles.det_angle_value,'Visible','on');set(handles.det_angle_unit,'Visible','on');
    set(handles.det_angle,'Min',0,'Max',2*pi/handles.n_seg,'Value',pi/handles.n_seg);set(handles.det_angle_value,'String',handles.det_angle.Value*180/pi);
    set(handles.display_images,'Visible','on');
    
    set(handles.trans_beam_x,'Visible','off');set(handles.trans_beam_x_text,'Visible','off');
    set(handles.trans_beam_y,'Visible','off');set(handles.trans_beam_y_text,'Visible','off');
    set(handles.trans_beam_radius,'Visible','off');set(handles.trans_beam_radius_text,'Visible','off');
    
    if isfield(handles,'center')
        handles.center0=handles.center;
    end
    
elseif strcmp(get(hObject,'String'),'Align Transmitted Beam')
    set(hObject,'Value',1);
    
    set(handles.trans_beam_x,'Visible','on');set(handles.trans_beam_x_text,'Visible','on');
    set(handles.trans_beam_y,'Visible','on');set(handles.trans_beam_y_text,'Visible','on');
    set(handles.trans_beam_radius,'Visible','on');set(handles.trans_beam_radius_text,'Visible','on');    
    
    set(handles.adf_inner,'Visible','off');set(handles.adf_inner_text,'Visible','off');set(handles.adf_inner_value,'Visible','off');set(handles.adf_inner_unit,'Visible','off');
    set(handles.adf_outer,'Visible','off');set(handles.adf_outer_text,'Visible','off');set(handles.adf_outer_value,'Visible','off');set(handles.adf_outer_unit,'Visible','off');
    set(handles.det_angle,'Visible','off');set(handles.det_angle_text,'Visible','off');set(handles.det_angle_value,'Visible','off');set(handles.det_angle_unit,'Visible','off');
    set(handles.display_images,'Visible','off');
    set(handles.seg_a,'Visible','off');set(handles.seg_a_text,'Visible','off');set(get(handles.seg_a,'children'),'visible','off')
    set(handles.seg_b,'Visible','off');set(handles.seg_b_text,'Visible','off');set(get(handles.seg_b,'children'),'visible','off')
    set(handles.seg_c,'Visible','off');set(handles.seg_c_text,'Visible','off');set(get(handles.seg_c,'children'),'visible','off')
    set(handles.seg_d,'Visible','off');set(handles.seg_d_text,'Visible','off');set(get(handles.seg_d,'children'),'visible','off')
    set(handles.seg_ac,'Visible','off');set(handles.seg_ac_text,'Visible','off');set(get(handles.seg_ac,'children'),'visible','off')
    set(handles.seg_bd,'Visible','off');set(handles.seg_bd_text,'Visible','off');set(get(handles.seg_bd,'children'),'visible','off')
    set(handles.vect_mag,'Visible','off');set(handles.vect_mag_text,'Visible','off');set(get(handles.vect_mag,'children'),'visible','off')
    set(handles.vect_angle,'Visible','off');set(handles.vect_angle_text,'Visible','off');set(get(handles.vect_angle,'children'),'visible','off')
    set(handles.save_images,'Visible','off');
    
    set(hObject,'String','Finish Alignment');
    
    delete(handles.inner_disk);
    delete(handles.outer_disk);
    delete(handles.seg.x1);
    delete(handles.seg.x2);
    delete(handles.seg.x3);
    delete(handles.seg.x4);
    
    axes(handles.detector_layout);
    handles.disk_edge=viscircles(handles.center,handles.radius/2,'Color','b');

end
guidata(hObject,handles)

function trans_beam_radius_Callback(hObject, eventdata, handles)

%% Create Functions
function generic_slider_CreateFcn(hObject, eventdata, handles)
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end

function generic_text_CreateFcn(hObject, eventdata, handles)
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
