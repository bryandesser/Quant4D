function varargout = import_4dstem(varargin)
% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @import_4dstem_OpeningFcn, ...
                   'gui_OutputFcn',  @import_4dstem_OutputFcn, ...
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


% --- Executes just before import_4dstem is made visible.
function import_4dstem_OpeningFcn(hObject, eventdata, handles, varargin)
handles.output = hObject;
varargin=varargin{1};
s=dir(varargin{1});
set(handles.actual_filesize,'String',sprintf('%.3f GB',s.bytes/(1e9)));

if strcmp(varargin{1}(end-2:end),'mib')
    set(handles.bitdepth,'String',{'1-bit';'6-bit';'12-bit';'24-bit'});
    set(handles.bitdepth,'Value',3);
    set(handles.nopiy,'String','256');set(handles.nopix,'String','256');
    set(handles.framesx,'String',floor(sqrt(s.bytes/(256*256*2))));set(handles.framesy,'String',floor(sqrt(s.bytes/(256*256*2))));
    handles.bitsize=[1/8;1;2;4];
    filesize=str2double(get(handles.nopiy,'String'))*str2double(get(handles.nopix,'String'))*str2double(get(handles.framesy,'String'))*str2double(get(handles.framesx,'String'))*handles.bitsize(handles.bitdepth.Value);
    set(handles.est_filesize,'String',sprintf('%.3f GB',filesize/(1e9)));
elseif strcmp(varargin{1}(end-2:end),'raw')
    set(handles.bitdepth,'String',{'8-bit';'16-bit';'32-bit';'64-bit'});
    set(handles.bitdepth,'Value',2);
    set(handles.nopiy,'String','512');set(handles.nopix,'String','512');
    set(handles.framesx,'String',floor(sqrt(s.bytes/(512*512*2))));set(handles.framesy,'String',floor(sqrt(s.bytes/(512*512*2))));
    handles.bitsize=[1;2;4;8];
    filesize=str2double(get(handles.nopiy,'String'))*str2double(get(handles.nopix,'String'))*str2double(get(handles.framesy,'String'))*str2double(get(handles.framesx,'String'))*handles.bitsize(handles.bitdepth.Value);
    set(handles.est_filesize,'String',sprintf('%.3f GB',filesize/(1e9)));
else
    return
end

% Update handles structure
guidata(hObject, handles);
uiwait(handles.figure1);

% --- Outputs from this function are returned to the command line.
function varargout = import_4dstem_OutputFcn(hObject, eventdata, handles) 
varargout{1}=str2double(handles.nopiy.String);
varargout{2}=str2double(handles.nopix.String);
varargout{3}=str2double(handles.framesy.String);
varargout{4}=str2double(handles.framesx.String);
varargout{5}=handles.bitdepth.String{handles.bitdepth.Value};
varargout{6}=str2double(handles.alpha.String);
delete(handles.figure1);

function box_Callback(hObject, eventdata, handles)
filesize=str2double(get(handles.nopiy,'String'))*str2double(get(handles.nopix,'String'))*str2double(get(handles.framesy,'String'))*str2double(get(handles.framesx,'String'))*handles.bitsize(handles.bitdepth.Value);
set(handles.est_filesize,'String',sprintf('%.3f GB',filesize/(1e9)));
guidata(hObject, handles);

function alpha_Callback(hObject, eventdata, handles)
guidata(hObject, handles);

function box_CreateFcn(hObject, eventdata, handles)
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

function bitdepth_CreateFcn(hObject, eventdata, handles)
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

function figure1_CloseRequestFcn(hObject, eventdata, handles)    
if strcmp(get(hObject,'Tag'),'import_button')
    uiresume(handles.figure1);
elseif isequal(get(hObject,'waitstatus'),'waiting')
    uiresume(hObject);
else
    delete(hObject);
end
