classdef Quant4D_exported < matlab.apps.AppBase

    % Properties that correspond to app components
    properties (Access = public)
        Quant4D_Fig                     matlab.ui.Figure
        DfrnDetrTabGroup                matlab.ui.container.TabGroup
        PreviewTab                      matlab.ui.container.Tab
        PreviewGrid                     matlab.ui.container.GridLayout
        PreviewFramePanel               matlab.ui.container.Panel
        PreviewButtonGrid               matlab.ui.container.GridLayout
        PreviewFrGrid                   matlab.ui.container.GridLayout
        PvFrYLabel                      matlab.ui.control.Label
        PvFrY                           matlab.ui.control.Spinner
        PvFrXLabel                      matlab.ui.control.Label
        PvFrX                           matlab.ui.control.Spinner
        PreviewButton                   matlab.ui.control.Button
        PvBR                            matlab.ui.control.Button
        PvBC                            matlab.ui.control.Button
        PvBL                            matlab.ui.control.Button
        PvCR                            matlab.ui.control.Button
        PvCC                            matlab.ui.control.Button
        PvCL                            matlab.ui.control.Button
        PvTR                            matlab.ui.control.Button
        PvTC                            matlab.ui.control.Button
        PvTL                            matlab.ui.control.Button
        AlignmentTab                    matlab.ui.container.Tab
        AlignmentGrid                   matlab.ui.container.GridLayout
        TransBeamAlignPanel             matlab.ui.container.Panel
        TransBeamAlignGrid              matlab.ui.container.GridLayout
        TBCrossAlign                    matlab.ui.control.Button
        TBY_NFLabel                     matlab.ui.control.Label
        TBY_NF                          matlab.ui.control.Spinner
        TBX_NFLabel                     matlab.ui.control.Label
        TBX_NF                          matlab.ui.control.Spinner
        TBR_NFLabel                     matlab.ui.control.Label
        TBR_NF                          matlab.ui.control.Spinner
        TBR                             matlab.ui.control.Slider
        TBRLabel                        matlab.ui.control.Label
        TBY                             matlab.ui.control.Slider
        TBYLabel                        matlab.ui.control.Label
        TBXLabel                        matlab.ui.control.Label
        TBX                             matlab.ui.control.Slider
        TBAutoAlign                     matlab.ui.control.Button
        AlignmentHelpIcon               matlab.ui.control.Image
        DfrnCalibPanel                  matlab.ui.container.Panel
        DfrnCalibGrid                   matlab.ui.container.GridLayout
        mradPx                          matlab.ui.control.NumericEditField
        DiffractionScaleLabel           matlab.ui.control.Label
        mradpxLabel                     matlab.ui.control.Label
        mradLabel                       matlab.ui.control.Label
        Alpha                           matlab.ui.control.NumericEditField
        ConvergenceAngleLabel           matlab.ui.control.Label
        AnnularDetectorTab              matlab.ui.container.Tab
        AnnDetrGrid                     matlab.ui.container.GridLayout
        ScanDirPanel                    matlab.ui.container.Panel
        ScanDirGrid                     matlab.ui.container.GridLayout
        autoCurl                        matlab.ui.control.Button
        ScanDirUnlock                   matlab.ui.control.StateButton
        ScanDirYFlip                    matlab.ui.control.StateButton
        ScanDirLabel                    matlab.ui.control.Label
        ScanDir                         matlab.ui.control.Slider
        ScanDir_NF                      matlab.ui.control.Spinner
        ScanDir_NFLabel                 matlab.ui.control.Label
        SegDetrPanel                    matlab.ui.container.Panel
        SegDetrGrid                     matlab.ui.container.GridLayout
        DetRot                          matlab.ui.control.Slider
        DetRotLabel                     matlab.ui.control.Label
        DetRot_NF                       matlab.ui.control.Spinner
        DetRot_NFLabel                  matlab.ui.control.Label
        NRung                           matlab.ui.control.Spinner
        RungsLabel                      matlab.ui.control.Label
        NSeg                            matlab.ui.control.Spinner
        SegmentsLabel                   matlab.ui.control.Label
        AnnRPanel                       matlab.ui.container.Panel
        AnnRGrid                        matlab.ui.container.GridLayout
        AnnRLink                        matlab.ui.control.StateButton
        AnnRoLabel                      matlab.ui.control.Label
        AnnRo                           matlab.ui.control.Slider
        AnnRiLabel                      matlab.ui.control.Label
        AnnRi                           matlab.ui.control.Slider
        AnnRi_NF                        matlab.ui.control.Spinner
        AnnRi_NFLabel                   matlab.ui.control.Label
        AnnRo_NFLabel                   matlab.ui.control.Label
        AnnRo_NF                        matlab.ui.control.Spinner
        VirtualApertureTab              matlab.ui.container.Tab
        VirtualApertureGrid             matlab.ui.container.GridLayout
        VrAperSymmOptPanel              matlab.ui.container.Panel
        VrAperSymmOptGrid               matlab.ui.container.GridLayout
        VrApMirrGrid                    matlab.ui.container.GridLayout
        VrApMirror                      matlab.ui.control.StateButton
        VrApMirrRot                     matlab.ui.control.Slider
        VrApMirrRotLabel                matlab.ui.control.Label
        VrApMirrRot_NFLabel             matlab.ui.control.Label
        VrApMirrRot_NF                  matlab.ui.control.Spinner
        VrApSymmLabel                   matlab.ui.control.Label
        VrApSymm                        matlab.ui.control.DropDown
        VrAperCoordPanel                matlab.ui.container.Panel
        VrAperCoordGrid                 matlab.ui.container.GridLayout
        VrAperRotGrid                   matlab.ui.container.GridLayout
        VrApInvert                      matlab.ui.control.StateButton
        VrApRotCW                       matlab.ui.control.Button
        VrApRotStep                     matlab.ui.control.DropDown
        VrApRotCCW                      matlab.ui.control.Button
        VrApReset                       matlab.ui.control.Button
        VrApY                           matlab.ui.control.Slider
        VrApYLabel                      matlab.ui.control.Label
        VrApY_NF                        matlab.ui.control.Spinner
        VrApY_NFLabel                   matlab.ui.control.Label
        VrApX                           matlab.ui.control.Slider
        VrApXLabel                      matlab.ui.control.Label
        VrApX_NF                        matlab.ui.control.Spinner
        VrApX_NFLabel                   matlab.ui.control.Label
        VrApR                           matlab.ui.control.Slider
        VrApRLabel                      matlab.ui.control.Label
        VrApR_NF                        matlab.ui.control.Spinner
        VrApR_NFLabel                   matlab.ui.control.Label
        CustomDetectorTab               matlab.ui.container.Tab
        CustomDetectorGrid              matlab.ui.container.GridLayout
        CDT                             matlab.ui.control.Table
        CDInterMaskGrid                 matlab.ui.container.GridLayout
        CDDelMask                       matlab.ui.control.Button
        ShowDfrnMaskWdw                 matlab.ui.control.Button
        CDInterMask                     matlab.ui.control.DropDown
        IntermaskLabel                  matlab.ui.control.Label
        CDNewMaskGrid                   matlab.ui.container.GridLayout
        CDNewMath                       matlab.ui.control.Button
        CDNewCircle                     matlab.ui.control.Button
        CDNewBandpass                   matlab.ui.control.Button
        CDNewFromFile                   matlab.ui.control.Button
        CDNewPolygon                    matlab.ui.control.Button
        CDNewWedge                      matlab.ui.control.Button
        CDNewGrid                       matlab.ui.control.Button
        CDDetailsPanel                  matlab.ui.container.Panel
        CDDetailsGrid                   matlab.ui.container.GridLayout
        CDColor                         matlab.ui.control.Button
        CDDTable                        matlab.ui.control.Table
        CDRotGrid                       matlab.ui.container.GridLayout
        CDIntraMask                     matlab.ui.control.DropDown
        CDIntraCombLabel                matlab.ui.control.Label
        CDRotCCW                        matlab.ui.control.Button
        CDRotCW                         matlab.ui.control.Button
        CDRotStep                       matlab.ui.control.DropDown
        CDInvert                        matlab.ui.control.StateButton
        CDMirror                        matlab.ui.control.StateButton
        CDTranspose                     matlab.ui.control.Button
        CDFlipVert                      matlab.ui.control.Button
        CDFlipHorz                      matlab.ui.control.Button
        SettingsPanel                   matlab.ui.container.Panel
        SettingsGrid                    matlab.ui.container.GridLayout
        SettingsTabGroup                matlab.ui.container.TabGroup
        DisplayTab                      matlab.ui.container.Tab
        DisplayGrid                     matlab.ui.container.GridLayout
        ImStatsNotes                    matlab.ui.control.TextArea
        DispHistGrid                    matlab.ui.container.GridLayout
        HistLog                         matlab.ui.control.StateButton
        HistAxes                        matlab.ui.control.UIAxes
        DispContrastsGrid               matlab.ui.container.GridLayout
        ShowMaskWdw                     matlab.ui.control.Button
        DispMaskOpa_NF                  matlab.ui.control.Spinner
        DispMaskOpa                     matlab.ui.control.Slider
        DispGamma_NF                    matlab.ui.control.Spinner
        DispContrast_NF                 matlab.ui.control.Spinner
        DispBrightness_NF               matlab.ui.control.Spinner
        DispBrightnessReset             matlab.ui.control.Button
        DispContrastReset               matlab.ui.control.Button
        DispGammaReset                  matlab.ui.control.Button
        DispGamma                       matlab.ui.control.Slider
        DispContrast                    matlab.ui.control.Slider
        DispBrightness                  matlab.ui.control.Slider
        DisplayDropDownGrid             matlab.ui.container.GridLayout
        ShowImageWdw                    matlab.ui.control.Button
        DispLock                        matlab.ui.control.StateButton
        ImageLabel                      matlab.ui.control.Label
        DispImage                       matlab.ui.control.DropDown
        DispCMapInvert                  matlab.ui.control.StateButton
        ColormapLabel                   matlab.ui.control.Label
        DispCMap                        matlab.ui.control.DropDown
        MiscTab                         matlab.ui.container.Tab
        MiscGrid                        matlab.ui.container.GridLayout
        annularStepGrid                 matlab.ui.container.GridLayout
        annularStep                     matlab.ui.control.NumericEditField
        AnnularIntegrationStepEditFieldLabel  matlab.ui.control.Label
        LiveUpdateImagesGrid            matlab.ui.container.GridLayout
        LiveUpdateImageIcon             matlab.ui.control.Image
        CalculationPolicyDropDownLabel  matlab.ui.control.Label
        CalcPolicy                      matlab.ui.control.DropDown
        ShowImageWindowsPanel           matlab.ui.container.Panel
        ShowImageWindowsGrid            matlab.ui.container.GridLayout
        ShowRealMaskWdw_2               matlab.ui.control.Button
        ShowColorWheelWdw_2             matlab.ui.control.Button
        ShowCoMMagWdw                   matlab.ui.control.Button
        ShowCoMPhWdw                    matlab.ui.control.Button
        ShowCoMPhMagWdw                 matlab.ui.control.Button
        ShowRealWdw                     matlab.ui.control.Button
        ShowDfrnWdw                     matlab.ui.control.Button
        ShowDfrnMaskWdw_2               matlab.ui.control.Button
        ShowiCoMWdw                     matlab.ui.control.Button
        ShowdCoMWdw                     matlab.ui.control.Button
        ShowCoMYWdw                     matlab.ui.control.Button
        ShowCoMXWdw                     matlab.ui.control.Button
        RealSpaceWindowPanel            matlab.ui.container.Panel
        RealSpaceWindowGrid             matlab.ui.container.GridLayout
        WdwSetAllReal                   matlab.ui.control.Button
        RealSpaceAxesGrid               matlab.ui.container.GridLayout
        ShowRealAxes                    matlab.ui.control.StateButton
        RvsXReal                        matlab.ui.control.StateButton
        RvsYReal                        matlab.ui.control.StateButton
        RotRealIcon                     matlab.ui.control.Image
        RotReal                         matlab.ui.control.DropDown
        WdwSetReal                      matlab.ui.control.Button
        WdwHReal                        matlab.ui.control.NumericEditField
        HEditField_2Label               matlab.ui.control.Label
        WEditField_2Label               matlab.ui.control.Label
        WdwWReal                        matlab.ui.control.NumericEditField
        DetectorCoordinatePanel         matlab.ui.container.Panel
        DetectorCoordinateGrid          matlab.ui.container.GridLayout
        DCUnit                          matlab.ui.control.DropDown
        DCPos                           matlab.ui.control.DropDown
        DCSys                           matlab.ui.control.DropDown
        DiffractionImageWindowsPanel    matlab.ui.container.Panel
        DiffractionWindowGrid           matlab.ui.container.GridLayout
        WdwSetAllDfrn                   matlab.ui.control.Button
        DiffractionAxesGrid             matlab.ui.container.GridLayout
        RotDfrnIcon                     matlab.ui.control.Image
        RotDfrn                         matlab.ui.control.DropDown
        RvsYDfrn                        matlab.ui.control.StateButton
        RvsXDfrn                        matlab.ui.control.StateButton
        ShowDfrnAxes                    matlab.ui.control.StateButton
        WdwSetDfrn                      matlab.ui.control.Button
        WdwHDfrn                        matlab.ui.control.NumericEditField
        HEditFieldLabel                 matlab.ui.control.Label
        WdwWDfrn                        matlab.ui.control.NumericEditField
        WEditFieldLabel                 matlab.ui.control.Label
        InfoTab                         matlab.ui.container.Tab
        InfoGrid                        matlab.ui.container.GridLayout
        DatasetOptionPanel              matlab.ui.container.Panel
        DatasetOptionGrid               matlab.ui.container.GridLayout
        SwapByteOrder                   matlab.ui.control.Button
        SwapRealXY                      matlab.ui.control.Button
        SwapDfrnXY                      matlab.ui.control.Button
        DatasetInfoTextAreaLabel        matlab.ui.control.Label
        DataInfo                        matlab.ui.control.TextArea
        MathTab                         matlab.ui.container.Tab
        MathGrid                        matlab.ui.container.GridLayout
        MathExampleGrid                 matlab.ui.container.GridLayout
        MathHelpIcon                    matlab.ui.control.Image
        MathExampleLabel                matlab.ui.control.Label
        MathButtonGrid                  matlab.ui.container.GridLayout
        MathEval                        matlab.ui.control.Button
        FormulaLabel                    matlab.ui.control.Label
        MathFormula                     matlab.ui.control.TextArea
        ImportPanel                     matlab.ui.container.Panel
        ImportGrid                      matlab.ui.container.GridLayout
        ImportButtonGrid                matlab.ui.container.GridLayout
        ImpKeepP                        matlab.ui.control.CheckBox
        ImportCancelButton              matlab.ui.control.Button
        ImportDataButton                matlab.ui.control.Button
        ImportOptionsPanel              matlab.ui.container.Panel
        ImportOptionsGrid               matlab.ui.container.GridLayout
        ImpMemGrid                      matlab.ui.container.GridLayout
        ImpMemType                      matlab.ui.control.DropDown
        ImpGPU                          matlab.ui.control.DropDown
        ImpFrPart                       matlab.ui.control.CheckBox
        ImpPxPart                       matlab.ui.control.CheckBox
        ImportFrRangeGrid               matlab.ui.container.GridLayout
        SamplingIntervalLabel_2         matlab.ui.control.Label
        IFrD                            matlab.ui.control.Spinner
        IFrY1                           matlab.ui.control.Spinner
        ysub1Label_6                    matlab.ui.control.Label
        INFrX                           matlab.ui.control.Spinner
        INFrXl                          matlab.ui.control.Label
        IFrX1                           matlab.ui.control.Spinner
        xsub1Label_6                    matlab.ui.control.Label
        INFrY                           matlab.ui.control.Spinner
        INFrYl                          matlab.ui.control.Label
        ImportPxRangeGrid               matlab.ui.container.GridLayout
        BinningDistanceLabel            matlab.ui.control.Label
        IPxD                            matlab.ui.control.Spinner
        INPxY                           matlab.ui.control.Spinner
        YLabel_3                        matlab.ui.control.Label
        IPxY1                           matlab.ui.control.Spinner
        ysub1Label_5                    matlab.ui.control.Label
        INPxX                           matlab.ui.control.Spinner
        XLabel_3                        matlab.ui.control.Label
        IPxX1                           matlab.ui.control.Spinner
        xsub1Label_5                    matlab.ui.control.Label
        ImportSummaryLabel              matlab.ui.control.Label
        ImpNotes                        matlab.ui.control.TextArea
        ImpDatasetInfoPanel             matlab.ui.container.Panel
        ImpDatasetInfoGrid              matlab.ui.container.GridLayout
        ImpFileMetaNotes                matlab.ui.control.TextArea
        DatasetInfofromMetadataLabel    matlab.ui.control.Label
        ImpFileSizeGrid                 matlab.ui.container.GridLayout
        ImpActualFilesize               matlab.ui.control.Label
        ImpEstFilesize                  matlab.ui.control.Label
        ImpActualFilesizeLabel          matlab.ui.control.Label
        ImpEstFilesizeLabel             matlab.ui.control.Label
        ImpDimensionGrid                matlab.ui.container.GridLayout
        DNFrY                           matlab.ui.control.NumericEditField
        YLabel                          matlab.ui.control.Label
        DNFrX                           matlab.ui.control.NumericEditField
        XLabel                          matlab.ui.control.Label
        ImpNumFramesLabel               matlab.ui.control.Label
        ImpDfrnResolutionLabel          matlab.ui.control.Label
        YLabel_2                        matlab.ui.control.Label
        DNPxY                           matlab.ui.control.NumericEditField
        XLabel_2                        matlab.ui.control.Label
        DNPxX                           matlab.ui.control.NumericEditField
        ImpDatasetStructGrid            matlab.ui.container.GridLayout
        SubdatasetDropDownLabel         matlab.ui.control.Label
        ImpSubImg                       matlab.ui.control.DropDown
        ByteOrderDropDownLabel          matlab.ui.control.Label
        ImpByteOrder                    matlab.ui.control.DropDown
        DataTypeLabel                   matlab.ui.control.Label
        ImpDataType                     matlab.ui.control.DropDown
        DataOffsetLabel                 matlab.ui.control.Label
        DataOffset                      matlab.ui.control.NumericEditField
        FrameFooterLabel                matlab.ui.control.Label
        FrFoot                          matlab.ui.control.NumericEditField
        FrameHeaderLabel                matlab.ui.control.Label
        FrHead                          matlab.ui.control.NumericEditField
        ImpFileTypeButtonGroup          matlab.ui.container.ButtonGroup
        HDF5Button                      matlab.ui.control.ToggleButton
        DM34Button                      matlab.ui.control.ToggleButton
        MRCButton                       matlab.ui.control.ToggleButton
        CustomButton                    matlab.ui.control.ToggleButton
        MedipixButton                   matlab.ui.control.ToggleButton
        EMPADButton                     matlab.ui.control.ToggleButton
        ImpFileGrid                     matlab.ui.container.GridLayout
        ImpFilePath                     matlab.ui.control.EditField
        ImpFileSelect                   matlab.ui.control.Button
        Quant4D_FigGrid                 matlab.ui.container.GridLayout
        DfrnDetrPanel                   matlab.ui.container.Panel
        RealSpacePadGrid                matlab.ui.container.GridLayout
        RealSpacePanel                  matlab.ui.container.Panel
        RealSpaceGrid                   matlab.ui.container.GridLayout
        RealSpacePosGrid                matlab.ui.container.GridLayout
        FrameY                          matlab.ui.control.Spinner
        RealYLabel                      matlab.ui.control.Label
        FrameX                          matlab.ui.control.Spinner
        RealXLabel                      matlab.ui.control.Label
        FramePosLabel                   matlab.ui.control.Label
        DispVecField                    matlab.ui.control.DropDown
        DispVecFieldLabel               matlab.ui.control.Label
        DispVecColor                    matlab.ui.control.Button
        ShowColorWheelWdw               matlab.ui.control.Button
        RealROIInvert                   matlab.ui.control.StateButton
        ShowRealMaskWdw                 matlab.ui.control.Button
        ROIShapeLabel                   matlab.ui.control.Label
        RealROIShape                    matlab.ui.control.DropDown
        DetectorModeGrid                matlab.ui.container.GridLayout
        DiffractionLabel                matlab.ui.control.Label
        DetrMode                        matlab.ui.control.DropDown
        ShortcutButtonGrid              matlab.ui.container.GridLayout
        ShowSettingsWdw                 matlab.ui.control.Button
        ShowImportWdw                   matlab.ui.control.Button
        ShowSaveWdw                     matlab.ui.control.Button
        UpdateImages                    matlab.ui.control.Button
        AutoSaveImg                     matlab.ui.control.Button
        SavePanel                       matlab.ui.container.Panel
        SaveGrid                        matlab.ui.container.GridLayout
        SaveExportButtonGrid            matlab.ui.container.GridLayout
        SaveExport                      matlab.ui.control.Button
        SaveCloseButton                 matlab.ui.control.Button
        SaveTabGroup                    matlab.ui.container.TabGroup
        SaveImgTab                      matlab.ui.container.Tab
        SaveImgGrid                     matlab.ui.container.GridLayout
        SaveImgFormatGrid               matlab.ui.container.GridLayout
        SaveImgPNGGrid                  matlab.ui.container.GridLayout
        SaveImgPNG                      matlab.ui.control.CheckBox
        SaveImgPNGAnnot                 matlab.ui.control.CheckBox
        SaveImgAnnotDPILabel            matlab.ui.control.Label
        SaveImgAnnotDPI                 matlab.ui.control.NumericEditField
        SaveImgTIF                      matlab.ui.control.CheckBox
        SaveImgListGrid                 matlab.ui.container.GridLayout
        SaveImgSelectAll                matlab.ui.control.CheckBox
        ImagestoSaveMultiselectwithCtrlShiftLabel  matlab.ui.control.Label
        SaveImgList                     matlab.ui.control.ListBox
        SaveImgDirGrid                  matlab.ui.container.GridLayout
        SaveImgPrefix                   matlab.ui.control.EditField
        FilenamePrefixLabel             matlab.ui.control.Label
        SaveImgAngleGrid                matlab.ui.container.GridLayout
        PrefixLabel                     matlab.ui.control.Label
        SavePrfxRo                      matlab.ui.control.CheckBox
        SavePrfxRi                      matlab.ui.control.CheckBox
        ExportTab                       matlab.ui.container.Tab
        ExportGrid                      matlab.ui.container.GridLayout
        ExportPxRangeGrid               matlab.ui.container.GridLayout
        BinningDistanceLabel_2          matlab.ui.control.Label
        EPxD                            matlab.ui.control.Spinner
        ENPxYl                          matlab.ui.control.Label
        ENPxY                           matlab.ui.control.Spinner
        ysub1Label_3                    matlab.ui.control.Label
        EPxY1                           matlab.ui.control.Spinner
        ENPxXl                          matlab.ui.control.Label
        ENPxX                           matlab.ui.control.Spinner
        xsub1Label_3                    matlab.ui.control.Label
        EPxX1                           matlab.ui.control.Spinner
        ExportFrRangeGrid               matlab.ui.container.GridLayout
        SamplingIntervalLabel           matlab.ui.control.Label
        EFrD                            matlab.ui.control.Spinner
        ENFrY                           matlab.ui.control.Spinner
        ENFrYl                          matlab.ui.control.Label
        EFrY1                           matlab.ui.control.Spinner
        ysub1Label_4                    matlab.ui.control.Label
        ENFrX                           matlab.ui.control.Spinner
        ENFrXl                          matlab.ui.control.Label
        EFrX1                           matlab.ui.control.Spinner
        xsub1Label_4                    matlab.ui.control.Label
        ExpPxPart                       matlab.ui.control.CheckBox
        ExpFrPart                       matlab.ui.control.CheckBox
        ExpByteOrder                    matlab.ui.control.DropDown
        ExpFormat                       matlab.ui.control.DropDown
        SummaryLabel                    matlab.ui.control.Label
        ExpNotes                        matlab.ui.control.TextArea
        ExportFileGrid                  matlab.ui.container.GridLayout
        FilenameLabel                   matlab.ui.control.Label
        ExpFilename                     matlab.ui.control.EditField
        ExpDimSuff                      matlab.ui.control.CheckBox
        SaveDirGrid                     matlab.ui.container.GridLayout
        SaveDir                         matlab.ui.control.EditField
        SaveDirButton                   matlab.ui.control.Button
        DebugContextMenu                matlab.ui.container.ContextMenu
        Test1Menu                       matlab.ui.container.Menu
        Test2Menu                       matlab.ui.container.Menu
        SaveVecMenu                     matlab.ui.container.Menu
        ReimportMenu                    matlab.ui.container.Menu
        ResetQuant4DMenu                matlab.ui.container.Menu
        EnableallUIsMenu                matlab.ui.container.Menu
        CDDelContext                    matlab.ui.container.ContextMenu
        CDDelResetMenu                  matlab.ui.container.Menu
    end

  % Refresh icon: http://simpleicon.com/wp-content/uploads/refresh.png
  % Brightness icon: https://www.onlinewebfonts.com/icon/156779

  properties (Access = public)
    Debug; % Debug mode: `0` to disable; Not `0` enables timers/tracers
    Data % For imported dataset, may be moved to GPU
    Memfile % Virtual mapping of the imported dataset
    C % Constants for system info that set at app startup
    T % Temporary global variables, e.g. for progress bar and import etc., should never be cleared
    D % Parameters of the current imported dataset; should be constants (except for data type conversion)
    P % Common parameters, should be cleared when a dataset is unloaded
    Prev % Previous values, should be cleared when a dataset is unloaded
    Fig; % Other figure windows
    Axes; % Image axes
    Image; % Arrays of raw data for the images/masks to be plotted/saved
    ImgD; % `Image` Objects with modified contrast for display, e.g. by `app.ImgD.(id) = imagesc()`
    A; % Image annotations on `axes` `uiaxes`, excluding annotations on `figure` `uifigure`
    Mask; % For masking `app.Data`
    G; % Different groups of figures/axes/images; assigned just once at startup in `createOtherWindows()`

    B0 = [0 0]; % Central beam absolute pixel coordinates
    RB0 = [0 0]; % Relative position of `app.B0`: [0 0] (when "Absolute" position) or `app.B0` (when "Relative")
    DfPxR = 1; % Diffraction pixel scale: 1 (when in pixel) or mrad/px (when in mrad)
    RsPxR = 1; % Real-space pixel scale: 1 (when in pixel) or nm/px (when in nm). Not implemented yet
    ByteSize = struct('uint8',1, 'int8',1, 'uint16',2, 'int16',2, 'single',4, 'int32',4, 'uint32',4, ...
      'double',8, 'int64',8, 'uint64',8);
    path
  end

  methods (Access = public)
    % Function to debug and time functions
    function debugToc(app, event, notes, t)
      if app.Debug
        srcn = "";  en = "";
        if ~isempty(event)
          % Find name of the source `srcn` by comparing the source with fieldnames of `app`
          if (isfield(event, 'Source') || isprop(event, 'Source')) && ~isempty(event.Source)
            fdn = fieldnames(app);
            for i = 1:length(fdn)
              if ~isa(app.(fdn{i}), 'gpuArray') && isequal(app.(fdn{i}), event.Source), srcn = fdn{i}; break; end
            end
          end
          % EventName
          if (isfield(event, "EventName") || isprop(event, "EventName")) && ~isempty(event.EventName)
            en = event.EventName;
          end
        end

        st = dbstack;  % `st(2).name`: caller of the function
        fprintf('%s, %s, %s, %s: %.3f s\n', st(2).name, srcn, en, notes, toc(t));
      end
    end

    % Function to flash the background of UIs, which have `BackgroundColor`
    % This process will pause the whole program during flashing
    function flashBackground(~, target)
      % Input `target` can be arrays of multiple UIs; they will be flashing together
      c0 = get(target,'BackgroundColor'); % Get original colors
      if ~iscell(c0), c0 = {c0}; end
      for i = 1:2
        pause(.2);
        set(target,'BackgroundColor','g');
        pause(.2);
        set(target,{'BackgroundColor'},c0)
      end
    end

    % Functoin to get all available GPUs
    function getGPU(app)
      app.ImpGPU.Items = {''};  app.ImpGPU.ItemsData = 0;  app.C.nGPU = 0;  app.C.nGPU = -1;
      % Check if parallel computing toolbox is installed for GPU acceleration
      if any(strcmpi("Parallel Computing Toolbox", {ver().Name}))
        try app.C.nGPU = gpuDeviceCount(); catch; end
      end
      % Find GPU devices and turn on/off GPU support; `app.ImgGPU.Value` of `0` is always "GPU off"
      switch app.C.nGPU
        case -1
          app.ImpGPU.Items = {'Parallel Computing Toolbox missing. GPU acceleration unavailable'};
          app.ImpGPU.ItemsData = 0;  app.ImpGPU.Value = 0;
        case 0 % no GPU devices
          app.ImpGPU.Items = {'No GPU found.'};
          app.ImpGPU.ItemsData = 0;  app.ImpGPU.Value = 0;
        otherwise % 1 or more devices found
          maxmem = 0;
          for i = 1:app.C.nGPU
            try
              tmp = parallel.gpu.GPUDevice.getDevice(i);
              app.C.GPU(i).mem = tmp.TotalMemory;
              app.C.GPU(i).name = tmp.Name;
              app.ImpGPU.Items{i} = sprintf('%d. %s %.1f GiB', i, app.C.GPU(i).name, app.C.GPU(i).mem/1024^3);
              app.ImpGPU.ItemsData(i) = i;
              % Select GPU with max memory
              if app.C.GPU(i).mem > maxmem
                maxmem = app.C.GPU(i).mem;  app.ImpGPU.Value = i;
              end
            catch
            end
          end
          app.ImpGPU.Items{end+1} = 'GPU off';
          app.ImpGPU.ItemsData(end+1) = 0;
      end
    end

    % Function to Check usable system memory and make sure the file will fit
    function getMem(app)
      if ispc
        [~,tmp] = memory;
        app.C.MemTot = tmp.PhysicalMemory.Total;
        app.C.MemFree = tmp.PhysicalMemory.Available;
      elseif ismac
        [~,app.C.MemTot] = system('sysctl -n hw.memsize');
        app.C.MemTot = str2double(app.C.MemTot);
        [~,app.C.MemPage] = system("vm_stat | grep 'page size' | awk '{print $8}'");
        app.C.MemPage = str2double(app.C.MemPage);
        [~,app.C.MemWired] = system("vm_stat | grep 'wired' | awk '{print $4}'");
        app.C.MemWired = str2double(app.C.MemWired)*app.C.MemPage;
        app.C.MemFree = app.C.MemTot - app.C.MemWired;
      elseif isunix
        [~,app.C.MemTot] = system("cat /proc/meminfo | grep MemTotal: | awk '{print $2}'");
        app.C.MemTot = str2double(app.C.MemTot)*1024;% memory output is in kB
        [~,app.C.MemFree] = system("cat /proc/meminfo | grep MemAvailable: | awk '{print $2}'");
        app.C.MemFree = str2double(app.C.MemFree)*1024;% memory output is in kB
      end
    end
    
    
    % UI components
    %   app.IPxD, app.IFrD: import binning/sampling distances
    %   app.EPxD, app.EFrD: export binning/sampling distances
    %   app.DNPxX, app.DNPxY, app.DNFrX, app.DNFrY: dataset dimensions in file on disk
    %   app.INPxX, app.INPxY, app.INFrX, app.INFrY: import dimensions (after binning/sampling/cropping)
    %   app.ENPxX, app.ENPxY, app.ENFrX, app.ENFrY: export dimensions (after binning/sampling/cropping)
    %   app.IPxX1, app.IPxY1, app.IFrX1, app.IFrY1: import start positions (cropping)
    %   app.EPxX1, app.EPxY1, app.EFrX1, app.EFrY1: export start positions (cropping)
    % Common local variables in data import/export:
    %   pd, fd: binning/sampling distances
    %   dnpx, dnpy, dnfx, dnfy: when importing, dataset dimensions in file on disk
    %                           when exporting, dataset dimensions in memory (import dimensions after binning/sampling/cropping)
    %   npx, npy, nfx, nfy: import/export dimensions (after binning/sampling/cropping)
    %   px1, py1, fx1, fy1: import/export start positions (cropping)
    %   px2, py2, fx2, fy2: import/export end positions (cropping), to be calculated from other variables
    % app.D, dataset parameters
    %   app.D.DNPxX, app.D.DNPxY, app.D.DNFrX, app.D.DNFrY: dataset dimensions in file on disk
    %   app.D.NPxX, app.D.NPxY, app.D.NFrX, app.D.NFrY: import dimensions (after binning/sampling/cropping)
    %   app.D.PxX1, app.D.PxY1, app.D.FrX1, app.D.FrY1: import start positions (cropping)
    % app.D, dataset convenient constants
    %   app.D.NPx = [NPxX NPxY],  app.D.NPxS = NPxX*NPxY
    %   app.D.NFr = [NFrX NFrY],  app.D.NFrS = NFrX*NFrY

    % Function to calculate importing/exporting ranges
    function [notes,bd,p1,np,p2] = rangeImportExport(app, evt)
      src = evt.Source;
      % `uispinner` upper/lower limits must be different, so now set lower limit `0` but force minimum to `1`
      if isfield(evt,'Value') || isprop(evt,'Value'), val = max(evt.Value, 1); end
      if isprop(evt,'CurrentPosition'), pos = round(evt.CurrentPosition); end  % Round positions from ROIs
      
      % `sp`/`U`: space/unit, "Dfrn"/"Px" for diffraction/pixel OR "Real"/"Fr" for real-space/frame
      if contains(src.Tag,"Dfrn"), sp = "Dfrn"; U = "Px";  
      else, sp = "Real"; U = "Fr"; 
      end
      % `O`: "I" or "E" for Import/Export
      if contains(src.Tag,"Import")
        O = "I";  dnp = [app.("DN"+U+"X").Value app.("DN"+U+"Y").Value];  % Raw dataset dimensions, e.g. app.DNPxX.Value
      else  % Export
        O = "E";  dnp = app.D.("N"+U); % Loaded dataset dimensions
      end
      
      % Get values from UI
      bd = app.(O+U+"D").Value;  % Binning/Sampling (app.IPxD, app.EPxD, app.IFrD or app.EFrD)
      switch src.Tag
        case "Export Dfrn ROI" % From Export Diffraction ROIs
          p1 = pos(1:2);  np = max(floor((pos(3:4)+1)/bd), 1);
        case "Export Real ROI" % From Export Real-space ROIs
          p1 = pos(1:2);  np = floor(pos(3:4)/bd)+1;
        otherwise % From other sources
          p1 = [app.(O+U+"X1").Value app.(O+U+"Y1").Value];  % app.IPxX1, app.EFrX1 etc, Point-1 X & Y UIs
          np = [app.(O+"N"+U+"X").Value app.(O+"N"+U+"Y").Value];  % app.INPxX, app.ENFrX etc, N-Points X & Y UIs
      end
      % Replace value with current event value
      switch src
        case app.(O+U+"D"), bd = val; % Binning/Sampling UI
        case app.(O+U+"X1"), p1(1) = val; % Point-1 X UI
        case app.(O+U+"Y1"), p1(2) = val; % Point-1 Y UI
        case app.(O+"N"+U+"X"), np(1) = val; % N-Points X UI
        case app.(O+"N"+U+"Y"), np(2) = val; % N-Points Y UI
        case {app.("DN"+U+"X") app.("DN"+U+"Y") app.("Imp"+U+"Part") app.("Exp"+U+"Part")}
          % Reset range options if dataset raw dimension changes OR partial selection enables/disables
          app.(O+U+"D").Limits(2) = min(dnp);  % Update binning/sampling UI limits
          if O == "I" && U == "Fr" % Update preview frame limits
            set([app.PvFrX app.PvFrY],{'Limits'},{[0 dnp(1)];[0 dnp(2)]},{'Value'},{dnp(1);dnp(2)});
          end
          bd = 1;  p1 = [1 1];  np = dnp;
      end
      % In general, N-Points are determined by Point-1 and Binning/Sampling, unless N-Points are the source
      s = [app.(O+"N"+U+"X") app.(O+"N"+U+"Y")] ~= src;  % Whether N-Points X or Y are not the source
      if U == "Px"
        np(s) = max(1, min(np(s), floor((dnp(s)-p1(s)+1)/bd)));  % Determine N-Points X/Y if not source
        p1 = min(p1, dnp-np*bd+1);  p2 = p1+np*bd-1; % Endpoints of Pixel ranges
        l1 = dnp-bd+1;  ln = floor(dnp/bd);  % Upper limits of Pixel Point-1 X & Y and N-Points X & Y
        pos = [p1, np*bd-1]; % Positions for Export ROI
        txt = "Diffraction Range (in pixels [px])";  u = " px";  txtb = "binning to ";
      else % "Fr"
        % Frame sampling has slightly different logics to pixel binning
        np(s) = min(np(s), floor((dnp(s)-p1(s))/bd)+1);
        p1 = min(p1, dnp-(np-1)*bd);  p2 = p1+(np-1)*bd; % Endpoints of Frame ranges
        l1 = dnp;  ln = floor((dnp-1)/bd)+1;  % Upper limits of Frame Point-1 X & Y and N-Points X & Y
        pos = [p1 (np-1)*bd]; % Positions for Export ROI
        txt = "Real-space Range (in frames [fr])";  u = " fr";  txtb = "sampling ";
      end
      % Set Point-1 X & Y, N-Points X & Y and Binning/Sampling UIs
      set([app.(O+U+"X1");app.(O+U+"Y1");app.(O+"N"+U+"X");app.(O+"N"+U+"Y");app.(O+U+"D")], ...
        {'Limits'},num2cell([l1 ln min(dnp)]'.*[0 1],2), {'Value'},num2cell([p1 np bd]'))

      % Try to update Export ROIs
      if O == "E"
        set(findobj(app.G.(sp+"Ax"),'Tag',"Export "+sp+" ROI"), 'Position', pos)
      end
      % Range notes
      tp = np+u;  if bd > 1, tp = txtb+tp+" from "+(p2-p1+1)+u; end % If any binning/sampling
      % If not from 1st to last
      s = p1 > 1 | p2 < dnp;  tp(s) = np(s)+u+", "+(p1(s)-1)+"/"+(dnp(s)-p2(s))+u+" offset from start/end";
      notes = sprintf("%s:\n  X = %s–%s (%s)\n  Y = %s–%s (%s)\n",txt,[""+p1;""+p2;tp]);
    end


    % Function for progress bar of data import/export, with a `timer()` to update its progress per second
    function [wb, tmr] = progImportExport(app, proc, tot_fr, frsize)
      % `proc` will be 'Import'/'Export', and used for texts like "Import/Export" + "ing/ed"
      wb = progDLG(app, sprintf("\n%sing ...\n",proc), "Data "+proc, true);
      set(wb.Children, 'Units', 'Normalized')
      % Total time and global variable for processed frames of [this second, last second]
      totT = tic;  app.T.frameJ = [0 0];
      % `timer()` to run the sub function per second
      tmr = timer('TimerFcn',@(~,~)updateDLG(app, wb),'ExecutionMode',"fixedDelay",'Name',proc);
      tmr.start(); % Start the timer now
      wb.DeleteFcn = {@(~,~,t) deletePort(app,t), tmr};  % Kill the timer when progress windows closes

      % Update progress per second
      function updateDLG(app, dlg)
        % Current frame, previous frame and remaining time
        j = app.T.frameJ(1);  j0 = app.T.frameJ(2);  r = (tot_fr-j)/(j - j0);  if j == j0, r = 0; end
        waitbar(j/tot_fr, dlg, sprintf("%sed frames: %d/%d\nSpeed: %.2f MiB/s\nElapsed: %s \t|\t Remaining: %s", ...
          proc, j, tot_fr, (j - j0) * frsize/1024^2, datestr(seconds(floor(toc(totT))),'MM:SS'), ...
          datestr(floor(seconds(r)),'MM:SS')))
        app.T.frameJ(2) = j;
      end
      
      % Function to kill the timer and keep windows disabled when progress windows is closed
      function deletePort(app,t)
        stop(t);  delete(t);  app.enableWindows(false)
      end
    end
    
    
    % Function to import mask for given (diffraction/real) space
    function im = importMask(app, sp)
      if sp == "Real"
        spn = "Real-space";  dsize = app.D.NFr; 
      else % "Dfrn"
        spn = "Diffraction";  dsize = app.D.NPx; 
      end
    
      im = [];  msg = "";
      [file,fpath] = uigetfile({'*.tif;*.tiff;*.png;*.jpg;*.jpeg;*.bmp;*.gif', ...
        'Supported Types (*.tif;*.tiff;*.png;*.jpg;*.jpeg;*.bmp;*.gif)';'*.*','All Files (*.*)'}, ...
        sprintf("Select a mask image with shape [%d,%d]",dsize),"MultiSelect","off");
      try [~,~,ext] = fileparts(file);catch, ext = ''; end
      switch lower(ext) % force lowercase just in case
        case {'.tif';'.tiff';'.png';'.jpg';'.jpeg';'.bmp';'.gif'}
          im0 = permute(imread([fpath,file]), [2 1 3]); % `imread()` transposes images implicitly
          % Check size/orientation
          isize = size(im0, [1 2]);
          if ~isequal(isize, dsize) % If dimension mismatch
            if isequal(isize, flip(dsize)) % If dimension transposed
              im0 = permute(im0, [2 1 3]);
              msg = msg + sprintf("Image size [%d,%d] transposed to fit data's "+spn+" size [%d,%d].\n", ...
                isize, dsize);
            else
              notifDLG(app, 'warn', sprintf("Image size [%d,%d] does not fit data's "+spn+" size [%d,%d]!", ...
                isize, dsize),'Dimension Mismatch'); return
            end
          end
          im = double(im0); % Convert to double
        case "" % Canceled, etc.
          return 
        otherwise
          notifDLG(app, 'warn', "File type '*"+ext+"' currently unsupported!", 'Import Failed'); return
      end
      if any(isnan(im) | isinf(im), 'all')
        im(isnan(im) | isinf(im)) = 0;  msg = msg+"NaN/Inf found in image, and set to 0.\n";
      end
      % Convert RGB to grayscale
      if size(im,3) > 1
        im = rgb2gray(im);  msg = msg+"Converted from RGB to grayscale.\n";
      end
      % Try to scale the maximum to 1
      imax = max(im,[],'all'); 
      if imax ~= 0 && imax ~= 1
        im = im/imax; 
        msg = msg+"The maximum was "+imax+"; now scaled to 1, by `IMG = IMG/"+imax+"`.\n";
      end
      % Notification
      if msg ~= "", msg = "Please note:\n"+msg+"\n"; end
      notifDLG(app, 'help', sprintf(msg+"Please check the "+spn+" Mask image."),'Mask Imported');
      figure(app.Fig.(sp+"Mask"))
    end


    function plotAllPatterns(app, evt)
      dbT = tic;
      % Update images if visible OR not in changing event; include CoMs if in the modes
      for id = app.G.ImgID(contains(app.G.ImgTyp, ["Primary";"Mask"]) ...
          | (ismember(app.DetrMode.Value, ["CoMMod" "DPCMod"]) ...
              & app.G.ImgTyp == "CoM" & app.G.ImgID ~= "ColorWheel"))
        if isStaticEvt(evt) || app.Fig.(id).Visible
          plotImage(app, evt, id)
        end
      end

      debugToc(app, evt, "", dbT)
    end


    % Generic function for plotting an image on a given axis with brightness/contrast/gamma values
    function plotImage(app, evt, id)
      % Special case for plotting the color wheel
      if id == "ColorWheel", plotColorWheel(); end
      ax = app.Axes.(id);  u = ax.UserData;
      delete(findobj(ax,'Tag',"Image "+u.space+" "+u.type));  % clear old `image` on `ax`
      % Abort if image not yet ready
      if ~isfield(app.Image, id) || isempty(app.Image.(id))
        if isequal(id, app.DispImage.Value), app.ImStatsNotes.Value = ax.UserData.name; end
        return;
      end
      im = app.Image.(id)';  % Raw array is column-major; transposed to row-major `im`
      % Put usable values in `ims` for statistics
      ims = im(~(isnan(im) | isinf(im)));
      if isempty(ims), ims = NaN(); end  % Make `ims` NaN if no usable values
      [mini,maxi] = bounds(ims,'all');  rangei = maxi-mini; % Find maximum/minimum/range
      % Brightness between -0.5 and 0.5; Contrast between -Inf and 0.5
      brt = (u.brightness-50)/100;  crs = log2(max(realmin(), u.contrast/50))/2; % Avoid log2(0)
      % Display limits from brightness/contrast; have the same magnitude to the raw image `im` 
      imlo = mini-(brt-crs)*rangei;  imhi = maxi-(brt+crs)*rangei; 
      % Normalize image, and apply display thresholds; `imj` is always between 0 and 1
      if imhi == imlo && (imhi <= 1 || imhi >= 0)
        % If display limits are both 1 or 0, then no rescale (e.g. `im` is all 1 or 0)
        imj = im;
      elseif imhi > imlo || (imhi == imlo && (imhi > 1 || imhi < 0))
        % Normal case for upper limit > lower limit, just apply the limits than rescale
        imj = rescale(im,"InputMin",imlo,"InputMax",imhi);
      else
        % Display limits are too close or identical, then make `imj` a binary image
        % If limits are NaN, then make them 0.5
        immi = (imhi+imlo)/2;  immi(isnan(immi)) = .5;  imhi = immi; imlo = immi;  
        imj = double(im > immi);
      end
      % Plot the row-major array as row-major `image`
      imgd = imagesc(ax, imj.^u.gamma,'Tag',"Image "+u.space+" "+u.type);  % Apply gamma
      % Plot the background, which zooms with the image, for images that rely on `AlphaData` shading
      bg = fill(ax, [.5 ax.XLim(2) ax.XLim(2) .5], [.5 .5 ax.YLim(2) ax.YLim(2)], 'k', 'Tag',"Image "+u.space+" "+u.type);
      
      % Plot mask opacity on non-mask/non-preview image
      if ~ismember(u.type, ["Mask" "Preview"])
        mask = app.Image.(u.space+"Mask")';
        imgd.AlphaData = (1-u.maskOpa/100)*(1-logical(mask))+logical(mask);
      end
      % Shade CoM/DPC Phase with Magnitude
      if id == "CoMPhMag", imgd.AlphaData = imgd.AlphaData.*app.Image.CoMMagNorm'; end
      ax.Children = [setdiff(ax.Children,[imgd; bg],'stable'); imgd; bg];  % Move the `image` to the bottom level
      app.ImgD.(id) = imgd;  app.ImgD.(id+"Bg") = bg;  % Assign the `imgd` `bg` to global handles
      plotVectorField(); % Plot vector field, if selected
      % Only update statistics if not in changing Event AND it is the "selected" image
      if isequal(id, app.DispImage.Value) && isStaticEvt(evt)
        updateDispImgStats();
      end


      %%% Sub functions
      % Function to update image's statistics
      function updateDispImgStats()
        dbT = tic;  histAx = app.HistAxes;
        % Update histogram; skip if image unchanged
        if isDiffToPrev(app,'ims',ims)
          if numel(im) ~= numel(ims), nanwarn = "Contains NaN/Inf"; else, nanwarn = ""; end
          app.ImStatsNotes.Value = ...
            sprintf('min:% -14.7g std:% -14.7g\nmax:% -14.7g sum:% -14.7g\navg:% -14.7g %s', ...
            mini, std(ims,0,'all'), maxi, sum(ims,'all','omitnan'), mean(ims,'all'), nanwarn);

          delete(findobj(histAx,'Tag','HistBars'))
          % Generate an intensity histogram for the selected image
          h = histogram(histAx,ims,128,"FaceColor",'r','Tag','HistBars');
          % Set histogram plot limits
          if maxi > mini
            histAx.XLim = [mini maxi] + [-1 1]*.02*rangei;
          else
            histAx.XLim = [-Inf Inf];
          end
          histAx.YLim = [.5 max([h.BinCounts*1.1, 1])]; % Make sure upper limit is at least 1
        end

        % Update histogram annotations; skip if values unchanged
        if isDiffToPrev(app,'hist',{ax maxi mini rangei imhi imlo u.gamma app.HistLog.Value})
          % Update ROIs
%           delete(findobj(histAx,'Tag','HistROI'))
          % Draw ROI of range if not yet
          if isempty(findobj(histAx,'Tag','HistROI'))
            app.A.hist.Box = drawrectangle(histAx,'Position',[1 1 1 1],'LineWidth',1,'MarkerSize',eps(), ...
              'FaceAlpha',.1,'InteractionsAllowed','translate');
            app.A.hist.Hi = drawpoint(histAx,'Position',[1 1]);
            app.A.hist.Lo = drawpoint(histAx,'Position',[1 1]);
            addlistener([app.A.hist.Box app.A.hist.Lo app.A.hist.Hi],'MovingROI',@moveHistHiLo);
            ud.Move = addlistener([app.A.hist.Box app.A.hist.Lo app.A.hist.Hi],'ROIMoved',@moveHistHiLo);
            set([app.A.hist.Box app.A.hist.Lo app.A.hist.Hi],'Deletable',0,'UserData',ud,'Tag','HistROI')
          end
          app.A.hist.Box.UserData = {ax maxi mini rangei imhi imlo}; % Save current display limits to ROIs
          % Update ROIs if not called from them
          if ~ismember(evt.Source, [app.A.hist.Box app.A.hist.Lo app.A.hist.Hi])
            moveHistHiLo(evt.Source, evt); 
          end

          % Update other annotations
          delete(findobj(histAx,'Tag','HistAnnot'))
          % Gamma line
          x = linspace(imlo,imhi,100);
          app.A.hist.gamCrv = plot(histAx,x,((x-imlo)/(imhi-imlo)).^u.gamma.*range(histAx.YLim)+histAx.YLim(1), ...
            'Color','k','Tag','HistAnnot');
          % Print display limits on the histogram
          app.A.hist.note = text(histAx,0.02,0.96,sprintf('Hi:% -.3g\nLo:% -.3g',imhi,imlo), ...
            'VerticalAlignment','top','BackgroundColor','w','Units','normalized', ...
            'FontName','FixedWidth',"FontWeight","bold","FontSize",11,'Tag','HistAnnot');
          app.A.hist.note.BackgroundColor(4) = .7;
        end

        debugToc(app, evt, "", dbT)

        % Sub function for ROI update
        function moveHistHiLo(src, evt)
          if isprop(evt,'CurrentPosition'), p = evt.CurrentPosition; end
          % Get preset values
          a = app.A.hist;  [iax,imax,imin,irange,hi,lo] = deal(a.Box.UserData{:});  yl = histAx.YLim;
          switch src
            case a.Box, lo = p(1);  hi = p(1)+p(3);
            case a.Lo, lo = p(1);
            case a.Hi, hi = p(1);
          end
          hi = max(lo,hi);  lo = min(lo,hi); % Sort out upper/lower limits
          % Find mid-height of the histogram, log- or linear-scale
          if app.HistLog.Value, ymid = sqrt(prod(yl)); else, ymid = mean(yl); end
          % Update ROI
          set([a.Box a.Hi a.Lo], {'Position'},{[lo, yl(1), hi-lo, yl(2)-yl(1)]; [hi ymid]; [lo ymid]})
          % Limit ROI translating area
          da = [histAx.XLim(1) ymid range(histAx.XLim) 0];  if any(isinf(da)), da='auto'; end
          set([a.Box a.Hi a.Lo],'DrawingArea',da,'Visible',app.DispContrast.Enable)
          % Update UI and image if called from ROIs
          if ismember(src,[a.Box a.Hi a.Lo])
            iax.UserData.brightness = max(min(double(50+(imax+imin-hi-lo)/2/irange*100),100),0);
            iax.UserData.contrast = max(min(double(2^((imax-imin-hi+lo)/2/irange*2)*50),100),0);
            displayCallbacks(app, evt); 
          end
        end
      end

      % Function to plot a vector field image over top of the DPC or CoM images (either magnitude, angle, or combination)
      function plotVectorField()
        delete(findobj(ax,'Tag',"VectorField"))
        vec = u.vecField;
        if ~vec || ~ismember(app.DetrMode.Value, ["CoMMod", "DPCMod"]), return; end
        % Plot vector arrows over the selected image
        app.A.vecField.(id) = quiver(ax, 1:vec:app.D.NFrX, 1:vec:app.D.NFrY, ...
          app.Image.CoMX(1:vec:end, 1:vec:end)'./vec, app.Image.CoMY(1:vec:end, 1:vec:end)'./vec, 1, ...
          'Color',u.vecColor,'LineWidth',1.5,'Tag',"VectorField");
      end

      % Function to plot color wheel
      function plotColorWheel()
        cla(app.Axes.ColorWheel)
        % Make ColorWheel for DPC/CoM imaging - this color scheme will stay constant for all DPC/CoM images
        % regardless of their individual parameters like scan or detector rotation for consistency
        width = cast(512, app.D.DataType);  r = width/2;
        [ygrid, xgrid] = meshgrid(1-r:r, 1-r:r);
        a = atan2d(ygrid, xgrid);       % Get atan from -180 to 180
        % shift the negative values of atan up by 360
        app.Image.ColorWheel = a .* (a >= 0) + (a+360) .* (a < 0);
        app.Image.ColorWheelMask = xgrid.^2 + ygrid.^2 < r^2;
        axis(app.Axes.ColorWheel,[0 width+1 0 width+1]);
        app.Axes.ColorWheel.UserData.maskOpa = 100;
      end
    end


    % Function to check whether the named given value is changed compared to the previous value, and store the new value
    function c = isDiffToPrev(app,name,val)
      c = ~isfield(app.Prev, name) || ~isequal(app.Prev.(name), val);
      if c, app.Prev.(name) = val; end
    end


    % Function to determine whether to update images
    %   Return true if any: 1) `app.CalcPolicy.Value` is 2 (active update)
    %                    OR 2) `app.CalcPolicy.Value` is 1 (reduced) and not when changing
    %                    OR 3) is a manual update (from update buttons or detector mode change)
    function upd = toUpdateImage(app,evt)
      calc = app.CalcPolicy.Value;
      upd = calc == 2 || (calc && isStaticEvt(evt)) || evt.Source == app.UpdateImages || evt.Source == app.DetrMode;
    end

    
    % Function to mock UI callbacks
    function mockUICallbacks(app,src,val)
      arguments, app;  src;  val = []; end
      % Set value if passed in
      if ~isempty(val), src.Value = val; end
      % Callbacks
      switch src
        case app.UpdateImages % Update all images
          updateImagesCallbacks(app, struct("Source",src,"EventName","ButtonPushed"))
          
        case app.DispImage % Update Display UI or Select current image
          displayCallbacks(app, struct("Source",src,"EventName","ValueChanged"))
          
        case app.SaveImgPrefix % Update image saving prefix
          saveCallbacks(app, struct("Source",src,"EventName","ValueChanged"))
          
        case {app.ShowDfrnAxes app.ShowRealAxes} % Update axes annotations
          axeDirCallbacks(app, struct('Source',src,'EventName',"ButtonPushed"))
          
        case app.RealROIShape % Update real-space controls
          realSpaceROICallbacks(app, struct("Source",src,"EventName","ValueChanged"));
          
        case app.CDT % Update Custom Detectors for Main Table selection change
          customDetectorCallbacks(app, struct('Source',src,'EventName',"SelectionChanged"))
          
        case app.CDDTable % Mock Custom Detector Detail Table edit to update ROI/images
          customDetectorCallbacks(app,struct("Source",src,"EventName","CellEdit"))
          
        case app.SaveTabGroup % Mock changing Save/Export tabs in Save window
          exportCallbacks(app, struct("Source",src,"EventName","SelectionChanged"))
          
        case app.ImpFileSelect % Mock import file select button
          importSelectFile(app,struct("Source",src,"EventName","ButtonPushed"));
          
        case app.DetrMode % Mock detector mode changed
          detectorModeCallbacks(app, struct("Source",src,"EventName","ValueChanged"));
          
        case app.PreviewButton % Mock "Import Preview" button
          previewCallbacks(app, struct('Source',src,'EventName',"ButtonPushed"))
      end
    end


    % Wrapper for notification dialogs; use `sprintf()` before calling this function to process "\n" in `msg`
    function sel = notifDLG(app, icon, msg, ttl, opt)
      arguments, app;  icon;  msg;  ttl = "";  opt = ["OK" "Cancel"]; end
      sel='';
      % Set global default UI font size
      fs = 9.5;  fs0 = get(0,'DefaultUIControlFontSize');  set(0,'DefaultUIControlFontSize',fs)
      beep
      switch icon
        case 'quest'
          % `questdlg()` will block all windows and background process
          if numel(opt) > 2
            sel = questdlg(msg, ttl, opt(1), opt(2), opt(3), opt(1));
          else
            sel = questdlg(msg, ttl, opt(1), opt(2), opt(1));
          end
        case 'list'
          % `listdlg()` will block all windows and background process
          sel = listdlg('ListString',opt,'SelectionMode','single',"PromptString",cellstr(split(msg,newline)), ...
            "Name",ttl,"ListSize",[300 150]);
        case {'help','warn','error','none',''}
          % The only way to set font size here is Tex; escape special characters in Tex; Tex is only used for font size
          msg = "\fontsize{"+fs+"}" + regexprep(msg,"([\\^_{}])","\\$1"); 
          enableWindows(app,false)  % Disable windows because `msgbox()` cannot block `uifigure()` windows
          f = msgbox(msg, ttl, icon, struct('WindowStyle','modal','Interpreter','tex'));
          f.DeleteFcn = {@(~,~) enableWindows(app,true)}; % Enable windows when the notification is gone
          uiwait(f) % Block background process until `msgbox()` is gone
      end
      set(0,'DefaultUIControlFontSize',fs0) % Reset global default UI font size
    end

    
    % Wrapper for `waitbar`
    function wb = progDLG(app, msg, ttl, interruptible)
      arguments, app;  msg;  ttl = "";  interruptible = 0; end

      enableWindows(app,false)  % Disable all windows
      set(app.G.AllFig,'Pointer','watch') % Set mouse cursor to "busy"
      if ~interruptible, ttl = "(Uninterruptible) "+ttl; end
      wb = waitbar(0,msg,"Name",ttl,"WindowStyle","modal");
      % For uninterruptible process:
      if ~interruptible
        findall(wb,'type','hgjavacomponent').JavaPeer.setIndeterminate(1);  % Indeterminate progress bar
        wb.CloseRequestFcn = [];  % Disable the close function
        wb.DeleteFcn = @(~,~) enableWindows(app,true); % Enable windows and reset mouse pointer when the progress windows is gone
      end
    end

    
    % Function to unload data and clean all images
    function unloadData(app, keep_p)
      arguments, app;  keep_p = 0; end
      
      enableWindows(app,false) % Disable windows for the data unload process
      app.Quant4D_Fig.Name = 'Quant4D';
      % Whether to swap dataset only, without changing any existing parameters
      if ~keep_p
        arrayfun(@(x) cla(x), app.G.ImgAx);  cla(app.HistAxes); % Clear all Axes
        app.P = [];  app.A = [];  app.Image = [];  app.Mask = [];  app.ImgD = [];  app.CDT.Data(:,:) = [];
      end
      % Remove all data from GPU if in use
      try if app.D.GPU > 0, reset(parallel.gpu.GPUDevice.getDevice(app.D.GPU)); gpuDevice([]); end; catch; end
      % Clear data, parameters and Axes
      app.Data = [];  app.Memfile = [];  app.D = [];  app.Prev = [];
    end

    
    % Function to enable/disable windows/UI; disable is only for notification/progress bar/busy background etc
    function enableWindows(app,sw)
      arguments, app;  sw = true; end
      prvw = app.DetrMode.Value == "PrvwMod"; % Preview mode or not
      % Detector Mode UI, keep disabled in Import Preview Mode unless a dataset is loaded
      set(app.DetectorModeGrid.Children,"Enable",switchOnOff(sw && (~prvw || ~isempty(app.D))))
      % Real-space ROI controls, keep disabled in Import Preview Mode
      set(app.RealSpacePanel,'Enable',switchOnOff(sw && ~prvw))
      % Other UIs can be enabled in Import Preview Mode
      set([app.ShortcutButtonGrid.Children; app.DfrnDetrPanel; app.SettingsPanel; app.SavePanel; app.ImportPanel], ...
        'Enable',switchOnOff(sw))
      % Disable all images when not "on"; visible means disable
      set(app.G.ImgGyO,'Visible',~sw)
      % Also reset all windows' mouse pointer when enabling UIs
      if sw, set(app.G.AllFig,'Pointer','arrow'); end
    end

    
    % Function to create other UI windows and Image figures
    function createOtherWindows(app)
      dbT = tic;

      % Set window position without using `movegui()`, to avoid its implicit `drawnow`
      th = app.C.ttlH;  dw = app.C.decW;  sn = app.C.ScreenAvl; % sn = [left bottom width height]
      % Available sizes of width/height/left/bottom/right/top
      sw = sn(3);  sh = sn(4);  sl = sn(1)+dw/2;  sb = sn(2);  sr = sl+sw-dw;  st = sb+sh-th; % Top excludes title bar
      shc = (sl+sr)/2;  svc = (sb+st)/2;  sz = floor(min(sw,sh)/2-th); % Horizontal/Vertical centers and image size
      % Set limits/values for image window resize options
      set([app.WdwWDfrn app.WdwHDfrn app.WdwWReal app.WdwHReal], {'Limits'},{[1 sw];[1 sh];[1 sw];[1 sh]}, 'Value',sz)
      
      % Create Image Windows. Inputs:
      %   id, title, space (Dfrn/Real/ColorWheel/Preview), type (Primary/Mask/CoM/Test/Preview), colormap, position/size
      createAxesFig("ColorWheel","Color Wheel for Phase Direction","ColorWheel","CoM","hsv",[shc 1 200 200]);
      axtoolbar(app.Axes.ColorWheel, {'datacursor'});
      createAxesFig("Dfrn","Diffraction","Dfrn","Primary","gray",[shc-sz/2 st-sz sz sz]); % Top-center
      createAxesFig("DfrnMask","Diffraction Mask","Dfrn","Mask","gray",[shc-sz/2 1 sz sz]); % Botton-center
      % Place Real-space images on the right, from top to bottom
      l = sr-sz;  wb0 = st-sz;  b = wb0;  bi = wb0/8;
      createAxesFig("Real","Real-space","Real","Primary","gray",[l b sz sz]);  b = b-bi;
      createAxesFig("CoMPhMag","CoM Phase (Magnitude-shaded)","Real","CoM","hsv",[l b sz sz]);  b = b-bi;
      createAxesFig("CoMPh","CoM Phase","Real","CoM","hsv",[l b sz sz]);  b = b-bi;
      createAxesFig("CoMMag","CoM Magnitude","Real","CoM","gray",[l b sz sz]);  b = b-bi;
      createAxesFig("CoMX","CoM X","Real","CoM","gray",[l b sz sz]);  b = b-bi;
      createAxesFig("CoMY","CoM Y","Real","CoM","gray",[l b sz sz]);  b = b-bi;
      createAxesFig("dCoM","dCoM","Real","CoM","gray",[l b sz sz]);  b = b-bi;
      createAxesFig("iCoM","iCoM","Real","CoM","gray",[l b sz sz]);  b = b-bi;
      createAxesFig("RealMask","Real-space Mask","Real","Mask","gray",[l b sz sz]);
      if app.Debug
        createAxesFig("tDfrn","Test Diffraction","Dfrn","Test","gray",[shc-sz/2 1 sz sz]); % Botton-center
        createAxesFig("tReal","Test BF/DF","Real","Test","gray",[l b sz sz]);
      end
      % Preview image for import
      createAxesFig("Preview","Preview","Preview","Preview","gray",[sr-sz svc-sz/2 sz sz]); % Center-left

      % Variable names, image names and image types (tag) for all patterns'/images' figures/axes/images
      app.G.ImgID = string(fieldnames(app.Axes))'; % ID/fieldnames under `app.Axes` `app.Fig` `app.Image` `app.ImgD` etc
      app.G.ImgSp = string(structfun(@(x) x.UserData.space, app.Axes))'; % Spaces ("Real"/"Dfrn")
      app.G.ImgTyp = string(structfun(@(x) x.UserData.type, app.Axes))'; % Types ("Primary", "CoM" related, "Mask", "Test")
      app.G.ImgNm = string(structfun(@(x) x.UserData.name, app.Axes))'; % Names/Titles
      % AND their Axes/Figure objects, as well as the gray overlay to disable them
      app.G.ImgAx = arrayfun(@(x) app.Axes.(x), app.G.ImgID);
      app.G.ImgFig = arrayfun(@(x) app.Fig.(x), app.G.ImgID);
      app.G.ImgGyO = arrayfun(@(x) app.Fig.(x).UserData.grayout, app.G.ImgID); % Set them visible to disable the axes
      % Variable names for all diffraction-sized figures/axes/images AND THEN their Axes objects
      app.G.DfrnID = app.G.ImgID(app.G.ImgSp == "Dfrn");
      app.G.DfrnAx = arrayfun(@(x) app.Axes.(x), app.G.DfrnID);
      % Variable names for all real-space-sized figures/axes/images AND THEN their Axes objects
      app.G.RealID = app.G.ImgID(app.G.ImgSp == "Real");
      app.G.RealAx = arrayfun(@(x) app.Axes.(x), app.G.RealID);
      % Group all "Show ... Window" buttons related to CoM/DPC
      app.G.CoM_btns = [findobj(app.ShowImageWindowsGrid,'-regexp','Tag','CoM'); ...
        app.ShowColorWheelWdw; app.ShowColorWheelWdw_2];
      % Group all diffraction detector panels
      app.G.DetrUI = [app.PreviewGrid app.AlignmentGrid app.AnnDetrGrid app.VirtualApertureGrid app.CustomDetectorGrid];
      
      % Transfer all detector panels to main window, then delete their old container
      set(flip(app.G.DetrUI),'Parent',app.DfrnDetrPanel); delete(app.DfrnDetrTabGroup)
      % Create other UI Windows
      app.Fig.Settings = moveUI2NewFig('Settings', app.SettingsPanel);
      app.Fig.Settings.Position(1:2) = [sum(app.Quant4D_Fig.Position([1,3])) + dw + 2, ...
        st - app.Fig.Settings.Position(4)]; % Move next to main window
      app.Fig.Import = moveUI2NewFig('Import Data', app.ImportPanel);
      app.Fig.Import.Position(1:2) = ([shc svc]-app.Fig.Import.Position(3:4)/2); % Move to center
      app.Fig.Import.CloseRequestFcn = @(~,~)importCallbacks(app, struct("Source", app.ImportCancelButton, ...
        "EventName",'ButtonPushed')); % Set `app.Fig.Import` window close as "pushing `app.ImportCancelButton"
      app.Fig.Save = moveUI2NewFig('Save/Export', app.SavePanel);
      app.Fig.Save.Position(1:2) = ([shc svc]-app.Fig.Save.Position(3:4))/2; % Move to center
      app.Fig.Save.CloseRequestFcn = @(~,~)exportCallbacks(app, struct("Source", app.SaveCloseButton, ...
        "EventName",'ButtonPushed')); % Set `app.Fig.Save` window close as "pushing `app.SaveCloseButton`"
      % Set main windows `app.Quant4D_Fig` other properties
      app.Quant4D_Fig.Position(1:2) = [sl st-app.Quant4D_Fig.Position(4)]; % Move to top-left
      app.Quant4D_Fig.SizeChangedFcn = {@minSize, app.Quant4D_Fig.Position(3:4)};
      app.Quant4D_Fig.KeyPressFcn = @keyPress;
      % When delete the main window `app.Quant4D_Fig` (e.g. closing), also delete other windows
      app.Quant4D_Fig.DeleteFcn = {@(~,~,figs) delete(figs), structfun(@(x) x, app.Fig)};
      % Group all window `figure` `uifigure`
      app.G.AllFig = [app.Quant4D_Fig; structfun(@(f) f, app.Fig)];

      debugToc(app, [], "", dbT)


      %%% Sub functions of `otherFigures()`
      % Limit minimum window size
      function minSize(src, ~, wh)
        src.Position(3:4) = max(src.Position(3:4), wh);
        movegui(src)
      end
      
      % Keyboard shortcuts
      function keyPress(~, evt)
        dbT = tic;
        switch evt.Key
          case 'f5'
            if app.UpdateImages.Enable, mockUICallbacks(app,app.UpdateImages); end
        end
        debugToc(app, evt, "", dbT)
      end
      
      % Hide window instead of closing it
      function hideWindow(src, ~)
        if isvalid(app), src.Visible = 'off'; else, delete(src); end
      end
      
      % Transplant `UI` from its parent to a new separated Figure `fig`
      function fig = moveUI2NewFig(name, ui)
        fig = uifigure('Name',name,'Visible','off','Position',[1 1 ui.Position(3:4)+2],'AutoResizeChildren','off', ...
          'CloseRequestFcn',@hideWindow,'SizeChangedFcn',{@minSize, ui.Position(3:4)+2},'KeyPressFcn',@keyPress);
        grd = uigridlayout(fig,[1 1],'Padding',[0 0 0 0]);
        ui.Parent = grd;
      end
      
      % Create Image Window/Axes
      function createAxesFig(id, name, sp, typ, cmap, pos)
        fig = figure('Visible',"off", 'Name',name, 'Position',pos, 'MenuBar',"none", 'NumberTitle',"off", ...
          'IntegerHandle',"off", "Color",app.C.BgC, "InvertHardcopy",0, 'WindowButtonDownFcn',@clickedWindow, ...
          'CloseRequestFcn',@hideWindow,'KeyPressFcn',@keyPress,'Tag',sp+" "+typ);
        % An overlay on figure to cover axes; disables the axes when visible
        grayout = annotation(fig,"rectangle",[0 0 1 1],"Visible","off","FaceColor",[.96 .96 .96],"FaceAlpha",.7);
        % Not `Clipping` axes to let images expand beyond the axes when zooming in
        ax = axes(fig, 'Color','k', 'Colormap',feval(cmap), 'CLimMode','manual', 'Position',[0 0 1 1], ...
          'DataAspectRatio',[1 1 1], 'XTick',[], 'YTick',[], 'XColor','k', 'YColor','k', 'Box',1, 'Clipping',0, ...
          'NextPlot',"add",  'Interactions',[], 'Tag',sp+" "+typ);
        % Toolbar & its `restoreview()`
        tb = axtoolbar(ax, {'export', 'datacursor', 'pan', 'zoomin', 'zoomout', 'restoreview'});
        tb.Children(end).ButtonPushedFcn = @restoreView;
        % Data Tips
        dcm = datacursormode(fig);  dcm.UpdateFcn = @showVal;
        set(dcm.UIContextMenu.Children,'Visible','off')
        % Image properties
        if cmap == "gray", vC = 'r'; else, vC = 'w'; end
        ax.UserData = struct('id',id,'name',name,'space',sp,'type',typ,'colormap',cmap,'invert',0,'maskOpa',0, ...
          'brightness',50,'contrast',50,'gamma',1,'vecField',0,'vecColor',vC);
        fig.UserData = struct('id',id,'name',name,'space',sp,'type',typ,'grayout',grayout);
        app.Fig.(id) = fig;  app.Axes.(id) = ax;

        %% Sub sub functions
        % "restoreview" goes back to the limits of the actual image, nothing more/less.
        function restoreView(~,evt)
          axis(evt.Axes, app.P.(evt.Axes.UserData.space+"AxLim"))
        end
        % Modify Data Tips to show the raw value from `app.Image.(...)`
        function txt = showVal(~,evt)
          x = evt.Position(1);  y = evt.Position(2);
          v = strtrim(sprintf('%14.7g',app.Image.(evt.Target.Parent.UserData.id)(x,y)));
          txt = sprintf('Value: \\bf%s\n\\rmX: \\bf%g\\rm, Y: \\bf%g',v,x,y);
        end
        % Select image in Display/constrast panel
        function clickedWindow(src, ~)
          id = string(src.UserData.id);
          if ~app.DispLock.Value && app.DispImage.Value ~= id && ismember(id, app.DispImage.ItemsData)
            mockUICallbacks(app, app.DispImage, id)
          end
        end
      end
    end

    % Function to check nan/inf in data/image
    function sel = checkNaN(app, im, prvw)
        sel='';
        if any(isnan(im),'all') || any(isinf(im),'all')
            ttl = 'NaN/Inf in Data!';
            txt = "There are NaN/Inf values in the data! Which may indicate the data structure is not correctly set " ...
                + "(e.g. wrong Data Type, Byte Order, Data Offset, Frame Header/Footer etc).\n\nIf any data are corrupt, NaNs can be set to 0.";

            if prvw % For preview only
                sel = notifDLG(app, 'quest', sprintf(txt), ttl, ["Continue","Set NaNs to 0"]);
            elseif app.D.PxD > 1 || app.D.FrFoot + app.D.FrHead > 0
                sel = notifDLG(app, 'quest', sprintf(txt+"\n\nRe-importing with corrected configuration is suggested."), ttl,["Continue","Set NaNs to 0"]);
            else
                sel = notifDLG(app, 'quest', sprintf(txt+"\n\nDo you want to swap the byte-order?"), ttl, ...
                    ["Yes, try to swap the byte-order","No"]);
                app.SettingsTabGroup.SelectedTab = app.InfoTab;  figure(app.Fig.Settings)  % Select the Data Info tab
                % Execute the swap byte order callbacks
                if startsWith(sel,"Yes")
                    datasetOptCallbacks(app,struct('Source',app.SwapByteOrder,'EventName',"ButtonPushed"))
                end
            end
        end
    end

  end


    % Callbacks that handle component events
    methods (Access = private)

        % Code that executes after component creation
        function startupFcn(app, debug)
      arguments, app; debug = 0; end
      dbT = tic;
      app.Debug = debug; % Non-0 values for debugging
      app.Quant4D_Fig.Visible = 'off'; % Hide until startup process is ready
      app.C.ScreenSize = get(0, 'ScreenSize'); % Get main screen size (Matlab "pixels")
      app.C.MonitorPositions = get(0,'MonitorPositions');  % Get all monitor position/size
      % Scale for Matlab "pixels" vs actual pixels, for HiDPI
      app.C.ScreenPxScale = app.C.ScreenSize(4)/java.awt.Toolkit.getDefaultToolkit.getScreenSize.height;
      % A Java window to measure window decorations like "title bar"/"border width"
      jf = javax.swing.JFrame('Test');  jf.setDefaultCloseOperation(javax.swing.JFrame.DISPOSE_ON_CLOSE);  jf.pack();
      ins = jf.getInsets(); % Not accurate for Windows OS, due to the transparent shadow 
      app.C.ttlH = ins.top*app.C.ScreenPxScale;
      app.C.decH = app.C.ttlH + ins.bottom*app.C.ScreenPxScale;
      app.C.decW = (ins.left + ins.right)*app.C.ScreenPxScale;
      jf.dispose()
      % Actual avaiable main screen size excluding taskbar etc
      ins = java.awt.Toolkit.getDefaultToolkit().getScreenInsets(getGraphicsConfiguration(javax.swing.JFrame));
      ins = [ins.left, ins.bottom, ins.right+ins.left, ins.top+ins.bottom]*app.C.ScreenPxScale;
      app.C.ScreenAvl = [ins(1:2)+1, app.C.ScreenSize(3:4)-ins(3:4)];
      % Get other system constants
      app.C.BgC = app.Quant4D_Fig.Color;  % Default app background color
      app.C.WarnC = [1 .65 0];  % Warning color
      [~,~,app.C.SysEndian] = computer();  % Get native endianness
      app.C.SysEndian = lower(app.C.SysEndian);
      app.C.EndianTxt = struct('l','Little Endian','b','Big Endian');
      app.HistAxes.Interactions = [];  % Disable histogram interactions
      % Setup "Custom Detector" tables
      set(app.CDT,'SelectionType','row', 'Multiselect',0, 'Data',table('Size',[0 6], ...
        'VariableTypes',{'string','string','string','logical','logical','double'}, ...
        'VariableNames',{'ID','Type','Label','Enable','Show','Weight'}));
      app.CDDTable.ColumnFormat = {'bank','bank','bank'};
      createOtherWindows(app)     % Create Other Panel and Image Windows
      enableWindows(app,false)  % Keep UIs disabled
      getMem(app);  getGPU(app)  % figure out how much RAM is available and look for gpu(s)

      % Open the import file selection window to let user select file before initialization finish
      %mockUICallbacks(app, app.ImpFileSelect)
      app.Quant4D_Fig.Visible = 'on';
      % Reset app UI and data, which enters Import Preview Mode
      resetQuant4DCallbacks(app, struct("Source","startupFcn","EventName",[]))
      % Plot axes display directions
      mockUICallbacks(app,app.ShowDfrnAxes);  mockUICallbacks(app,app.ShowRealAxes)
      % Link Axes limits for zooming, `drawnow` implied
      linkaxes(app.G.RealAx);  linkaxes(arrayfun(@(x) app.Axes.(x), app.G.DfrnID))

      debugToc(app, [], "`startupFcn` finished", dbT)
        end

        % Callback function: ImportCancelButton, ImportDataButton, 
        % ...and 2 other components
        function importCallbacks(app, event)
      switch event.Source
        case app.ShowImportWdw
          figure(app.Fig.Import)
          % Enter Import Preview Mode
          if app.DetrMode.Value ~= "PrvwMod", mockUICallbacks(app,app.DetrMode,"PrvwMod"); end

        case app.ImportCancelButton % Hide window when closing
          app.Fig.Import.Visible = 'off'; 
          % Try to re-enter previous detector mode from Import Preview Mode
          if app.DetrMode.Value == "PrvwMod" && isfield(app.P,'DetrMode')
            mockUICallbacks(app,app.DetrMode,app.P.DetrMode);
          end

        case app.ReimportMenu % Reimport the current dataset, mostly for debugging
          if ~isfield(app.T,'prev_D'), return; end
          unloadData(app)
          app.D = app.T.prev_D;
          importData(event)

        case {app.ImportDataButton app.PreviewButton} % When the "Import Data" or "Preview" button is pressed
          app.T.Preview = [];
          if ~isfile(app.ImpFilePath.Value)
            notifDLG(app, 'warn', 'The entered file path is invalid!', 'Invalid File!');
          elseif app.ImpDataType.Value == "unknown"
            notifDLG(app, 'warn', 'Select the correct data type!', 'Select Data Type!');
          else
            if event.Source == app.ImportDataButton % Import data
              app.Fig.Import.Visible = 'off';
              unloadData(app, app.ImpKeepP.Value)
              app.D = gatherImportOptions(0);
              app.T.prev_D = app.D; % Backup current `app.D`
              importData(event)
            else % Preview
              app.T.Preview = gatherImportOptions(1);
            end
          end

        case {app.SwapDfrnXY app.SwapRealXY} % Refresh axes settings etc when dimensions swapped
          prepareData(event)

      end


      %%% Sub functions
      % Function to read Import Panel options into `app.D`
      function d = gatherImportOptions(prvw)
        d.filePath = app.ImpFilePath.Value;  
        [d.fileDir, d.fileName, d.fileExt] = fileparts(d.filePath);
        d.fileDir = strcat(d.fileDir, filesep);
        d.subImg = app.ImpSubImg.Value;
        % BYTES offset of: 1) the dataset from the beginning of file, 2) before and 3) after each frame
        d.Offset = app.DataOffset.Value;  d.FrHead = app.FrHead.Value;  d.FrFoot = app.FrFoot.Value;
        % Endianness (big 'b' or little 'l'), Data type of the dataset and Size in bytes of the data type
        d.ByteOrder = app.ImpByteOrder.Value;  d.DataType = app.ImpDataType.Value;  d.ByteSize = app.ByteSize.(d.DataType);
        % Physical or virtual memory loading
        d.mem = app.ImpMemType.Value;
        % Select GPU if acceleration is enabled AND not in Import Preview Mode
        d.GPU = app.ImpGPU.Value;  if ~prvw && d.GPU, gpuDevice(d.GPU); end
        % Dimensions of pixels/frames in file and import binning/sampling distance
        d.DNPxX = app.DNPxX.Value;  d.DNPxY = app.DNPxY.Value;  d.PxD = app.IPxD.Value;
        d.DNFrX = app.DNFrX.Value;  d.DNFrY = app.DNFrY.Value;  d.FrD = app.IFrD.Value;
        % Starting points and Number of pixels/frames after binning/sampling to import
        d.PxX1 = app.IPxX1.Value;  d.PxY1 = app.IPxY1.Value;  d.NPxX = app.INPxX.Value;  d.NPxY = app.INPxY.Value;
        d.FrX1 = app.IFrX1.Value;  d.FrY1 = app.IFrY1.Value;  d.NFrX = app.INFrX.Value;  d.NFrY = app.INFrY.Value;
        % Frequently used dimension parameters
        d.NPx = [d.NPxX d.NPxY];  d.NPxS = d.NPxX * d.NPxY;
        d.NFr = [d.NFrX d.NFrY];  d.NFrS = d.NFrX * d.NFrY;
        % Estimated memory usage for current dataset
        d.EstMem = app.T.EstMem;
        % Swap dataset option+app.ImpNotes.Value;
        d.KeepP = app.ImpKeepP.Value; 
        % Notes at import
        d.NoteFileMeta = app.ImpFileMetaNotes.Value;  d.NoteImp = app.ImpNotes.Value;
        % H5 dataset path within the H5 file; if not set empty, the H5 library API will be called when importing
        d.h5ds = [];  if app.HDF5Button.Value && d.mem == "Physical Memory", d.h5ds = d.subImg; end
      end

      % Initialize GUI/Image/app.P for the data
      function prepareData(evt)
        app.T.progDLG = progDLG(app, 'Preparing data ...', "Data Preparation");
        % Detector controls
        app.P.ScanDirInit = 0; % Reset alignments
        app.DetrMode.Value = "AlignMod";  app.AnnRLink.Value = 0;  % Prepare to enter alignment mode
        set([app.NSeg app.NRung app.DetRot app.DetRot_NF app.ScanDir app.ScanDir_NF],{'Value'},{4;1;0;0;0;0})
        set([app.VrApSymm app.VrApInvert app.VrApMirror app.VrApMirrRot],{'Value'},{1;0;0;0})
        % Alignments
        app.P.DfCtr = app.D.NPx/2+.5;  % Exact center of the Diffraction image
        app.P.RsCtr = app.D.NFr/2+.5;  % Exact center of the Real-space image
        app.Alpha.Value = 1;  app.P.VrApXY = app.P.DfCtr;
        % Axes limits, restrict to avoid rounding to pixels outside the image
        app.P.DfrnAxLim = [0.51, app.D.NPxX + .49, 0.51, app.D.NPxY + .49];
        app.P.RealAxLim = [0.51, app.D.NFrX + .49, 0.51, app.D.NFrY + .49];
        set(app.G.DfrnAx, "XLim",app.P.DfrnAxLim(1:2), "YLim",app.P.DfrnAxLim(3:4));
        set(app.G.RealAx, "XLim",app.P.RealAxLim(1:2), "YLim",app.P.RealAxLim(3:4));
        % Transmitted Beam controls
        if evt.Source ~= app.SwapRealXY % Keep transmitted beam alignment if swapping Real-space X/Y
          app.P.TransBeamInit = 0;  
          set([app.TBR app.TBX app.TBY],{'Limits'},{[eps() max(app.D.NPx)]; [0 app.D.NPxX]; [0 app.D.NPxY]}, ...
            {'Value'},{min(app.D.NPx)/10; app.P.DfCtr(1); app.P.DfCtr(2)});
          set([app.TBX_NF app.TBY_NF],{'Limits'},get([app.TBX app.TBY],'Limits'))
          transBeamCallbacks(app,evt) % Update Transmitted Beam dependant variables
        end
        % Real-space ROI controls
        set([app.FrameX app.FrameY],{'Limits'},{[0 app.D.NFrX];[0 app.D.NFrY]}, ...
          {'Value'},{app.P.RsCtr(1);app.P.RsCtr(2)})
        app.RealROIInvert.Value = 0;  app.RealROIShape.Value = "full";
        % Export controls
        exportCallbacks(app, struct("Source",app.ExpPxPart,"EventName",[],"Value",0))
        exportCallbacks(app, struct("Source",app.ExpFrPart,"EventName",[],"Value",0))
        % Image display contrasts and vector field
        for ax = app.G.ImgAx
          ax.UserData.brightness = 50;  ax.UserData.contrast = 50;  ax.UserData.gamma = 1;
          ax.UserData.maskOpa = 0;  ax.UserData.vecField = 0;
        end
        
        mockUICallbacks(app,app.UpdateImages) % Update all images
        delete(app.T.progDLG);  % Close progress bar and Enable panel objects
        mockUICallbacks(app,app.DetrMode)  % Enter intializing alignment
        app.SettingsTabGroup.SelectedTab = app.DisplayTab;  figure(app.Fig.Settings)  % Show the brightness
        flashBackground(app, [app.DfrnCalibGrid app.TransBeamAlignGrid])
      end

      % Function to import data
      function importData(evt)
        dbT = tic;

        if ~isfile(app.D.filePath)
          notifDLG(app,'warn',"File: '"+app.D.filePath+"' is not found!",'File Unfound!');
          return
        end
        % Set save/export filenames etc.
        app.Quant4D_Fig.Name = "Quant4D: "+app.D.fileName+app.D.fileExt;
        app.SaveDir.Value = app.D.fileDir;  app.SaveImgPrefix.Value = app.D.fileName+"_";
        app.ExpFilename.Value = app.D.fileName+"_export";

        % Start file reading here
        try
          err = readFile();
        catch ME
          try stop(app.T.tmr), delete(app.T.tmr); catch; end % Kill the reading progress update timer
          try delete(app.T.progDLG); catch; end
          try unloadData(app); catch; end
          stk = "";
          for i = 1:numel(ME.stack)
            stk = sprintf('%s\n%s, Line: %d',stk,ME.stack(i).name,ME.stack(i).line);
          end
          notifDLG(app,'error',sprintf('%s\n%s\n%s%s',ME.identifier,ME.message,ME.Correction,stk), ...
            'Error during Import!');
          enableWindows(app,true)
          rethrow(ME)
        end
        % If aborted or errors occured during file reading, reset app like just opened without import
        if err == -1, resetQuant4DCallbacks(app, evt);  return; end
        debugToc(app, evt, "", dbT)

        % Prepare imported data
        if app.D.KeepP
          app.DetrMode.Value = "AlignMod";  % Enter alignment mode
          % Not re-initalizing and just to update all images if "swap data"
          mockUICallbacks(app,app.UpdateImages)
          mockUICallbacks(app,app.DetrMode)
          datasetOptCallbacks(app, evt) % Swap byte check
        else
          prepareData(evt)  
        end

        
        %%%% Sub sub functions
        % Sub sub function to read file into memory
        function err = readFile()
          dbT = tic;  err = 0;
          % Use local variables, which is faster
          offs = app.D.Offset;  hdr = app.D.FrHead;  ftr = app.D.FrFoot;
          order = app.D.ByteOrder;  dtype = app.D.DataType;  bsize = app.D.ByteSize;
          dnpx = app.D.DNPxX;  dnpy = app.D.DNPxY;  pd = app.D.PxD;
          dnfx = app.D.DNFrX;  dnfy = app.D.DNFrY;  fd = app.D.FrD;
          px1 = app.D.PxX1;  py1 = app.D.PxY1;  npx = app.D.NPxX;  npy = app.D.NPxY;
          fx1 = app.D.FrX1;  fy1 = app.D.FrY1;  nfx = app.D.NFrX;  nfy = app.D.NFrY;
          frsize = npx*npy*pd^2*bsize;

          % convert to single/double if int/uint
          dtype1 = dtype;
          if contains(dtype,'int')
            if bsize > 4, dtype1 = 'double'; bsize1 = 8;  else, dtype1 = 'single'; bsize1 = 4; end
            app.D.DataType = dtype1;  app.D.ByteSize = bsize1;
          end

          [app.T.progDLG, app.T.tmr] = progImportExport(app, "Import", app.D.NFrS, frsize);

          if ~isempty(app.D.h5ds) % HDF5 import
            data = zeros(npx, npy, nfx, nfy, dtype1); % Pre-allocate array
            fid = H5F.open(app.D.filePath);   dset_id = H5D.open(fid, app.D.h5ds);
            file_space_id = H5S.create_simple(4, [dnfy dnfx dnpy dnpx], []);
            mem_space_id = H5S.create_simple(2, [npy*pd npx*pd], []);
            % data = H5D.read(dset_id,'H5ML_DEFAULT','H5S_ALL','H5S_ALL','H5P_DEFAULT'); % Read whole
            for ify = 1:nfy
              for ifx = 1:nfx
                if ~isvalid(app.T.progDLG), err = -1; break; end % Cancel if progress window closed
                app.T.frameJ(1) = (ify-1)*nfx + ifx; % Update processed Frame Number for progress update
                H5S.select_hyperslab(file_space_id, 'H5S_SELECT_SET', [fy1+(ify-1)*fd, fx1+(ifx-1)*fd, py1, px1]-1, ...
                  [],[], [1 1 npy*pd npx*pd]); % Read 1 frame at a time; C-like array indices for H5 low-level APIs
                frame = H5D.read(dset_id, 'H5ML_DEFAULT', mem_space_id, file_space_id, 'H5P_DEFAULT');
                if pd > 1, frame = squeeze(sum(reshape(frame, [pd npx pd npy]), [1 3]),'omitnan'); end % Pixel binning
                data(:, :, ifx, ify) = frame; % Store frame
              end
              if err == -1, break; end
            end
            % Close opened handles
            H5S.close(mem_space_id);  H5S.close(file_space_id);  H5D.close(dset_id);  H5F.close(fid);
            data = reshape(data, app.D.NPxS, app.D.NFrS); % Make dataset a 2D array
            app.Data = data;
          elseif app.D.mem == "Physical Memory" % General reading method; read data into physical memory
            data = zeros(npx, npy, nfx, nfy, dtype1); % Pre-allocate array
            dfrSize = hdr+dnpx*dnpy*bsize+ftr; % frame size including header/footer
            fid = fopen(app.D.filePath,'r');
            for ify = 1:nfy
              for ifx = 1:nfx
                if ~isvalid(app.T.progDLG), err = -1; break; end % Cancel if progress window closed
                app.T.frameJ(1) = (ify-1)*nfx + ifx; % Update processed Frame Number for progress update
                % Read 1 frame at a time; move cursor to "frame offset" + "pixel Y offset" in file dataset
                dfx = fx1+(ifx-1)*fd;  dfy = fy1+(ify-1)*fd; % Frame indices in dataset file
                fseek(fid, offs + (dfx-1 + (dfy-1)*dnfx) * dfrSize + hdr + ((px1-1) + (py1-1)*dnpx) * bsize, 'bof');
                frame = fread(fid, [dnpx, npy*pd], dtype, 0, order); % Read including "pixel X offset"
                if npx*pd ~= dnpx, frame = frame(px1:px1+npx*pd-1, :); end % Crop "pixel X offset" off from array memory
                if pd > 1, frame = squeeze(sum(reshape(frame, [pd npx pd npy]), [1 3]),'omitnan'); end % Pixel binning
                data(:, :, ifx, ify) = frame; % Store frame
              end
              if err == -1, break; end
            end
            fclose(fid);
            data = reshape(data,app.D.NPxS,app.D.NFrS); % Make dataset a 2D array
            app.Data = data;
          elseif app.D.mem == "Virtual Mapping" % Virtual memory mapping
            % Create a memory mapped file, rather than reading the file directly into memory
            if ~strcmp(app.C.SysEndian, order)
              error("Dataset's endianness is different to that of the system's!")
            end

            if hdr == 0 && ftr == 0
              app.Memfile = memmapfile(app.D.filePath,'Offset',offs, ...
                'Format',{dtype1,[app.D.NPxS app.D.NFrS],'data'}, 'Repeat',1);
              app.Data = app.Memfile.Data.data;
            else
              error("Virtual memory with header/footer > 0 not supported yet.")
            end
          end
          clear data
          delete(app.T.progDLG) % Delete the interruptable progress window
          % Move to GPU if enabled
          if app.D.GPU > 0 && err == 0
            app.T.progDLG = progDLG(app,"Moving dataset to GPU memory ...","GPU Transfer");
            app.Data = gpuArray(app.Data);
            delete(app.T.progDLG)
          end

          sel = checkNaN(app,app.Data(:),1); % Check data NaN/Inf, without asking to sway byte-order
          if strcmp(sel,'Set NaNs to 0')
              app.Data(isnan(app.Data(:)))=0;
          end

          debugToc(app, evt, "", dbT)
        end

      end
        end

        % Callback function: ImpFilePath, ImpFileSelect
        function importSelectFile(app, event)
      dbT = tic;

      if event.Source == app.ImpFileSelect
        [fileName, fileDir] = uigetfile({'*.raw;*.mib;*.mrc;*.dm3;*.dm4;*.npy;*.h5;*.hdf5','Supported Formats'; ...
          '*.*','All Files'}, 'Select 4DSTEM Dataset');
        set(app.Fig.Import,'Visible','off','Visible','on'); % Force to show
        if fileName, app.ImpFilePath.Value = fullfile(fileDir, fileName); end
      end
      
      if isfile(app.ImpFilePath.Value)
        [fileDir, ~, fileExt] = fileparts(app.ImpFilePath.Value);
        cd(fileDir)
        app.T.FileSize = dir(app.ImpFilePath.Value).bytes;
        % Display actual file size in bytes and GiB
        app.ImpActualFilesize.Text = sprintf('%d bytes, %.1f GiB',app.T.FileSize,app.T.FileSize/1024^3);
  
        switch lower(fileExt)
          case ".mib" % Medipix data
            app.MedipixButton.Value = 1;
          case ".mrc" % mrc data
            app.MRCButton.Value = 1;
          case {".dm3"; ".dm4"} % Gatan K2/K3 data
            app.DM34Button.Value = 1;
          case {".h5"; ".hdf5"}
            app.HDF5Button.Value = 1;
          case {".raw"}
            app.EMPADButton.Value=1;
          otherwise
            app.CustomButton.Value = 1;
        end
      else
        app.ImpActualFilesize.Text = '';  app.T.FileSize = 0;
      end

      debugToc(app, event, "", dbT)
      % Further file info
      importFileType(app,event)
        end

        % Callback function: ImpFileTypeButtonGroup, ImpSubImg
        function importFileType(app, event)
      % Make an initial guess at the file dimensions (assume ~square field of view: NFrX≈NFrY)
      function guessFramesFromSize()
        if app.DNPxX.Value > 1 && app.DNPxY.Value > 1
            x = sqrt((app.T.FileSize-app.DataOffset.Value-app.T.fileTail) ...
              /(app.DNPxX.Value*app.DNPxY.Value*app.ByteSize.(app.ImpDataType.Value)+app.FrHead.Value+app.FrFoot.Value));
            set([app.DNFrX app.DNFrY],'Value',max(floor(x),1))
        end
      end

      % Guess numbers of Frame X and Y from 3D dataset (with only Frame X)
      function guessFramesFromDimZ(dz)
        app.DNFrX.Value = round(sqrt(dz));
        app.DNFrY.Value = round(dz/app.DNFrX.Value);
      end

      % Guess dataset size from fileName in the following style (only the first match):
      %   fileName = 'fooAxBxCxDbar', where:  A = NPxX, B = NPxY, C = NFrX, D = NFrY, and are numbers
      function getDimFromName(name)
        %s = regexp(name,"\d*x\d*x\d*x\d*",'match');
        %if ~isempty(s)
        %  set([app.DNPxX app.DNPxY app.DNFrX app.DNFrY],{'Value'},num2cell(str2double(strsplit(s{1},'x')))')
        %end

        s = regexp(name,["scan_x(\d*)_y(\d*).raw","(\d*)x(\d*)x(\d*)x(\d*)"],'tokens');
        if ~isempty(s{1})
            set([app.DNPxX app.DNPxY app.DNFrX app.DNFrY],{'Value'},num2cell([128 128 str2double(s{1}{1})])')
        elseif ~isempty(s{2})
          set([app.DNPxX app.DNPxY app.DNFrX app.DNFrY],{'Value'},num2cell(str2double(s{2}{1}))')
        end

        

      end

      dbT = tic;

      % Medipix data are saved as a .mib file of varying bit-depth as unsigned integers of the next highest class
      %   (i.e. 12-bit is saved as a 16-bit unsigned integer) with big-endian ordering.
      % EMPAD data are saved as a .raw file with 32-bit depth with little endian ordering.
      % Fiji/ImageJ tend to save their files with big-endian ordering, though this is also system- and user-dependent.

      notes = "";  err = 0;
      app.ImpDataType.Items = {'Select Data Type';'8-bit Signed';'8-bit Unsigned';'16-bit Signed';'16-bit Unsigned'; ...
        '32-bit Real';'32-bit Signed';'32-bit Unsigned';'64-bit Real';'64-bit Signed';'64-bit Unsigned'};
      app.ImpDataType.ItemsData = {'unknown';'int8';'uint8';'int16';'uint16';'single';'int32';'uint32';'double'; ...
        'int64';'uint64'};
      app.T.dm = [];  app.T.h5 = [];
      set([app.DataOffset app.FrHead app.FrFoot],'Value',0)
      app.T.fileTail = 0;  app.ImpByteOrder.Value = 'l';  app.ImpDataType.Value = 'unknown';
      if event.Source == app.ImpFileSelect
          set(app.ImpSubImg,"Items",{},"Enable","off")
      end
      if isfile(app.ImpFilePath.Value)
        switch app.ImpFileTypeButtonGroup.SelectedObject
          case app.EMPADButton
            app.FrFoot.Value = 1024;  app.ImpDataType.Value = 'single';  app.DNPxX.Value = 128;  app.DNPxY.Value = 128;
            notes = sprintf('Pixels:\t128x128\n32-bit Real\n** EMPAD data have 1024-byte frame footers');
            guessFramesFromSize();
            getDimFromName(app.ImpFilePath.Value)
  
          case app.MedipixButton
            app.ImpDataType.Items = ["Select Data Type"; ["1 or 6";"12";"24"]+"-bit Padded Unsigned"];
            app.ImpDataType.ItemsData = {'unknown';'uint8';'uint16';'uint32'};
            fid = fopen(app.ImpFilePath.Value,'r');
            fmeta = strsplit(fread(fid, 128, 'uint8=>char')', ',');  
            if numel(fmeta) >= 7 && ismember(lower(fmeta{7}(1)), ["r", "u"]) % Signature character in header
              frewind(fid)
              fmeta = strsplit(fread(fid, str2double(fmeta{3}), 'uint8=>char')', ','); % Re-read with known header size
              dtype = lower(fmeta{7});  bitsize = str2double(fmeta(end-1));
              if dtype(1) == 'u'
                switch bitsize
                  case {1; 6}, app.ImpDataType.Value = 'uint8';
                  case 12, app.ImpDataType.Value = 'uint16';
                  case 24, app.ImpDataType.Value = 'uint32';
                end
              end
              app.FrHead.Value = str2double(fmeta{3});  app.ImpByteOrder.Value = 'b';
              app.DNPxX.Value = str2double(fmeta{5});  app.DNPxY.Value = str2double(fmeta{6}); 
              notes = sprintf(['Dim: X = %s, Y = %s\nData type: %s\nPixel depth: %d bit\n' ...
                'Frame header: %s bytes\nBig endian'], fmeta{5}, fmeta{6}, fmeta{7}, bitsize, fmeta{3});
              guessFramesFromSize();
              getDimFromName(app.ImpFilePath.Value)
            else
              notes = 'Unrecognizable as a Medipix/.mib file.';  err = -1;
            end
            fclose(fid);
  
          case app.MRCButton
            % Read in MRC header - first 1024 bytes
            fid = fopen(app.ImpFilePath.Value,'r');  fseek(fid,208,'bof');
            map = fread(fid, [1, 4], 'uint8=>char');
            if map == "MAP " % Signature characters
              e = fread(fid, 2, 'uint8'); % Bytes for Endianness
              if e(1) == 68 && ismember(e(2), [65, 68])
                app.ImpByteOrder.Value = 'l';  bo = 'Little Endian';
              elseif e(1) == 17 && e(2) == 17
                app.ImpByteOrder.Value = 'b';  bo = 'Big Endian';
              else
                bo = 'Unknown Endianness';
              end
              frewind(fid);
              dim = fread(fid,3,'uint32'); % X, Y and Z, only 3D
              app.DNPxX.Value = dim(1);  app.DNPxY.Value = dim(2);  app.DNFrX.Value = dim(3);
              guessFramesFromDimZ(dim(3))
              getDimFromName(app.ImpFilePath.Value)
    
              dtype = fread(fid,1,'uint32');
              switch dtype
                case 0, app.ImpDataType.Value = 'int8';  tnote = '8-bit Signed Integer';
                case 1, app.ImpDataType.Value = 'int16';  tnote = '16-bit Signed Integer';
                case 2, app.ImpDataType.Value = 'single';  tnote = '32-bit Real Float';
                case 3, tnote = '16-bit Complex Signed Integer, unsupported';
                case 4, tnote = '32-bit Complex Float, unsupported';
                case 6, app.ImpDataType.Value = 'uint16';  tnote = '16-bit Unsigned Integer';
                otherwise, tnote = 'Uknown data type';
              end
              app.DataOffset.Value = 1024;
              notes = sprintf('Dim: X = %d, Y = %d, Z = %d\n%s, %s\n** MRC files have a 1024-byte data offset', ...
                dim, tnote, bo);
            else
              notes = sprintf('Unrecognizable as MRC.\n\n"MAP " word missed.');  err = -1;
            end
            fclose(fid);
  
          case app.DM34Button
            % Read .dm3/4 tag values
            try app.T.dm = dmInfo(app.ImpFilePath.Value);catch;end
            if iscell(app.T.dm) && numel(app.T.dm) > 1
              % List all images' names in `app.ImpSubImg`
              pdim = zeros(numel(app.T.dm)-1, 1);
              app.ImpSubImg.Enable = 'on';
              for i = 1:numel(pdim)
                app.ImpSubImg.Items{i} = char(app.T.dm{i}.Name);
                pdim(i) = prod(cell2mat(app.T.dm{i}.Dimensions));
              end
              % Select sub-image with the largest dimension; unless manuel selected
              if event.Source == app.ImpSubImg
                app.ImpSubImg.Value = event.Value;
              else
                [~, i] = max(pdim);  app.ImpSubImg.Value = app.ImpSubImg.Items{i};
              end
              % Info of selected sub-image
              dm = app.T.dm{[strcmp(app.ImpSubImg.Items, app.ImpSubImg.Value), false]};
              finfo = app.T.dm{end};
              % Read dimensions
              dims = dm.Dimensions;
              for i = 1:4, if i > numel(dims), dims{i} = 1; end; end % Fill missing dimensions as 1
              set([app.DNPxX app.DNPxY app.DNFrX app.DNFrY],{'Value'},dims)
              % Find offset, file tail, data type, byte-order of dataset
              app.DataOffset.Value = dm.Data.offset;  try app.ImpDataType.Value = dm.Data.dataType; catch;end
              app.T.fileTail = finfo.fileSize - dm.Data.offset - dm.Data.size;
              if dm.ImageDataType.pixel ~= "scalar" % If pixels are not scalars (e.g. complex image)
                app.ImpDataType.Value = 'unknown';
              end
              % Is it little endian?
              if finfo.liEndian
                app.ImpByteOrder.Value = 'l';  bo = 'Little Endian';
              else
                app.ImpByteOrder.Value = 'b';  bo = 'Big Endian';
              end
              
              notes = sprintf("Dim: X = %d, Y = %d, Z = %d, W = %d\nDM%d, %s\nData-type: %s\n" ...
                +"Selected sub-image's offset is %d bytes.", ...
                dims{:}, finfo.version, bo, dm.ImageDataType.full, dm.Data.offset);
    
              if dims{4} == 1, guessFramesFromDimZ(dims{3}); end
            else
              notes = "Read DM file error: "+app.T.dm;  err = -1;
            end
  
          case app.HDF5Button
            try
              app.T.h5 = h5datasets(app.ImpFilePath.Value);
            catch
              notes = 'Read HDF5 file error';  err = -1;
            end
            
            if ~err
              app.ImpSubImg.Enable = 'on';
              % Select sub-image with the 1st largest dimension; unless manuel selected
              if event.Source ~= app.ImpSubImg
                  % List all images' names in `app.ImpSubImg`
                  pdim = zeros(numel(app.T.h5)-1, 1);
                  for i = 1:numel(pdim)
                      app.ImpSubImg.Items{i} = char(app.T.h5(i).Name);
                      pdim(i) = prod(app.T.h5(i).Dataspace.Size);
                  end
                  [~, i] = max(pdim);
                  app.ImpSubImg.Value = app.ImpSubImg.Items{i};
              end
              % Info of selected sub-image
              h5i = app.T.h5([strcmp(app.ImpSubImg.Items, app.ImpSubImg.Value), false]);
              % Read dimensions
              dims = h5i.Dataspace.Size;
              for i = 1:4, if i > numel(dims), dims(i) = 1; end; end % Fill missing dimensions as 1
              set([app.DNPxX app.DNPxY app.DNFrX app.DNFrY],{'Value'},num2cell(dims)')
              % Find offset, file tail, data type, byte-order of dataset
              if h5i.offset == -1
                app.DataOffset.Value = 0;  noteoffs = 'This dataset is not "contiguous", thus data offset is unknown.';
              else
                app.DataOffset.Value = h5i.offset;  noteoffs = "Selected dataset's offset is "+h5i.offset+" bytes.";
              end
              app.T.fileTail = app.T.h5(end).size - app.DataOffset.Value - h5i.size;
              if ~isempty(h5i.type), app.ImpDataType.Value = h5i.type;  end % If data type is unknown
              if endsWith(h5i.byte_order, "_BE")
                app.ImpByteOrder.Value = 'b';  bo = 'Big Endian';
              else
                app.ImpByteOrder.Value = 'l';  bo = 'Little Endian';
              end
    
              notes = sprintf("Dim: X = %d, Y = %d, Z = %d, W = %d\n%s, %s\n%s", dims, bo, h5i.Datatype.Type, noteoffs);
              if dims(4) == 1, guessFramesFromDimZ(dims(3)); end
            end
  
          otherwise %case app.CustomButton
            getDimFromName(app.ImpFilePath.Value)
            app.ImpDataType.Value = 'single';
            notes = "Custom import";
  
        end
      else
        notes = "File path is invalid";  err = -1;
      end
      
      app.ImpFileMetaNotes.Value = notes;
      if app.ImpDataType.Value == "unknown" &&  err ~= -1
        notifDLG(app, 'warn', "The data type indicated in the file's metadata is not supported/recognized.", ...
          'Invalid Data Type!');
      end

      debugToc(app, event, "", dbT)
      % Reset import range selections
      rangeImportExport(app, struct("Source",app.DNPxX,"EventName",[]));
      rangeImportExport(app, struct("Source",app.DNFrX,"EventName",[]));
      importBoxInput(app, event)
        end

        % Callback function: DNFrX, DNFrY, DNPxX, DNPxY, DataOffset,
        % FrFoot, 
        % ...and 27 other components
        function importBoxInput(app, event)
      dbT = tic;
      app.ImpEstFilesize.Text = '';  notes = "";  dfrn_evt = event;  real_evt = event;
      if isfile(app.ImpFilePath.Value)
        % Update Diffraction and Real-space import ranges; use dummy event if source is not a range UI
        if ~contains(event.Source.Tag, "Dfrn"), dfrn_evt = struct('Source',app.IPxD,'Value',app.IPxD.Value); end
        if ~contains(event.Source.Tag, "Real"), real_evt = struct('Source',app.IFrD,'Value',app.IFrD.Value); end
        [dnote,~,~,np,~] = rangeImportExport(app, dfrn_evt);
        [rnote,~,~,nf,~] = rangeImportExport(app, real_evt);
        notes = dnote+rnote;
        % Enable/Disable Range UIs
        set(app.ImportPxRangeGrid.Children,'Enable', app.ImpPxPart.Value)
        set(app.ImportFrRangeGrid.Children,'Enable', app.ImpFrPart.Value)
        % Current dataset dimensions
        irng = [np nf]; 
        % Allow for virtual memory mapping in some situations
        if app.FrHead.Value == 0 && app.FrFoot.Value == 0 ...
            && (~app.HDF5Button.Value || app.DataOffset.Value) ...
            && app.ImpByteOrder.Value == app.C.SysEndian && ~contains(app.ImpDataType.Value,'int') ...
            && isequal([app.DNPxX.Value app.DNPxY.Value app.DNFrX.Value app.DNFrY.Value], irng)
          app.ImpMemType.Enable = 'on';
        else
          app.ImpMemType.Enable = 'off';
          app.ImpMemType.Value = "Physical Memory";
        end
        % Calculate dataset size and memory usage
        if app.ImpDataType.Value ~= "unknown"
          byte_size = app.ByteSize.(app.ImpDataType.Value);
          app.T.EstSize = app.DataOffset.Value + app.T.fileTail ...
            + (app.FrHead.Value+app.DNPxX.Value*app.DNPxY.Value*byte_size+app.FrFoot.Value) ...
            * app.DNFrX.Value*app.DNFrY.Value;
          app.ImpEstFilesize.Text = sprintf('%d bytes, %.1f GiB',app.T.EstSize,app.T.EstSize/1024^3);
  
          if contains(app.ImpDataType.Value,'int')
            if byte_size > 4, f = 'double'; else, f = 'single'; end
            byte_size = app.ByteSize.(f);
            notes = notes+"\nDataset will be converted into "+byte_size*8+"-bit Real.";
          end
          notes = notes+"\nImport by "+app.ImpMemType.Value+"\n"+checkMem(np,nf,byte_size);
          notes = notes+"\n\n"+checkGPUMEM(np,nf);
        end
        % Allow to swap dataset/keep parameters if the dimensions are identical
        app.ImpKeepP.Enable = ~isempty(app.D) && isequal(irng, [app.D.NPxX app.D.NPxY app.D.NFrX app.D.NFrY]);
        if ~app.ImpKeepP.Enable, app.ImpKeepP.Value = 0; end
        if app.ImpKeepP.Value
          notes = notes+"\n\nSwapping dataset - keep current setups/alignments etc.";
        end
      end
      
      app.ImpNotes.Value = sprintf(notes);

      debugToc(app, event, "", dbT)


      %%% Sub functions
      function notes = checkMem(np,nf,byte_size)
        % Display estimated size in green if matches actual size, brown if smaller, red if larger
        if app.T.EstSize == app.T.FileSize
          app.ImpEstFilesize.FontColor = [0 0.5 0];
        elseif app.T.EstSize < app.T.FileSize
          app.ImpEstFilesize.FontColor = [0.5 0.5 0];
        else
          app.ImpEstFilesize.FontColor = 'r';
        end

        % Estimate the amount of memory needed to hold the largest arrays in memory
        % Estimate of the distance to the far corner of the diffraciton pattern
        est_mem = prod([np nf]) ...           % app.Data
          + prod(nf)*size(0:0.5:floor(sqrt(sum((np/2).^2))),2) ...   % app.Image.IntgAnn
          + prod(nf)*10 + prod(np)*2  ...    % app.Image
          + prod(np)*10;                        % app.Mask

        app.T.EstMem = est_mem*byte_size;

        notes = sprintf("Estimated memory usage: %.3f GiB.",app.T.EstMem/1024^3);
        if app.T.EstMem > app.C.MemTot
          msg = sprintf("WARNING: Size of dataset is larger than the system memory!");
          notifDLG(app,'error', msg, 'Size Exceeds System Memory!');
          notes = notes+"\n"+msg;
        end
        notes = notes+"\nSystem byte order: "+app.C.EndianTxt.(app.C.SysEndian)+".";
      end

      function gpu_note = checkGPUMEM(np,nf)
        igpu = app.ImpGPU.Value;
        if ~igpu
          gpu_note = 'GPU disabled.';
        elseif prod([np nf]) > intmax('int32')
          gpu_note = 'GPU disabled, because dataset has more elements than MATLAB CUDA''s maximum (2^31-1).';
          app.ImpGPU.Value = 0;
        else
          tgpu = sprintf('GPU %d. %s %.1f GiB', igpu, app.C.GPU(igpu).name, app.C.GPU(igpu).mem/1024^3);
          try
            if ~parallel.gpu.GPUDevice.getDevice(igpu).DeviceSelected, gpuDevice(igpu); end
            amem = parallel.gpu.GPUDevice.getDevice(igpu).AvailableMemory;
            % If GPU is already in use, taking the current data size into account
            if isfield(app.D, "GPU") && app.D.GPU == app.ImpGPU.Value
              try amem = amem + app.D.EstMem; catch; end
            end
            amem_t = sprintf('%.3f GiB', amem/1024^3);  wt = [];
            if app.T.EstMem > amem - 128*1024^2 % Has 128 MiB extra?
              gpu_note = tgpu+" has NOT enough free memory ("+amem_t+"). 128 MiB EXTRA free memory is also required.";
              wt = 'GPU Not Enough Free Memory!';
              app.ImpGPU.Value = 0;
            elseif app.T.EstMem > amem - 512*1024^2 % Has 512 MiB extra?
              gpu_note = tgpu+" has LIMITED free memory ("+amem_t+") and may cause errors.";
              wt = 'GPU Limited Free Memory!';
            else
              gpu_note = tgpu+" has enough free memory ("+amem_t+") for the selected dataset.";
            end
            % Notify warnings if any
            if ~isempty(wt), notifDLG(app,'warn', gpu_note, wt); end
          catch ME
            gpu_note = sprintf('Failed to select %s!\n%s\n%s\n%s',tgpu,ME.identifier,ME.message,ME.Correction);
            notifDLG(app,'error', gpu_note, 'Error Selecting GPU!');
            app.ImpGPU.Value = 0;
          end
        end
      end
        end

        % Callback function: AutoSaveImg, SaveDir, SaveDirButton, 
        % ...and 11 other components
        function saveCallbacks(app, event)
      dbT = tic;
      updatePrefix() % Try to update image name prefix
      
      switch event.Source
        case app.ShowSaveWdw
          figure(app.Fig.Save)
          % Trigger tab change callbacks defined in `@app.exportCallbacks()`
          mockUICallbacks(app,app.SaveTabGroup);
        case app.SaveDirButton
          dir = uigetdir(app.SaveDir.Value, 'Select Directory to Save Images');
          drawnow
          figure(app.Fig.Save)
          if dir, app.SaveDir.Value = dir; end
        case app.SaveDir
        case {app.SaveImgPrefix app.SavePrfxRi app.SavePrfxRo}
        case app.SaveImgList % Save image list selection change
          % If user selects all of the images in the list, tick the "Save All" checkbox
          app.SaveImgSelectAll.Value = numel(app.SaveImgList.Value) == numel(app.SaveImgList.Items);
        case {app.AutoSaveImg app.SaveExport} % Save images/Auto-save images or Export data
          if app.SaveDir.Value == "" || isempty(app.SaveDir.Value)
            notifDLG(app,'warn',sprintf("Please specify the directory!"),'Directory Missing'); 
          else
            % Create directory if not exists
            [s, msg] = mkdir(app.SaveDir.Value);
            if ~s
              notifDLG(app,'warn',sprintf("Failed to create directory!\n\n"+msg),'Directory Error'); 
            else
              % Save images if called from `app.AutoSaveImg` or currently the `app.SaveImgTab` is selected
              if app.SaveTabGroup.SelectedTab == app.SaveImgTab || event.Source == app.AutoSaveImg
                saveImages(); % Save images
              else
                exportCallbacks(app, event) % Export data
              end
            end
          end
        case app.SaveImgSelectAll % Select all/none
          if event.Value
            app.SaveImgList.Value = app.SaveImgList.ItemsData;
          else
            app.SaveImgList.Value = {};
          end
        case {app.SaveImgPNG app.SaveImgPNGAnnot} % Enable/Disable PNG options
          app.SaveImgPNGAnnot.Enable = app.SaveImgPNG.Value;
          set([app.SaveImgAnnotDPI app.SaveImgAnnotDPILabel],'Enable',app.SaveImgPNGAnnot.Value && app.SaveImgPNG.Value)
      end

      debugToc(app, event, "", dbT)


      %%% Sub functions
      % Update Image name prefix
      function updatePrefix()
        if isStaticEvt(event)
          % If not in any annular mode, disable the inner/outer radii prefix
          set([app.SavePrfxRi app.SavePrfxRo],'Enable',ismember(app.DetrMode.Value,["AnnMod" "CoMMod" "DPCMod"]))
          if ~app.SavePrfxRi.Enable, set([app.SavePrfxRi app.SavePrfxRo],'Value',0); end
          % Include inner and outer annular radii
          ang = "";  ri = "";  ro = "";
          if app.SavePrfxRi.Value, ri = ""+round(app.AnnRi_NF.Value,2); end
          if app.SavePrfxRo.Value, ro = ""+round(app.AnnRo_NF.Value,2); end
          if all([ri ro] ~= ""), ang = "-"; end
          ang = ri+ang+ro;
          if ang ~= "", ang = ang+app.DCUnit.Value+"_"; end
  
          app.SaveImgList.Items = app.SaveImgPrefix.Value + ang + app.SaveImgList.ItemsData;
          if app.DetrMode.Value == "DPCMod"
            app.SaveImgList.Items = replace(app.SaveImgList.Items, "CoM", "DPC");
          end
        end
      end

      function saveImages()
        % Give the user a progress bar in case it takes some time to save
        app.T.progDLG = progDLG(app, 'Saving image(s) ...', "Image Saving");

        % Save as 32-bit unscaled, uncompressed Tiff images
        tagstruct = struct('PlanarConfiguration',Tiff.PlanarConfiguration.Chunky,'Compression',Tiff.Compression.None, ...
          'SampleFormat',Tiff.SampleFormat.IEEEFP,'Photometric',Tiff.Photometric.MinIsBlack,'BitsPerSample',32);

        for id = reshape(string(app.SaveImgList.Value),1,[])
          imgfile = fullfile(app.SaveDir.Value, app.SaveImgList.Items{app.SaveImgList.ItemsData == id});

          if app.SaveImgPNG.Value
            if app.SaveImgPNGAnnot.Value
              print(app.Fig.(id), imgfile, '-dpng', "-r"+num2str(app.SaveImgAnnotDPI.Value))
            else
              imgd = app.ImgD.(id);
              imwrite(ind2rgb(round(255*imgd.CData)+1,app.Axes.(id).Colormap).*imgd.AlphaData, [imgfile '.png'])
            end
          end

          if app.SaveImgTIF.Value
            if id == "DfrnMask" && app.DetrMode.Value == "DPCMod"
              % Save all mask segments into a TIFF stack
              for j = 1:app.NRung.Value
                for i = 1:app.NSeg.Value
                  im = uint8(reshape(app.Mask.Seg(app.NSeg.Value*(j-1)+i, :), app.D.NPx))';
                  imwrite(im, [imgfile '.tif'], 'WriteMode','append');
                end
              end
            elseif id == "DfrnMask" && app.DetrMode.Value == "CoMMod"
              im = uint8(app.Mask.Ann)';
              imwrite(im, [imgfile '.tif']);
            else
              % Other images (and "DiffractionMask" from `app.Image.DfrnMask` for other Detector Modes)
              t = Tiff([imgfile '.tif'], 'w');
              im = app.Image.(id)';
              [tagstruct.ImageLength, tagstruct.ImageWidth] = size(im);
              tagstruct.SamplesPerPixel = size(im,3);
              t.setTag(tagstruct);
              t.write(single(im));
              t.close();
            end
          end
        end

        delete(app.T.progDLG);
      end
        end

        % Callback function: EFrD, EFrD, EFrX1, EFrX1, EFrY1, EFrY1, ENFrX,
        % 
        % ...and 21 other components
        function exportCallbacks(app, event)
      dbT = tic;  
      
      switch event.Source
        case app.SaveCloseButton % Close button on Save/Export Window
          delete(findobj(app.G.ImgAx,'-regexp','Tag','Export .... ROI')) % Try to remove Export ROIs
          app.SaveCloseButton.BackgroundColor = app.C.BgC; % Reset button color
          app.Fig.Save.Visible = 'off';
        case {app.SaveTabGroup app.ExpPxPart app.ExpFrPart} % Tab change or enable/disable partial export
          delete(findobj(app.G.ImgAx,'-regexp','Tag','Export .... ROI')) % Try to delete old ROIs
          if ~isempty(app.D), updateExpRange(); end % Try to update export range
          if app.SaveTabGroup.SelectedTab == app.ExportTab && app.Fig.Save.Visible
            % To start Export Data Mode
            app.SaveExport.Text = "Export Data";
            % Draw ROIs & add listening functions for live updates
            for id = app.G.ImgID(app.G.ImgSp ~= "ColorWheel" & app.G.ImgTyp ~= "Mask")
              app.A.Export.(id) = drawrectangle(app.Axes.(id),'Position',[1 1 0 0],'Color',"y", ...
                'Deletable',0,'FaceAlpha',0,'FaceSelectable',0);
              app.A.Export.(id).Tag = "Export "+app.Axes.(id).UserData.space+" ROI";
              app.A.Export.(id).UserData.Move = addlistener(app.A.Export.(id),'MovingROI',@moveExpAnnot);
              addlistener(app.A.Export.(id),'ROIMoved',@moveExpAnnot);
            end
            % Update ROIs
            exportCallbacks(app, struct("Source",app.EPxX1,"EventName","ValueChanged","Value",app.EPxX1.Value))
            exportCallbacks(app, struct("Source",app.EFrX1,"EventName","ValueChanged","Value",app.EFrX1.Value))
            % Show/Hide ROIs and enable/disable UIs if (not) selecting whole ranges
            set(findobj(app.G.DfrnAx, 'Tag','Export Dfrn ROI'), 'Visible', app.ExpPxPart.Value)
            set(findobj(app.G.RealAx, 'Tag','Export Real ROI'), 'Visible', app.ExpFrPart.Value)
            set(app.ExportFrRangeGrid.Children,'Enable', app.ExpFrPart.Value)
            set(app.ExportPxRangeGrid.Children,'Enable', app.ExpPxPart.Value)
            % Color the close button to hint/link with the ROIs
            if app.ExpPxPart.Value || app.ExpFrPart.Value, c = 'y'; else, c = app.C.BgC; end
          else
            % For "Save Images"
            app.SaveExport.Text = "Save Images";  c = app.C.BgC;
          end
          app.SaveCloseButton.BackgroundColor = c;
        case {app.ExpDimSuff app.ExpFormat app.ExpByteOrder}
          updateExpRange();
        case app.SaveExport % Export Button
          [pd,px1,py1,npx,npy,px2,py2,fd,fx1,fy1,nfx,nfy] = updateExpRange();
          try
            exportData();
          catch ME
            try delete(app.T.progDLG); catch; end
            try delete(app.T.efile); catch; end
            try app.Data = reshape(app.Data, app.D.NPxS, []);  catch; end % Reshape dataset to 2D
            enableWindows(app,true)
            rethrow(ME)
          end
      end

      debugToc(app, event, "", dbT)


      %%% Sub functions of `exportControls()`
      % Update Export Data boundaries as user change the Export Data Annotations
      function moveExpAnnot(~, evt)
        dbT = tic;
        exportCallbacks(app,evt)
        debugToc(app, evt, "", dbT)
      end
      
      function [pd,px1,py1,npx,npy,px2,py2,fd,fx1,fy1,nfx,nfy] = updateExpRange()
        dfrn_evt = event;  real_evt = event;
        % Update Diffraction and Real-space export ranges; use dummy event if source is not a range UI
        if ~contains(event.Source.Tag, "Dfrn"), dfrn_evt = struct('Source',app.EPxD,'Value',app.EPxD.Value); end
        if ~contains(event.Source.Tag, "Real"), real_evt = struct('Source',app.EFrD,'Value',app.EFrD.Value); end
        [dnote,pd,p1,np,p2] = rangeImportExport(app, dfrn_evt);
        [rnote,fd,f1,nf, ~] = rangeImportExport(app, real_evt);
        % Store parameters for file export
        px1 = p1(1);  py1 = p1(2);  npx = np(1);  npy = np(2);  px2 = p2(1);  py2 = p2(2);
        fx1 = f1(1);  fy1 = f1(2);  nfx = nf(1);  nfy = nf(2);
        % Add dimension suffix
        app.ExpFilename.Value = regexprep(app.ExpFilename.Value, '_\d*x\d*x\d*x\d*$', ''); % Remove old suffix
        if app.ExpDimSuff.Value
          app.ExpFilename.Value = sprintf('%s_%dx%dx%dx%d', app.ExpFilename.Value, np, nf);
        end
        % Export summary notes
        filenote = sprintf("Directory: '%s'\nFilename: '%s.%s'", ...
          app.SaveDir.Value, app.ExpFilename.Value, app.ExpFormat.Value);
        if app.ExpFormat.Value == "h5", filenote = filenote+sprintf("\nDataset: '/STEM4D'"); end
        notes = dnote+rnote;
        notes = notes+"\nData Type: "+app.D.DataType+" (was "+app.T.prev_D.DataType+" in original file)";
        notes = notes+"\nByte Order: "+app.C.EndianTxt.(app.ExpByteOrder.Value)+" (was " ...
          +app.C.EndianTxt.(app.T.prev_D.ByteOrder)+" in original file)";
        notes = notes+"\nSystem Byte Order: "+app.C.EndianTxt.(app.C.SysEndian);
        notes = notes+sprintf('\nEstimated file size: %.3f GiB', prod([np nf])*app.D.ByteSize/1024^3);
        notes = notes+sprintf('\nAvailable space: %.3f GiB', java.io.File(app.SaveDir.Value).getUsableSpace/1024^3);
        app.ExpNotes.Value = filenote+sprintf("\n\n"+notes);
      end
      
      % Function to export data
      function err = exportData()
        err = 0;
        app.T.efile = fullfile(app.SaveDir.Value, app.ExpFilename.Value+"."+app.ExpFormat.Value);
        if isfile(app.T.efile)
          notifDLG(app,'warn',"File: '"+app.T.efile+"' already exists!",'File Exists!');
          return
        end
        % Local variables
        dtype = app.D.DataType;  frsize = npx*npy*app.D.ByteSize;  b_order = app.ExpByteOrder.Value;
        % Progress window with per-second-updating `timer`
        [app.T.progDLG, app.T.tmr] = progImportExport(app, "Export", nfx*nfy, frsize);
        % Make dataset 4D
        app.Data = reshape(app.Data, [app.D.NPx app.D.NFr]);

        if app.ExpFormat.Value == "h5"
          % Sort out the h5 data type string; e.g. H5T_IEEE_F32LE, H5T_IEEE_F32BE, H5T_IEEE_F64LE, H5T_IEEE_F64BE
          h5dt = "H5T_IEEE_F"+app.ByteSize.(dtype)*8+upper(b_order)+"E";
          % C-like array indices for H5 low-level APIs
          fid = H5F.create(app.T.efile);  type_id = H5T.copy(h5dt);
          file_space_id = H5S.create_simple(4, [nfy nfx npy npx], []);
          mem_space_id = H5S.create_simple(2, [npy npx], []);
          dcpl = H5P.create('H5P_DATASET_CREATE');
          H5P.set_chunk(dcpl, [1 1 npy npx]);
          dset_id = H5D.create(fid, '/STEM4D', type_id, file_space_id, dcpl);
          %         H5D.write(dset_id,'H5ML_DEFAULT','H5S_ALL','H5S_ALL','H5P_DEFAULT', ...
          %           data(px1:px2, py1:py2, fx1:fx2, fy1:fy2));  % Whole data in one go
          % One frame at a time
          for efy = 0:nfy-1
            for efx = 0:nfx-1
              if ~isvalid(app.T.progDLG), err = -1; break; end % Break when progress windows closed
              app.T.frameJ(1) = efy*nfx + efx + 1; % Update processed Frame Number for progress update
              H5S.select_hyperslab(file_space_id, 'H5S_SELECT_SET', [efy efx 0 0], [], [], [1 1 npy npx]);
              frame = gather(app.Data(px1:px2, py1:py2, fx1+efx*fd, fy1+efy*fd)); % Selected frame
              if pd > 1, frame = squeeze(sum(reshape(frame, [pd npx pd npy]), [1 3]),'omitnan'); end % Pixel Binning
              H5D.write(dset_id, 'H5ML_DEFAULT', mem_space_id, file_space_id, 'H5P_DEFAULT', frame);
            end
            if err == -1, break; end
          end
          % Close created handles
          H5D.close(dset_id);  H5S.close(mem_space_id);  H5S.close(file_space_id);  H5T.close(type_id);
          H5P.close(dcpl);  H5F.close(fid);

        elseif app.ExpFormat.Value == "raw"
          fid = fopen(app.T.efile,'w');
          % One frame at a time
          for efy = 0:nfy-1
            for efx = 0:nfx-1
              if ~isvalid(app.T.progDLG), err = -1; break; end % Break when progress windows closed
              app.T.frameJ(1) = efy*nfx + efx + 1; % Update processed Frame # for progress update
              frame = gather(app.Data(px1:px2, py1:py2, fx1+efx*fd, fy1+efy*fd)); % Selected frame
              if pd > 1, frame = squeeze(sum(reshape(frame, [pd npx pd npy]), [1 3]),'omitnan'); end % Pixel binning
              fwrite(fid, frame, dtype, b_order);
            end
            if err == -1, break; end
          end
          fclose(fid);
        end
        delete(app.T.progDLG); % Close progress window
        app.Data = reshape(app.Data, app.D.NPxS, []); % Make dataset 2D again
        
        if err
          app.T.progDLG = progDLG(app,"Deleting the canceled export file ...","Export Canceled");
          delete(app.T.efile);  % Delete created file, if export canceled
          delete(app.T.progDLG)
        else
          notifDLG(app,'help',"Export to '"+app.T.efile+"' finished!",'Export Finished!');
        end
        enableWindows(app,true)
      end
        end

        % Value changed function: RotDfrn, RotReal, RvsXDfrn, RvsXReal, 
        % ...and 4 other components
        function axeDirCallbacks(app, event)
      % Function to flip/rotate image axes
      dbT = tic;

      sp = event.Source.Tag; % Space, "Real" or "Dfrn"
      adir = ["normal" "reverse"]; % For axis direction
      % Get X/Y-axis direction and rotation options of diffraction/real-space
      rvsx = struct('Dfrn',app.RvsXDfrn.Value,'Real',app.RvsXReal.Value);
      rvsy = struct('Dfrn',app.RvsYDfrn.Value,'Real',app.RvsYReal.Value);
      rot = struct('Dfrn',app.RotDfrn.Value,'Real',app.RotReal.Value);
      % Set axis directions and rotations of either diffraction or real-space images
      set(app.G.(sp+"Ax"),'XDir',adir(rvsx.(sp)+1), 'YDir',adir(rvsy.(sp)+1), 'View',[rot.(sp), 90])
      if sp == "Real" % Sync ColorWheel with real-space axes direction
        set(app.Axes.ColorWheel,{'XDir' 'YDir' 'View'},get(app.Axes.Real,{'XDir' 'YDir' 'View'}));
      end
      % X/Y labels of axis annotations
      lbl = struct('x',struct('Dfrn',"kx",'Real',"rx"),'y',struct('Dfrn',"ky",'Real',"ry"));
      % Update axis annotations
      arrayfun(@(x) drawAxeDir(x,sp), app.G.(sp+"ID"));

      debugToc(app, event, "", dbT)
      
      
      % Sub function to draw the axis annotations
      function drawAxeDir(id,sp)
        fig = app.Fig.(id);  cx = 'r';  cy = 'g';  % Colors of X/Y axes
        % Draw annotations on `figure`
        %         delete(findall(fig,'-depth',2,'Tag','AxeDir')) % Always delete old and draw new annotations
        if isempty(findall(fig,'-depth',2,'Tag','AxeDir')) || ~isfield(fig.UserData, 'AxAnnot')
          fig.UserData.AxAnnot = [];
          if sp == "Dfrn", drawAxeDir(id,"Real"); end % Draw scan directions on Diffraction images
          xa = annotation(fig,'arrow');  xt = annotation(fig,"textbox","String",lbl.x.(sp));
          ya = annotation(fig,'arrow');  yt = annotation(fig,"textbox","String",lbl.y.(sp));
          set([xa ya],'LineWidth',1,'HeadLength',3,'HeadWidth',3,'HeadStyle','plain')
          set([xt yt],'FontWeight','bold','HorizontalAlignment','center','VerticalAlignment','middle')
          set([xa; ya; xt; yt],'Units',"pixels","PickableParts",'no',"Tag","AxeDir",{'Color'},{cx;cy;cx;cy})
          fig.UserData.AxAnnot = [xa; ya; xt; yt; fig.UserData.AxAnnot]; % Scan direction annot at 5:8 for "Dfrn"
          uistack(fig.UserData.AxAnnot,'bottom')
        end
        % Set annotaion positions/directions
        %  `l`/`t`: length for arrow/total; `xy`: [arrow origin, arrow X, arrow Y, label X, label Y] positions; 
        l = 4;  t = 12;  xy = [-t -t; l -t; -t l; t -t; -t t];  
        % `offset`: offset from bottom-left; `xyf`: X/Y flip; `R`: axes rotation (clockwise)
        offset = 22;  xyf = 1-[rvsx.(sp) rvsy.(sp)]*2;  R = rotMatD(-rot.(sp));
        posAxeDir(fig.UserData.AxAnnot(1:4), offset*[1 1], xy.*xyf*R)
        set(fig.UserData.AxAnnot(1:4),'Visible',app.("Show"+sp+"Axes").Value)
        
        % Set scan directions on Diffraction patterns
        if sp == "Dfrn"
          l = 1;  t = 9;  xy = [-t -t; l -t; -t l; t -t; -t t];
          Rscan = rotMatD(app.ScanDir.Value);  syf = 1-[0 app.ScanDirYFlip.Value]*2;
          posAxeDir(fig.UserData.AxAnnot(5:end), offset*[2.8 1], xy.*syf*Rscan.*xyf*R)
          % Warning color if scan directions not aligned
          if ~isfield(app.P,'ScanDirInit') || ~app.P.ScanDirInit, cx = app.C.WarnC;  cy = cx; end
          % Only visible when: 1) show Dfrn annot AND 2) not during scan direction alignment AND 3) in CoM/DPC modes
          set(fig.UserData.AxAnnot(5:8),{'Color'},{cx;cy;cx;cy}, 'Visible', app.ShowDfrnAxes.Value ...
            && ~app.ScanDirUnlock.Value && any(app.DetrMode.Value == ["CoMMod" "DPCMod"]))
        end

        % Sub sub function to update annotation positions
        function posAxeDir(annot,offset,xy)
          % Arrow position, xap/yap: [ Origin XY, Vector XY ]; Label position, xtp/ytp: [ Center XY, width, height ]
          xap = [offset+xy(1,:), xy(2,:)-xy(1,:)];  xtp = [offset+xy(4,:), 0, 0];
          yap = [offset+xy(1,:), xy(3,:)-xy(1,:)];  ytp = [offset+xy(5,:), 0, 0];
          set(annot,{'Position'},{xap; yap; xtp; ytp})
        end
      end
        end

        % Callback function: DispBrightness, DispBrightness, 
        % ...and 24 other components
        function displayCallbacks(app, event)
      dbT = tic;

      id = app.DispImage.Value;  u = app.Axes.(id).UserData;  src = event.Source;
      % Initial contrast will be set as the total range of min:max
      % A change in contrast will expand or contract the width of the range
      % Initial brightness will be also set as the total range of min:max
      % A change in brightness will result in shift of the range up or down
      % Initial gamma is set to 1
      % A change in gamma will result in a powerlaw change in contrast I' = I^gamma
      switch src
        case app.HistLog % Log-scale option of histogram
          if app.HistLog.Value, app.HistAxes.YScale = 'log'; else, app.HistAxes.YScale = 'linear'; end
        case app.DispLock % Lock "current" image
          % Change dropdown color if locked
          if event.Value, c = [1 .8 .5]; else, c = app.C.BgC;  end
          app.DispImage.BackgroundColor = c;
        case app.DispVecField, u.vecField = event.Value; % Vector field
        case app.DispVecColor % Vector field color
          % Vector field color
          c = uisetcolor(u.vecColor);
          if isequal(c, 0), return; end % Early return if canceled
          u.vecColor = c;
        case app.DispCMap, u.colormap = event.Value; % Colormap
          cmap = str2func(u.colormap);  cm = cmap();
          if u.invert, cm = flipud(cmap()); end  % Whether to invert colormap
          colormap(app.Axes.(id), cm)
        case app.DispCMapInvert, u.invert = event.Value; % Invert colormap
        case app.DispBrightnessReset, u.brightness = 50; % Reset brightness
        case app.DispContrastReset, u.contrast = 50; % Reset contrast
        case app.DispGammaReset, u.gamma = 1; % Reset gamma
        case {app.DispBrightness_NF app.DispBrightness}, u.brightness = event.Value; % Brightness
        case {app.DispContrast_NF app.DispContrast}, u.contrast = event.Value; % Contrast
        case {app.DispGamma app.DispGamma_NF}, u.gamma = event.Value; % Gamma
        case {app.DispMaskOpa app.DispMaskOpa_NF}, u.maskOpa = event.Value; % Mask opacity
        otherwise   % E.g. app.DispImage
          % Update GUIs by values stored in `app.Axes.(id).UserData` for the current selected image
          figure(app.Fig.(id)) % Bring selected image to front
          set([app.DispVecField app.DispCMap app.DispCMapInvert],{'Value'},{u.vecField;u.colormap;u.invert})
          app.DispVecColor.BackgroundColor = u.vecColor;
          % Enable vector field UIs if: 1) in CoM/DPC mode AND 2) real-space image selected
          set([app.DispVecField app.DispVecFieldLabel app.DispVecColor],'Enable', ...
            ismember(app.DetrMode.Value, ["CoMMod" "DPCMod"]) && u.space == "Real")
          % Disable brightness/contrast/colormap UIs if: (CoM/DPC) "Phase" and "ColorWheel for Phase" images
          set([findobj(app.DispContrastsGrid.Children,'-not','type','uibutton');app.DispCMap;app.DispCMapInvert], ...
            'Enable', ~contains(u.name, "Phase"));
          % Disable mask opacity UIs if: ColorWheel/Mask/Preview images selected
          set([app.ShowMaskWdw app.DispMaskOpa_NF app.DispMaskOpa], ...
            'Enable',u.space ~= "ColorWheel" && ~ismember(u.type, ["Mask" "Preview"]))
      end
      % Update UI
      setExSrc(event,[app.DispBrightness_NF app.DispBrightness],'Value',u.brightness)
      setExSrc(event,[app.DispContrast_NF app.DispContrast],'Value',u.contrast)
      setExSrc(event,[app.DispGamma_NF app.DispGamma],'Value',u.gamma)
      setExSrc(event,[app.DispMaskOpa_NF app.DispMaskOpa],'Value',u.maskOpa)
      % Update image
      app.Axes.(id).UserData = u; % Update properties stored by the `axes`
      plotImage(app, event, id); % Re-plot image
      
      debugToc(app, event, "", dbT)
        end

        % Callback function: FrameX, FrameX, FrameY, FrameY, RealROIInvert,
        % 
        % ...and 1 other component
        function realSpaceROICallbacks(app, event)
      dbT = tic;

      switch event.Source
        case app.UpdateImages % Update diffraction image
          if isempty(findobj(app.G.RealAx, 'Tag','Real-space ROI')) % Draw ROI etc if not exists
            mockUICallbacks(app, app.RealROIShape)
          else
            moveRealROI(app.A.RealROI.Real, event)
          end
        case app.RealROIShape
          val = app.RealROIShape.Value;
          if val == "file"
            app.Image.RealROIFile = importMask(app, "Real");
            if isempty(app.Image.RealROIFile), val = "full"; end
          end
          app.RealROIShape.Value = val;  % Update GUI if changed
          % Panel enable/disable
          set([app.RealSpacePosGrid.Children;app.FramePosLabel], "Enable", val == "point")
          app.RealROIInvert.Enable = val ~= "full";
          app.RealROIInvert.Value = app.RealROIInvert.Value && app.RealROIInvert.Enable; % If disabled, then off
          % Draw ROIs
          drawRealROI(val);
        case {app.FrameX app.FrameY}
          moveRealROI(event.Source, event)
        otherwise
          % run the listener to update any/all other ROIs and the diffraction pattern
          moveRealROI(app.A.RealROI.Real, event)
      end

      debugToc(app, event, "", dbT)


      %% Sub functions
      % function to draw Real-space ROI of various shapes on real space image(s)
      function drawRealROI(typ)
        delete(findobj(app.G.RealAx, 'Tag','Real-space ROI')) % Delete all previous ROIs
        c = [1 .5 .5];
        % Special case for drawing polygon ROI
        if typ == "poly"
          % List for available real-space images
          rs = app.G.ImgSp == "Real" & app.G.ImgTyp ~= "Mask" & ismember(app.G.ImgID,app.DispImage.ItemsData);
          sel = notifDLG(app,'list',sprintf("Select a Real-space Image to draw a polygon ROI.\n\n" + ...
            "Press 'Esc' to cancel during drawing. Please refer to MATLAB's 'drawpolygon' for more tips.\n"), ...
            "Draw Polygon ROI",app.G.ImgNm(rs));
          % Revert to "full" is canceled
          if isempty(sel), mockUICallbacks(app, app.RealROIShape, "full");  return; end
          % Bring selected image window to front
          opt = app.G.ImgID(rs);  id = opt(sel);  ax = app.Axes.(id);  figure(app.Fig.(id))
          enableWindows(app,false) % Disable UIs until drawing finishes
          app.Fig.(id).UserData.grayout.Visible = 'off'; % Enable the selected image only
          % Draw temporary polygon for positions
          tmpPoly = drawpolygon(ax,"Color",c);  polyPos = tmpPoly.Position;  delete(tmpPoly)
          enableWindows(app,true) % Re-enable all windows
          % Revert to "full" is canceled
          if isempty(polyPos), mockUICallbacks(app, app.RealROIShape, "full");  return; end
        end
        % Draw ROIs on Real-space images, except the mask image
        rg = range([app.Axes.Real.XLim; app.Axes.Real.YLim]');  p = [app.FrameX.Value app.FrameY.Value];
        for id = app.G.ImgID(app.G.ImgSp == "Real" & app.G.ImgTyp ~= "Mask")
          switch typ
            case "full"
              roi = drawrectangle(app.Axes.(id),"Position",[1 1 rg],"Visible",0,"EdgeAlpha",0,"FaceAlpha",0);
            case 'point'
              roi = drawpoint(app.Axes.(id),"Position",p);
            case 'ellipse'
              roi = drawellipse(app.Axes.(id),'Center',p,"SemiAxes",min(0.1*rg)*[1 1],'FaceAlpha',0);
            case 'rectangle'
              roi = drawrectangle(app.Axes.(id),"Position",[p-0.1*rg, 0.2*rg],"Rotatable",true,'FaceAlpha',0);
            case 'poly'
              roi = drawpolygon(app.Axes.(id),"Position",polyPos,'FaceAlpha',0);
            case "file"
              roi = drawrectangle(app.Axes.(id),"Position",[1 1 rg],"Visible",0,"EdgeAlpha",0,"FaceAlpha",0);
              bw = visboundaries(app.Axes.(id), bwboundaries(app.Image.RealROIFile'), 'Color',c, ...
                "EnhanceVisibility",0);
              bw.Tag = 'Real-space ROI';
          end
          set(roi,'Deletable',false,'Color',c,'Tag','Real-space ROI');
          roi.UserData.Move = addlistener(roi,'MovingROI',@moveRealROI);
          addlistener(roi,'ROIMoved',@moveRealROI);
          app.A.RealROI.(id) = roi;
        end

        moveRealROI(app.A.RealROI.Real, event)
      end


      % live update function for Real-space ROIs
      function moveRealROI(src, evt)
        dbT = tic;
        % Update panel values for individual probe positions
        roi = app.A.RealROI.Real;  x = app.FrameX.Value;  y = app.FrameY.Value;
        switch src
          case app.FrameX, x = max(1,evt.Value); % Force X >= 1
          case app.FrameY, y = max(1,evt.Value); % Force Y >= 1
          otherwise % E.g. ROIs
            roi = src;
            switch app.RealROIShape.Value
              case {'rectangle', 'full', 'file'}
                pos = src.Position(1:2)+0.5*src.Position(3:4);
                x = pos(1);  y = pos(2);
              case 'point'
                x = src.Position(1);  y = src.Position(2);
              case 'ellipse'
                x = src.Center(1);  y = src.Center(2);
              case 'poly'
                [x, y] = centroid(polyshape(src.Position));
            end
        end
        x = round(x);  y = round(y);
        % Set current ROI position if called from `app.FrameX` or `app.FrameY`, and it's a point ROI
        if ismember(src, [app.FrameX app.FrameY]) && app.RealROIShape.Value == "point", roi.Position = [x y]; end
        % Update UI
        setExSrc(evt,[app.FrameX app.FrameY],{'Value'},{x;y})
        % Only upate ROIs on other visible figures; update all when not in "changing" Event
        rois = structfun(@(i) i, app.A.RealROI);
        rois = rois(arrayfun(@(i) ancestor(i,'figure').Visible, rois) | isStaticEvt(evt));
        % Sync existing properties of positions etc.
        for p = ["Position" "Center" "SemiAxes" "RotationAngle"]
          if isprop(roi, p), setExSrc(evt, rois, p, roi.(p)); end
        end
        % Update images
        if toUpdateImage(app,evt)
          % generate a mask for displaying diffraction pattern
          switch app.RealROIShape.Value
            case "full", mask_real = true(app.D.NFr);
            case 'point', mask_real = false(app.D.NFr);  mask_real(x, y) = true;
            case 'file', mask_real = app.Image.RealROIFile;
            otherwise, mask_real = createMask(src, app.ImgD.Real)';
          end
          mask_real = cast(mask_real,app.D.DataType); % Convert to single/double
          if app.RealROIInvert.Value, mask_real = max(mask_real,[],'all') - mask_real; end  % Invert mask?
          app.Image.RealMask = mask_real; % Store the mask for plotting/saving
          % Update diffraction pattern for the specified ROI
          app.Image.Dfrn = gather(reshape(app.Data*reshape(mask_real,[],1), app.D.NPx)/sum(mask_real,'all'));
          plotAllPatterns(app, evt)
        end

        debugToc(app, evt, "", dbT)
      end
        end

        % Value changed function: DetrMode
        function detectorModeCallbacks(app, event)
      dbT = tic;  dmod = app.DetrMode.Value;  
      enableWindows(app,false) % Enable windows
      clearDetectors(); % Clear ROIs on Diffraction
      % Clear Real-space images if not switching to alignment or preview
      if ~ismember(dmod, ["AlignMod" "PrvwMod"])
        delete(findobj(app.G.RealAx(~contains({app.G.RealAx.Tag},"Mask")),'Type','image')); 
      end
      % Enable/Disable CoM/DPC related GUI/images
      set(app.G.CoM_btns,"Enable", any(dmod == ["CoMMod" "DPCMod"])); % Buttons 
      if ismember(dmod, ["CoMMod" "DPCMod"])
        app.DispImage.Items = app.G.ImgNm;  app.DispImage.ItemsData = app.G.ImgID;
        % Subsitute "CoM"/"DPC" in image names, window titles and button texts
        t1 = extractBefore(dmod, 4);
        app.DispImage.Items = replace(app.G.ImgNm, ["CoM" "DPC"], t1);
        set(app.G.ImgFig, {'Name'},cellstr(app.DispImage.Items)')
        set(app.G.CoM_btns,{'Text'},cellstr(replace(get(app.G.CoM_btns,'Text'), ["CoM" "DPC"], t1)))
      else
        app.DispImage.Items = app.G.ImgNm(app.G.ImgTyp ~= "CoM"); % Image dropdown texts
        app.DispImage.ItemsData = app.G.ImgID(app.G.ImgTyp ~= "CoM"); % Image dropdown values
        set(app.G.ImgFig(app.G.ImgTyp == "CoM"), 'Visible', 'off') % Image windows
      end
      
      % Show primary diffraction/real-space image when mode changes unless in Preview mode
      set([app.Fig.Dfrn; app.Fig.Real],'Visible',dmod ~= "PrvwMod")
      % Special case for Import Preview Mode
      if dmod == "PrvwMod"
        % Keep only "Preview" image
        app.DispImage.Items = "Preview";  app.DispImage.ItemsData = "Preview";
        % Hide other UIs
        set([app.MiscTab app.InfoTab app.ExportTab],'Parent',[])
        set([app.Fig.Preview app.Fig.Import app.Fig.Settings],'Visible','on')
      else
        app.P.DetrMode = app.DetrMode.Value; % Note current mode
        % Keep no "Preview" image
        logi = app.DispImage.ItemsData == "Preview";
        app.DispImage.Items(logi) = [];  app.DispImage.ItemsData(logi) = [];  app.Fig.Preview.Visible = 'off';
        % Show all UIs
        set([app.MiscTab app.InfoTab],'Parent',app.SettingsTabGroup)
        set(app.ExportTab,'Parent',app.SaveTabGroup)
      end
      
      % Define images in the saving list
      app.SaveImgList.Items = app.DispImage.ItemsData;
      app.SaveImgList.ItemsData = app.SaveImgList.Items;
      mockUICallbacks(app,app.SaveImgPrefix)  % Update Image saving prefix
      mockUICallbacks(app,app.ShowDfrnAxes) % Update diffraction axis annotations
      
      % Set detector size when transmitted beam is aligned the first time
      if isfield(app.P,'TransBeamInit') && ~app.P.TransBeamInit && dmod ~= "AlignMod"
        set([app.AnnRi app.AnnRo app.VrApR],{'Value'},{app.TBR.Value; (app.TBR.Value + app.P.RMax)/3; app.TBR.Value})
        app.P.VrApXY = app.B0;
        app.P.TransBeamInit = 1;
      end

      set(app.G.DetrUI,'Visible','off');  % Diffraction detector UI
      app.MathTab.Parent = []; % Math Tab
      switch dmod
        case "PrvwMod"
          app.PreviewGrid.Visible = 'on';
          previewCallbacks(app,event)
        case "AlignMod"
          app.AlignmentGrid.Visible = 'on';
          transBeamCallbacks(app,event)
        case {"AnnMod", "CoMMod", "DPCMod"}
          app.AnnDetrGrid.Visible = 'on';
          annularDetectorCallbacks(app, event)
          if dmod ~= "AnnMod" % 'CoMMod' OR 'DPCMod'
            plotImage(app, event, 'ColorWheel') % Plot ColorWheel
            figure(app.Fig.CoMPhMag);  figure(app.Fig.ColorWheel)
            if ~app.P.ScanDirInit
              flashBackground(app, app.ScanDirGrid); % Flashing to align scan direction
            end
          end
        case "VrApMod" % 'Virtual Aperture'
          app.VirtualApertureGrid.Visible = 'on';
          virtualApertureCallbacks(app, event);
        case "CustMod"
          app.CustomDetectorGrid.Visible = 'on';  app.MathTab.Parent = app.SettingsTabGroup;
          customDetectorCallbacks(app, event)
          figure(app.Fig.DfrnMask)
      end

      debugToc(app, event, "", dbT)
      
      
      %% Sub function
      % Function to delete plotted detectors if they exist
      function clearDetectors()
        % Transmitted Beam alignment
        delete(findobj(app.Axes.Dfrn,'Tag','TransBeamAnnot'))
        % Annular/Round detectors and Segmented detectors
        delete(findobj(app.Axes.Dfrn,'-regexp','Tag','AnnDetrAnnot'))
        delete(findobj(app.Axes.Dfrn,'Tag','SegDetrAnnot'))
        % Virtual apertures
        delete(findobj(app.Axes.Dfrn,'Tag','VrApertAnnot'))
        % Custom detectors
        % Hide Custom ROIs only
        set(findobj(app.Axes.Dfrn.Children,'-regexp','Tag',"Custom "),'Visible',0);
        % Scan direction alignment
        delete(findobj(app.Axes.Dfrn,'Tag','ScanDirAnnot'))
      end
        end

        % Value changed function: DCPos, DCSys, DCUnit
        function detrCoordCallbacks(app, event)
      % "Polar" and "Absolute" are mutually exclusive
      switch event.Source
        case app.DCSys, if app.DCSys.Value == "Polar", app.DCPos.Value = "Relative"; end
        case app.DCPos, if app.DCPos.Value == "Absolute", app.DCSys.Value = "Cartesian"; end
        case app.DCUnit
      end
      % Update coordinate conversion related convenient global properties
      app.DfPxR = 1;  app.RB0 = [0 0];
      if app.DCUnit.Value == "mrad", app.DfPxR = app.mradPx.Value; end
      if app.DCPos.Value == "Relative", app.RB0 = app.B0; end
      % Update UI
      switch app.DetrMode.Value
        case "AlignMod"
        case {'AnnMod' 'DPCMod' 'CoMMod'}
          annularDetectorCallbacks(app,struct("Source",app.DCSys,"EventName","UpdateCoord"))
        case "VrApMod"
          virtualApertureCallbacks(app,struct("Source",app.DCSys,"EventName","UpdateCoord"))
        case "CustMod"
          customDetectorCallbacks(app,struct("Source",app.DCSys,"EventName","UpdateCoord"))
      end
        end

        % Button pushed function: SwapByteOrder, SwapDfrnXY, SwapRealXY
        function datasetOptCallbacks(app, event)
      switch event.Source
        case app.SwapByteOrder % Swap byte-order
          msg = "Swapping byte order ...";
          app.T.progDLG = progDLG(app, sprintf("\n%s\n",msg), "Byte Order Swap");
          try
            app.Data = swapbytes(app.Data);
          catch
            if app.D.GPU
              waitbar(0,app.T.progDLG,msg+sprintf("\nIt seems GPU has not enough memory.\nUsing CPU for this process ..."))
              app.Data = gather(app.Data);
              app.Data = swapbytes(app.Data);
              app.Data = gpuArray(app.Data);
            else
              delete(app.T.progDLG)
              notifDLG(app,'error',"It seems the system has not enough memory for this process! " + ...
                "Maybe try to increase system's virtual memory.", "Out of Memory")
              return
            end
          end
          bo = struct('l',"b",'b',"l");  app.D.ByteOrder = bo.(app.D.ByteOrder); % update data info at `app.D.ByteOrder`
          app.DataInfo.Value = getImportInfo();
          mockUICallbacks(app,app.UpdateImages)
          delete(app.T.progDLG)
          sel = notifDLG(app,'quest',"Is the current byte-order correct?",'Byte Order Swap',["Yes","No. Revert"]);
          % Run the process again if selected "No ....."
          if startsWith(sel,"No")
            datasetOptCallbacks(app,struct('Source',app.SwapByteOrder,'EventName',""))
          end

        case {app.SwapDfrnXY app.SwapRealXY}
          % Diffraction or real-space
          if event.Source.Tag == "Dfrn"
            U = "Px"; 
          else
            % Delete all Real-space ROIs;  
            U = "Fr";  delete(findobj(app.G.RealAx, 'Tag','Real-space ROI'));  app.P.TransBeamInit = 1;
          end
          % Swap X/Y dimensions
          [app.D.("DN"+U+"X"), app.D.("DN"+U+"Y")] = swap(app.D.("DN"+U+"X"), app.D.("DN"+U+"Y"));
          [app.D.("N"+U+"X"), app.D.("N"+U+"Y")] = swap(app.D.("N"+U+"X"), app.D.("N"+U+"Y"));
          [app.D.(U+"X1"), app.D.(U+"Y1")] = swap(app.D.(U+"X1"), app.D.(U+"Y1"));
          app.D.("N"+U) = flip(app.D.("N"+U));
          % Re-prepare the imported data
          importCallbacks(app,event)
          app.DataInfo.Value = getImportInfo();
          
        case app.PreviewButton
          sel = checkNaN(app, app.Image.Preview,1); % Check data NaN/Inf, without asking to sway byte-order
          if strcmp(sel,'Set NaNs to 0')
              app.Data(isnan(app.Data(:)))=0;
          end

        otherwise
          app.DataInfo.Value = getImportInfo();
          % Check data NaN/Inf, ask whether to sway byte-order
          sel = checkNaN(app, app.Image.Dfrn,0);
          if strcmp(sel,'Set NaNs to 0')
              app.Data(isnan(app.Data(:)))=0;
          end

      end
      

      %% Sub functions
      % Function to swap values
      function [b,a] = swap(a,b); end
      
      % Function to update current data info
      function notes = getImportInfo()
        d = app.D;  d0 = app.T.prev_D;
        notes = "File: "+replace(d.filePath,"\","\\");
        if ~isempty(d.subImg), notes = notes+"\nSub-dataset: "+d.subImg; end
        notes = notes+"\n\n# Current Data Info #";
        notes = notes+"\nByte Order: "+app.C.EndianTxt.(d.ByteOrder)+"\nData Type: "+d.DataType ...
          +"\nByte Size: "+app.ByteSize.(d.DataType)+" bytes";
        notes = notes+sprintf("\n%s size (X×Y): %d×%d","Diffraction",d.NPx,"Real-space",d.NFr);
        notes = notes+"\n\n# Data Structure in File #";
        notes = notes+"\nData Offset: "+d0.Offset+" bytes\nFrame Header: "+d0.FrHead ...
          +" bytes\nFrame Footer: "+d0.FrFoot+" bytes";
        notes = notes+"\nByte Order: "+app.C.EndianTxt.(d0.ByteOrder)+"\nData Type: "+d0.DataType ...
          +"\nByte Size: "+app.ByteSize.(d0.DataType)+" bytes";
        notes = notes+"\n\n# File Meta Info Notes #\n"+strjoin(d0.NoteFileMeta,'\n');
        notes = notes+"\n\n# Import Option Notes #\n"+strjoin(d0.NoteImp,'\n');
        notes = sprintf(notes);
      end
        end

        % Callback function: PreviewButton, PvBC, PvBL, PvBR, PvCC, PvCL, 
        % ...and 6 other components
        function previewCallbacks(app, event)
      switch event.Source
        case app.DetrMode % Entering mode
          cla(app.Axes.Preview);  app.Image.Preview = []; % Clear previous preview
          enableWindows(app,true) % Enable windows
          
        case app.UpdateImages % Update image
          mockUICallbacks(app,app.PreviewButton) % Preview
          
        case {app.PvFrX app.PvFrY} % Preview Frame X/Y
          event.Source.Value = max(event.Value, 1); % Force Frame X/Y minimum as 1
          mockUICallbacks(app,app.PreviewButton) % Preview
          
        case {app.PvBC app.PvBL app.PvBR app.PvCC app.PvCL app.PvCR app.PvTC app.PvTL app.PvTR} % Location buttons
          X = app.PvFrX.Limits(2);  Y = app.PvFrY.Limits(2); % Get limits from Frame X/Y UIs
          xy = min(ceil(eval(event.Source.Text)), [X Y]); % Evaluate the text on buttons
          set([app.PvFrX app.PvFrY],{'Value'},{xy(1);xy(2)}); % Set values of Frame X/Y UIs
          mockUICallbacks(app,app.PreviewButton) % Preview
          
        case app.PreviewButton
          cla(app.Axes.Preview);  
          % Get parameters
          importCallbacks(app,event);  d = app.T.Preview;  ifx = app.PvFrX.Value-1;  ify = app.PvFrY.Value-1;  
          if ~isempty(d)
            dnpx = d.DNPxX;  dnpy = d.DNPxY;  dnfx = d.DNFrX;  dnfy = d.DNFrY;
            app.P.PreviewAxLim = [0.51, dnpx + .49, 0.51, dnpy + .49];
            set(app.Axes.Preview, "XLim",app.P.PreviewAxLim(1:2), "YLim",app.P.PreviewAxLim(3:4));
            try
              if ~isempty(d.h5ds) % Preview HDF5
                fid = H5F.open(d.filePath);   dset_id = H5D.open(fid, d.h5ds);
                file_space_id = H5S.create_simple(4, [dnfy dnfx dnpy dnpx], []);
                mem_space_id = H5S.create_simple(2, [dnpy dnpx], []);
                % C-like array indices for H5 low-level APIs
                H5S.select_hyperslab(file_space_id, 'H5S_SELECT_SET', [ify ifx 0 0], [], [], [1 1 dnpy dnpx]); 
                frame = H5D.read(dset_id, 'H5ML_DEFAULT', mem_space_id, file_space_id, 'H5P_DEFAULT');
              else % Preview others
                fid = fopen(d.filePath,'r');
                % Move cursor to end of the to-be-read frame, for testing
                err = fseek(fid, d.Offset + (1 + ifx + ify*dnfx)*(d.FrHead + dnpx*dnpy*d.ByteSize + d.FrFoot), 'bof');
                if err == -1, throw(MException('','')); end
                % Move cursor to start of the to-be-read frame
                fseek(fid, -(dnpx*dnpy*d.ByteSize + d.FrFoot), 'cof');
                frame = fread(fid, [dnpx, dnpy], d.DataType, 0, d.ByteOrder);
              end
              app.Image.Preview = frame;
              plotImage(app,event,"Preview") % Plot image
              datasetOptCallbacks(app, event) % Check NaN
            catch
              notifDLG(app,'error',"Errors occurred during preview! Maybe reached end-of-file.", 'Error during Preview!');
            end
            % Close opened handles
            try
              if ~isempty(d.h5ds)
                H5S.close(mem_space_id);  H5S.close(file_space_id);  H5D.close(dset_id);  H5F.close(fid);
              else
                fclose(fid);
              end
            catch
            end
          end
      end
      
        end

        % Callback function: Alpha, TBAutoAlign, TBCrossAlign, TBR, TBR, 
        % ...and 11 other components
        function transBeamCallbacks(app, event)
      dbT = tic;
      switch event.Source
        case app.DetrMode % Entering mode
          % Create transmitted beam annotation, allow for disk as large as the entire diffraction pattern
          app.A.TransBeam = drawcircle(app.Axes.Dfrn,'Center',app.B0,'Radius',app.TBR.Value,'Color',"b",...
            'DrawingArea',"unlimited",'Deletable',0,'EdgeAlpha',.7,'FaceAlpha',0,'Tag','TransBeamAnnot');
          app.A.TransBeam.UserData.Move = addlistener(app.A.TransBeam,'MovingROI',@moveTransBeam);
          addlistener(app.A.TransBeam,'ROIMoved',@moveTransBeam);
          mockUICallbacks(app, app.DispImage, "Dfrn"); % Select `Dfrn` image
          % If this is the initializing alignment, then do swap byte check and auto-align
          if ~app.P.TransBeamInit
            datasetOptCallbacks(app, event);  autoAlign();
          end
          enableWindows(app,true) % Enable windows
        case app.UpdateImages % Update images
          % Create a summed image of all diffraction patterns simply for alignment and calibration
          app.Image.DfrnMask = ones(app.D.NPx,app.D.DataType);
          app.Image.Real = gather(reshape(reshape(app.Image.DfrnMask,1,[])*app.Data, app.D.NFr));
        case app.TBAutoAlign % Auto-align
          autoAlign();
        case app.TBCrossAlign % Align transmitted beam via two crossed lines
          crossAlign();
      end
      % Update dependent variables
      moveTransBeam(event.Source,event);

      debugToc(app, event, "", dbT)


      %% Sub functions
      % Function to sync UIs/ROIs depending on the central beam location
      function moveTransBeam(src,evt)
        b0 = [app.TBX.Value app.TBY.Value];  r = app.TBR.Value;  a = app.Alpha.Value;
        mrad_per_px = a/r;  np = app.D.NPx;
        if isempty(findobj(app.Axes.Dfrn,'Tag','TransBeamAnnot'))
          app.A.TransBeam = []; % If ROI is not plotted
        else
          switch evt.Source
            case {app.TBX app.TBX_NF}, b0(1) = max(1, evt.Value); % Force X >= 1
            case {app.TBY app.TBY_NF}, b0(2) = max(1, evt.Value); % Force Y >= 1
            case {app.TBR app.TBR_NF}, r = evt.Value; % Radius
              case app.Alpha, a = evt.Value;  mrad_per_px = a/r; app.annularStep.Value = mrad_per_px/2; % Calculate the diffraction scale
            case app.mradPx, mrad_per_px = evt.Value;  a = mrad_per_px*r; % Manually set the diffraction scale
            case app.A.TransBeam, b0 = src.Center;  r = src.Radius; % ROI
          end
        end
        % Restrict transmitted beam location/size
        b0(b0 > np) = np(b0 > np);
        b0(b0 < 1) = 1;
        app.B0 = b0;
        app.P.RMax = ceil(sqrt(sum((abs(app.P.DfCtr-b0)+app.P.DfCtr).^2))); % Find the max allowed radius
        r = min(r, app.P.RMax);
        % Update UI limits
        set([app.TBR app.TBR_NF],'Limits',[eps(), app.P.RMax])
        set([app.AnnRi app.AnnRo app.VrApR],'Limits',[0, app.P.RMax])
        % Update UI values
        setExSrc(evt, [app.TBR; app.TBX; app.TBY; app.TBR_NF; app.TBX_NF; app.TBY_NF; app.Alpha; app.mradPx], ...
          {'Value'},{r;b0(1); b0(2); r; b0(1); b0(2); a; mrad_per_px})
        % Update ROI
        set(app.A.TransBeam,'Center',b0,'Radius',r)
        % Update global coordnate properties
        detrCoordCallbacks(app, event)
      end

      % Auto-align transmitted beam
      function autoAlign()
        app.T.progDLG = progDLG(app, 'Finding transmitted beam ...', "Auto Alignment");
        % Reset any zoom on the transmitted beam
        axis(app.Axes.Dfrn, app.P.DfrnAxLim)

        % Align transmitted beam by trying to find the transmitted disk in the diffraction pattern (app.Image.Dfrn),
        % apply slight gaussaian blur of 5 pixels to help the fit if necessary
        try
          warning('off');
          [center, radius, ~] = imfindcircles(app.Image.Dfrn, [1 round(max(app.D.NPx)/2)]);
          if isempty(center)
            [center, radius, ~] = imfindcircles(imgaussfilt(app.Image.Dfrn,5), [1 round(max(app.D.NPx)/2)]);
          end
          warning('on');
        catch
          center = [];  radius = [];
        end
        center = fliplr(center);
        delete(app.T.progDLG); % Close the progress bar
        transBeam_old = [app.B0 app.TBR.Value]; % Store old transmitted beam values

        % Find circle closest to the center of the diffraction pattern, plot for user confirmation
        if isempty(center)
          notifDLG(app,'warn',"No transmitted beam detected. Please align the transmitted beam manually.", ...
            'Auto-align Failed');
          sel = "No. Revert";
        else
          % Assign radius and center value(s) found above using imfindcircles based on whichever is found to be
          % closest to the diffraction pattern center `app.P.DfCtr`
          [~,im] = min(sqrt(sum((center-app.P.DfCtr).^2,2)));
          app.TBX.Value = center(im,1);  app.TBY.Value = center(im,2);  app.TBR.Value = radius(im);
          % To update annotation/panel values
          transBeamCallbacks(app,struct("Source","","EventName",""));

          sel = notifDLG(app,'quest',"Is the auto-alignment correct?",'Auto-align',["Yes","No. Revert"]);
        end

        % Revert alignment if not correctly detected
        if sel == "No. Revert"
          app.TBX.Value = transBeam_old(1);  app.TBY.Value = transBeam_old(2);  app.TBR.Value = transBeam_old(3);
        end
      end

      % align transmitted beam at the crossing of two lines
      function crossAlign()
          app.A.line1 = drawline("Position",app.D.NPx.*[1 1;3 3]/4,"Color","r","Deletable",false);
          app.A.line2 = drawline("Position",app.D.NPx.*[1 3;3 1]/4,"Color","r","Deletable",false);

          addlistener(app.A.line1,'ROIMoved',@moveTB);
          addlistener(app.A.line1,'MovingROI',@moveTB);
          addlistener(app.A.line2,'ROIMoved',@moveTB);
          addlistener(app.A.line2,'MovingROI',@moveTB);

          h = helpdlg('Push OK when finished');
          uiwait(h);

          delete(app.A.line1)
          delete(app.A.line2)

 

          function moveTB(source,event)
              x1 = app.A.line1.Position(1,1);
              x2 = app.A.line1.Position(2,1);
              x3 = app.A.line2.Position(1,1);
              x4 = app.A.line2.Position(2,1);

              y1 = app.A.line1.Position(1,2);
              y2 = app.A.line1.Position(2,2);
              y3 = app.A.line2.Position(1,2);
              y4 = app.A.line2.Position(2,2);

              app.B0 = [x1*y2-x2*y1,x3*y4-x4*y3]/[y2-y1,y4-y3;-(x2-x1),-(x4-x3)];

              app.TBX.Value = app.B0(1);
              app.TBX_NF.Value = app.B0(1);
              app.TBY.Value = app.B0(2);
              app.TBY_NF.Value = app.B0(2);

              app.A.TransBeam.Center = app.B0;

          end
      end
        end

        % Callback function: AnnRLink, AnnRi, AnnRi, AnnRi_NF, AnnRi_NF, 
        % ...and 17 other components
        function annularDetectorCallbacks(app, event)
      dbT = tic;
      b0 = app.B0;  % Absolute pixel coordinates of central beam; only changes in `transBeamCallbacks()`
      dmod = app.DetrMode.Value; % Detector mode; when changed this callback will be called
      
      ii=1;
      images = {};
      event2 = {};

      switch event.Source
        case app.DCSys % Change coordinate options
          limitAnnUI() % UI limits
        case app.DetrMode % Entering current mode
          limitAnnUI() % UI limits
          app.ScanDirUnlock.Value = 0; % Lock scan directions first upon entering annular modes
          enableAnnUI() % UI enable/disable
          integrateAnnular() % Update annular integral mask
          drawAnnDetr(); % Draw detectors
          if dmod == "DPCMod", drawSegDetr(); end % Whether to draw segmented detectors
          moveAnnDetr(event.Source, event) % Update UI/ROIs
          enableWindows(app,true) % Enable windows
        case {app.AnnRi app.AnnRi_NF app.AnnRo app.AnnRo_NF app.AnnRLink app.DetRot app.DetRot_NF app.NSeg app.NRung ...
            app.ScanDir app.ScanDir_NF app.ScanDirYFlip app.UpdateImages}
          moveAnnDetr(event.Source, event) % Update UI/ROIs
        case app.ScanDirUnlock
          app.P.ScanDirInit = 1; % Flag scan directions as aligned
          enableAnnUI() % Enable/Disable GUI elements
          delete(findobj(app.Axes.Dfrn,'Tag','ScanDirAnnot')); % Try to remove existing scan direction ROIs
          if app.ScanDirUnlock.Value, drawScanDir(); end % Draw annotations
          mockUICallbacks(app,app.ShowDfrnAxes) % Update diffraction axes annotations
        case app.autoCurl
            tic
            minimizeCurl()
            toc
            moveAnnDetr(event.Source, event) % Update UI/ROIs
            minimizeCurl()
            moveAnnDetr(event.Source, event) % Update UI/ROIs
            toc
      end

      debugToc(app, event, "", dbT)


      %% Sub functions
      % Function to try to automatically find angle between diffraction
      % space and real space by minimizing center of mass curl
      function minimizeCurl()
            % find the curl for all angles
            CoM = zeros([2,fliplr(app.D.NFr)]);
            CoM(1,:,:) = app.Image.CoMX';
            CoM(2,:,:) = app.Image.CoMY';
            
            % set up angles
            %theta = reshape(0:359,[1,1,360]);
            theta = reshape(app.ScanDir.Value:app.ScanDir.Value+359,[1,1,360]);
            R_applied = [cosd(-app.ScanDir_NF.Value) -sind(-app.ScanDir_NF.Value);sind(-app.ScanDir_NF.Value) cosd(-app.ScanDir_NF.Value)];
            R = permute([cosd(theta) -sind(theta);sind(theta) cosd(theta)],[3,1,2]);
            % undo rotatation by ScanDir angle via R_applied
            rotCoM = tensorprod(R,tensorprod(R_applied,CoM,2,1),3,1);
            %rotCoM = tensorprod(R,CoM,3,1);
            [dFx_dx,dFx_dy] = gradient(permute(squeeze(rotCoM(:,1,:,:)),[2,3,1]));
            [dFy_dx,dFy_dy] = gradient(permute(squeeze(rotCoM(:,2,:,:)),[2,3,1]));
            cav = squeeze(mean(abs(0.5*(dFy_dx-dFx_dy)),[1,2],'omitnan'));
            div = squeeze(sum(dFx_dx + dFy_dy,[1,2],'omitnan'));
            % try transpose
            [dFx_dx,dFx_dy] = gradient(permute(squeeze(rotCoM(:,1,:,:)),[3,2,1]));
            [dFy_dx,dFy_dy] = gradient(permute(squeeze(rotCoM(:,2,:,:)),[3,2,1]));
            cav(:,2) = squeeze(mean(abs(0.5*(dFy_dx-dFx_dy)),[1,2],'omitnan'));
            div(:,2) = squeeze(sum(dFx_dx + dFy_dy,[1,2],'omitnan'));
            
%             figure;
%             % plot curl vs angle
%             subplot(2,2,1);hold on
%             plot(squeeze(theta),cav,'--')
%             colororder(["r" "b"])
%             box on
%             grid on
%             xlabel("angle (degrees)")
%             xlim([min(theta(:)),max(theta(:))])
%             title('curl')
%             axis("square")
%             
%             % plot divergence vs angle
%             subplot(2,2,2);hold on
%             plot(squeeze(theta),div,'--')
%             colororder(["r" "b"])
%             box on
%             grid on
%             xlabel("angle (degrees)")
%             xlim([min(theta(:)),max(theta(:))])
%             title('divergence')
%             axis("square")

            % refine theta value
            thetaIdx = find(cav==min(cav(:)));
            if numel(thetaIdx)>1
                [~,idx] = max(div(thetaIdx));
                thetaIdx = thetaIdx(idx);
            end
            [thetaIdx,transVal] = ind2sub(size(cav),thetaIdx);
            transVal = transVal - 1;
            thetaCoarse = theta(thetaIdx)-app.ScanDir.Value;
            theta = reshape(thetaCoarse-1:0.1:thetaCoarse+1,[1,1,21]);
            R = permute([cosd(theta) -sind(theta);sind(theta) cosd(theta)],[3,1,2]);
            rotCoM = tensorprod(R,CoM,3,1);
            if transVal==1
                [~,dFx_dy] = gradient(permute(squeeze(rotCoM(:,1,:,:)),[3,2,1]));
                [dFy_dx,~] = gradient(permute(squeeze(rotCoM(:,2,:,:)),[3,2,1]));
%                color = "b";
            else
                [~,dFx_dy] = gradient(permute(squeeze(rotCoM(:,1,:,:)),[2,3,1]));
                [dFy_dx,~] = gradient(permute(squeeze(rotCoM(:,2,:,:)),[2,3,1]));
%                color = "r";
            end
            cav = squeeze(mean(abs(0.5*(dFy_dx-dFx_dy)),[1,2],'omitnan'));
%            div = squeeze(sum(dFx_dx + dFy_dy,[1,2]));
            
%             subplot(2,2,3);
%             hold on;
%             plot(squeeze(theta+app.ScanDir.Value),cav,'-','LineWidth',1,'Color',color)
%             box on
%             grid on
%             xlabel("angle (degrees)")
%             xlim([min(theta(:)),max(theta(:))]+app.ScanDir.Value)
%             title('curl')
%             axis("square")
% 
%             subplot(2,2,4);
%             hold on;
%             plot(squeeze(theta+app.ScanDir.Value),div,'-','LineWidth',1,'Color',color)
%             box on
%             grid on
%             xlabel("angle (degrees)")
%             xlim([min(theta(:)),max(theta(:))]+app.ScanDir.Value)
%             title('divergence')
%             axis("square")
% 
             thetaVal = theta(cav==min(cav))+app.ScanDir.Value;
%             subplot(2,2,1);
%             plot(thetaVal,min(cav),'ko')
%             legend(["as-is";"transpose"])
%             subplot(2,2,3);
%             plot(thetaVal,min(cav),'ko')
%             subplot(2,2,2);
%             plot(thetaVal,div(cav==min(cav)),'ko')
%             legend(["as-is";"transpose"])
%             subplot(2,2,4);
%             plot(thetaVal,div(cav==min(cav)),'ko')

            app.ScanDir.Value = wrapTo180(thetaVal);
            app.ScanDir_NF.Value = wrapTo180(thetaVal);
            app.ScanDirYFlip.Value = xor(app.ScanDirYFlip.Value,transVal);
      end

      % Function to update Annular detector UI limits/labels when coordinate options change
      function limitAnnUI()
        set([app.AnnRi_NFLabel app.AnnRo_NFLabel],'Text',app.DCUnit.Value)
        set([app.AnnRi_NF app.AnnRo_NF],'Limits',[0 app.P.RMax*app.DfPxR],'Step',0.25*app.DfPxR)
      end
      
      % Function to enable/disable UI
      function enableAnnUI()
        set(app.SegDetrGrid.Children,'Enable',switchOnOff(dmod == "DPCMod")) % Enable segmented panel
        % Change Enable state of scan direction UIs, except `app.ScanDirUnlock`
        set(setdiff(app.ScanDirGrid.Children,app.ScanDirUnlock),'Enable',switchOnOff(app.ScanDirUnlock.Value))
        app.ScanDirUnlock.Enable = ismember(dmod, ["CoMMod" "DPCMod"]);
        % Highlight to align Scanning Direction
        if ismember(dmod, ["CoMMod" "DPCMod"]) && ~app.P.ScanDirInit, bc = app.C.WarnC; else, bc = app.C.BgC; end
        app.ScanDirGrid.BackgroundColor = bc; % Set scan direction panel color
      end
      
      % Function to live update annular/round/segmented detectors
      function moveAnnDetr(src, evt)
        ri = app.AnnRi.Value;  ro = app.AnnRo.Value;  dr = app.DetRot.Value;
        sd = app.ScanDir.Value;  syf = 1-2*app.ScanDirYFlip.Value;
        % Cases for different detectors
        if contains(src.Tag,'AnnDetr'), moveAnnR()
        elseif contains(src.Tag,'SegDetr'), moveSeg()
        elseif contains(src.Tag,'ScanDir'), moveScan()
        else % app.DetrMode app.UpdateImages
          moveAnnR();  if app.ScanDirUnlock.Value, moveScan(); end  % Update scan directions as well
        end
        % Whether to update images
        if toUpdateImage(app,evt)
          % Skip calculations of new BF/DF `app.Image.Real` if annular radii are not changed
          if isDiffToPrev(app,'AnnR',[ri ro]) || isStaticEvt(evt)
            % 2D matrix of distances from central beam, X/Y on the 1st/2nd dimensions
            mask_ann = sqrt( ((1:app.D.NPxX)-b0(1))'.^2 + ((1:app.D.NPxY)-b0(2)).^2 );
            mask_ann = mask_ann >= ri & mask_ann <= ro;
            app.Image.DfrnMask = mask_ann;  app.Mask.Ann = mask_ann;
            % The factors of 2 here are because the radial integration was done on a 1/2 pixel step.
            %   The plus 1 is because the array begins at 0, but is 1-indexed.
            app.Image.Real = gather(sum(app.Image.IntgAnn(:, :, round(ri*2)+1:round(ro*2)+1), 3,'omitnan'));
          end
          % CoM/DPC calculations; skip if parameters unchanged
          if ismember(dmod, ["CoMMod", "DPCMod"])
            if isDiffToPrev(app,'CoM_P',[ri ro sd syf dr]) || isStaticEvt(evt)
              calcCoM(ri, ro, sd, syf, dr);
            end
          end
          % Update images
          plotAllPatterns(app,evt)
        end

        % Sub sub functions
        % Sub sub function for annular radii
        function moveAnnR()
          scale = app.DfPxR;
          switch src
            case app.A.AnnInner, ri = evt.CurrentRadius;
            case app.A.AnnOuter, ro = evt.CurrentRadius;
            case app.AnnRi, ri = evt.Value;
            case app.AnnRo, ro = evt.Value;
            case app.AnnRi_NF, ri = evt.Value/scale;
            case app.AnnRo_NF, ro = evt.Value/scale;
            otherwise % {app.AnnRLink app.DetrMode app.UpdateImages}
              app.P.detWidth = ro - ri;
          end
          % If inner/outer detector radii are linked
          if app.AnnRLink.Value
            dw = app.P.detWidth;
            if contains(src.Tag,'RI'), ri = min(ri, app.P.RMax-dw);  ro = ri + dw;
            elseif contains(src.Tag,'RO'), ro = max(ro, dw);  ri = ro - dw;  end
          end
          % Restrict Inner/Outer radii
          if contains(src.Tag,'RI'), ri = max(0, min(ri, ro));
          elseif contains(src.Tag,'RO'), ro = min(max(ro, ri), app.P.RMax);  end
          % Update ROI
          set([app.A.AnnInner;app.A.AnnOuter],{'Radius'},{ri;ro})
          % Update UI with Limits check
          setExSrc(evt, [app.AnnRi; app.AnnRo; app.AnnRi_NF; app.AnnRo_NF], ...
            {'Value'},{ri; ro; min(ri*scale, app.P.RMax*scale); min(ro*scale, app.P.RMax*scale)});
          if isStaticEvt(evt)
            mockUICallbacks(app,app.SaveImgPrefix) % Update saving prefix
          end
          % Whether to update segments as well
          if dmod == "DPCMod", moveSeg(); end
        end

        % Sub sub function for segemented detector
        function moveSeg()
          switch src
            case {app.DetRot app.DetRot_NF}, dr = evt.Value;
            case app.A.SegDetrP0, rxy = (evt.CurrentPosition-b0);  dr = atan2d(rxy(2), rxy(1));
            case {app.NSeg app.NRung}, drawSegDetr();
          end
          % Update UI
          setExSrc(evt, [app.DetRot app.DetRot_NF],'Value',dr)
          % Update ROI
          pos0 = [ri, 0; ro, 0; (ri+ro)/2, 0]*rotMatD(dr)+b0;
          set([app.A.SegDetrL0 app.A.SegDetrP0],{'Position'},{pos0(1:2,:);pos0(3,:)});
          set(app.A.SegDetrCir,{'Radius'}, num2cell((1:app.NRung.Value-1)'/app.NRung.Value*(ro - ri) + ri))
          % Use 3D matrix for positions, then put the 1st/2nd dimensions (2x2 array) in each cell for each segment
          t = dr+360*(reshape(1:app.NSeg.Value,1,1,[])-.5)/app.NSeg.Value;
          set(app.A.SegDetrL,{'Position'},squeeze(num2cell([ri;ro].*[cosd(t) sind(t)]+b0, 1:2)))
        end

        % Sub sub function for scan directions
        function moveScan()
          % Use polar relative pixel coordinates for calculation
          svx = app.A.ScanDir.xc.Center - b0;  svy = app.A.ScanDir.yc.Center - b0;
          switch src
            case app.A.ScanDir.xc, svx = evt.CurrentCenter - b0;  sd = atan2d(svx(2), svx(1));
            case app.A.ScanDir.yc, svy = (evt.CurrentCenter - b0)*syf;  sd = -atan2d(svy(1), svy(2));
            case {app.ScanDir app.ScanDir_NF}, sd = evt.Value;
            case app.ScanDirYFlip
          end
          % Convert back to cartesian absolute pixel coordiantes for annotations
          [x1,y1] = pol2cart(deg2rad(sd), sqrt(sum(svx.^2)));  sp1 = [x1 y1]+b0;
          [x2,y2] = pol2cart(deg2rad(sd+90*syf), sqrt(sum(svy.^2)));  sp2 = [x2 y2]+b0;
          % Not limiting annotation positions
          set([app.A.ScanDir.xl app.A.ScanDir.yl],{'Position'},{[b0;sp1];[b0;sp2]})
          setExSrc(evt, [app.A.ScanDir.xc app.A.ScanDir.yc],{'Center'},{sp1;sp2})
          setExSrc(evt, [app.ScanDir app.ScanDir_NF],'Value',sd)
        end
      end

      % Function to draw annular/round/segmented detectors
      function drawAnnDetr()
        delete(findobj(app.Axes.Dfrn,'-regexp','Tag','AnnDetrAnnot'))
        % draw inner and outer circles
        app.A.AnnInner = drawcircle(app.Axes.Dfrn,"Center",b0,"Radius",1,"Color","r",'Tag','AnnDetrAnnot RI');
        app.A.AnnOuter = drawcircle(app.Axes.Dfrn,"Center",b0,"Radius",2,"Color",'m','Tag','AnnDetrAnnot RO');
        % add listenr for live update during user interaction
        addlistener([app.A.AnnInner app.A.AnnOuter],'MovingROI',@moveAnnDetr);
        u.Move = addlistener([app.A.AnnInner app.A.AnnOuter],'ROIMoved',@moveAnnDetr);
        set([app.A.AnnInner app.A.AnnOuter],"FaceAlpha",0,"FaceSelectable",0,"LineWidth",4, ...
          'DrawingArea',"unlimited","Deletable",0,"InteractionsAllowed","reshape",'UserData',u)
      end

      % Function to draw segemented annotations
      function drawSegDetr()
        delete(findobj(app.Axes.Dfrn,'Tag','SegDetrAnnot'))
        app.A.SegDetrCir = gobjects(app.NRung.Value-1,1);  app.A.SegDetrL = gobjects(app.NSeg.Value,1);
        % plot the lines between segments
        for i = 1:app.NSeg.Value
          app.A.SegDetrL(i) = drawline(app.Axes.Dfrn,"Position",[0 1; 0 1]+b0,"Color","b","LineWidth",2);
        end
        % Zero-degree line
        app.A.SegDetrL0 = drawline(app.Axes.Dfrn,"Position",[b0;b0],'Color','w','StripeColor','k',"LineWidth",1.5, ...
          'EdgeAlpha',.7);
        % plot the circles between rungs
        for i = 1:app.NRung.Value-1
          app.A.SegDetrCir(i) = drawcircle(app.Axes.Dfrn,"Center",b0,"Radius",1,'Color',"y",'LineWidth',2, ...
            "FaceAlpha",0,"FaceSelectable",false);
        end
        % Zero-degree point
        app.A.SegDetrP0 = drawpoint(app.Axes.Dfrn,"Position",b0,'Color','w', ...
          'LabelTextColor','w','LabelAlpha',0,'Label','0',"Deletable",0,'Tag','SegDetrAnnot');
        addlistener(app.A.SegDetrP0,'MovingROI',@moveAnnDetr);
        app.A.SegDetrP0.UserData.Move = addlistener(app.A.SegDetrP0,'ROIMoved',@moveAnnDetr);
        set([app.A.SegDetrL0;app.A.SegDetrCir;app.A.SegDetrL],"InteractionsAllowed","none",'Tag','SegDetrAnnot')
      end

      % Function to draw Scan Direction alignment annotations
      function drawScanDir()
        p1 = b0+[app.P.RMax/2 0];  p2 = b0+[0 app.P.RMax/2];
        app.A.ScanDir.xl = drawline(app.Axes.Dfrn,'Position',[b0;p1],'Color','r','LabelTextColor','r','Label','Scan X');
        app.A.ScanDir.yl = drawline(app.Axes.Dfrn,'Position',[b0;p2],'Color','g','LabelTextColor','g','Label','Scan Y');
        app.A.ScanDir.xc = drawcircle(app.Axes.Dfrn,'Center',p1,'Radius',app.TBR.Value);
        app.A.ScanDir.yc = drawcircle(app.Axes.Dfrn,'Center',p2,'Radius',app.TBR.Value);
        addlistener([app.A.ScanDir.xc app.A.ScanDir.yc],'MovingROI',@moveAnnDetr);
        u.Move = addlistener([app.A.ScanDir.xc app.A.ScanDir.yc],'ROIMoved',@moveAnnDetr);
        set([app.A.ScanDir.xc app.A.ScanDir.yc],'Color',[0 .5 1],'FaceAlpha',0,'UserData',u)
        set([app.A.ScanDir.xl app.A.ScanDir.yl],'MarkerSize',1,'LineWidth',1,'LabelAlpha',0,'InteractionsAllowed','none')
        set([app.A.ScanDir.xc app.A.ScanDir.yc app.A.ScanDir.xl app.A.ScanDir.yl],'Deletable',0, ...
          "DrawingArea","unlimited",'Tag','ScanDirAnnot')
        moveAnnDetr(event.Source, event)
      end

      % Annularly integrate the annular detector for the primary real-space pattern `app.Axes.Real`
      function integrateAnnular()
        dbT = tic; 
        % Rerun the annular integration based on the newly aligned location of the transmitted disk
        msg = "Generating radial masks (takes a while) ...";
        if isDiffToPrev(app,'B0',app.B0)
          app.T.progDLG = progDLG(app, sprintf("\n%s\n",msg), "Annular Integration");
          % Make pixel array for mask
          [ygrid, xgrid] = meshgrid(1:app.D.NPxY, 1:app.D.NPxX);
          % Integrate in app.annularStep (mrad) increments all the way out to the furthest corner; put these on the 3rd dimension
          dist = reshape(0:app.annularStep.Value/app.mradPx.Value:app.P.RMax, 1, 1, []);
          mask_ann = sqrt((xgrid-app.B0(1)).^2 + (ygrid-app.B0(2)).^2);
          mask_ann = reshape(mask_ann >= dist & mask_ann < dist+app.annularStep.Value/app.mradPx.Value, [], numel(dist))';
          mask_ann = cast(mask_ann,app.D.DataType);
          % Multiply data by the annular masks
          try
            app.Image.IntgAnn = reshape((mask_ann*app.Data)', app.D.NFrX, app.D.NFrY, []);
          catch ME
            if app.D.GPU
              waitbar(0,app.T.progDLG,msg+sprintf("\nIt seems GPU has not enough memory.\nUsing CPU for this process ..."))
              app.Image.IntgAnn = reshape((mask_ann*gather(app.Data))', app.D.NFrX, app.D.NFrY, []);
              try % Move the integrated images to GPU
                app.Image.IntgAnn = gpuArray(app.Image.IntgAnn); 
              catch
              end
            else
              delete(app.T.progDLG)
              notifDLG(app,'error',"It seems the system has not enough memory for this process! " + ...
                "Maybe try to increase system's virtual memory.", "Out of Memory")
              rethrow(ME)
            end
          end
          % Record previous transmitted disk location to see if the annular integration needs to be performed again
          delete(app.T.progDLG); % Close progress window
        end

        debugToc(app, [], "", dbT)
      end

      % Calculate the CoM images
      %   `ri` - annular inner radius `app.AnnRi.Value`; `ro` - outer radius `app.AnnRo.Value`
      %   `sd` - scan direction `app.ScanDir.Value`; `syf` - flip scan Y or not
      %   `dr` - detector rotation `app.DetRot.Value`
      function calcCoM(ri, ro, sd, syf, dr)
        dbT = tic;
        if ~isfield(app.Mask, "Ann"), return; end

        [CoMX, CoMY] = integrateCoM();
        app.Image.CoMX = CoMX;
        app.Image.CoMY = CoMY;
        % CoM magnitude is the length of the vector -- in mrad
        app.Image.CoMMag = sqrt(CoMX.^2+CoMY.^2);
        app.Image.CoMMagNorm = rescale(app.Image.CoMMag);
        % CoM angle was calculated from the arctangent of the difference images (CoMX and CoMY)
        app.Image.CoMPh = atan2(CoMY,CoMX);
        % Adjust atan2 range from [-pi/2:pi/2) to [0:2pi)
        app.Image.CoMPh(app.Image.CoMPh < 0) = app.Image.CoMPh(app.Image.CoMPh < 0) + 2*pi;
        app.Image.CoMPhMag = app.Image.CoMPh;

        % Make iCoM/iDPC and dCoM/dDPC images - based on maths from Lazic et al.,
        % (https://doi.org/10.1016/j.ultramic.2015.10.011)
        %         [ky, kx] = meshgrid(floor(-app.D.NFrY/2):floor(-app.D.NFrY/2)+app.D.NFrY-1, ...
        %           floor(-app.D.NFrX/2):floor(-app.D.NFrX/2)+app.D.NFrX-1);
        [ky, kx] = meshgrid((1:app.D.NFrY)-app.P.RsCtr(2), (1:app.D.NFrX)-app.P.RsCtr(1));

        kr = sqrt(kx.^2+ky.^2); % 1:20;   -10 .. 0 .. 9;   -9.5 .. 0  .. 9.5
        kr(kr == 0) = 1; % a zero pixel will mess up the maths here
        kx = fftshift(kx);  ky = fftshift(ky);  kr = fftshift(kr);
        % integrated center of mass
        app.Image.iCoM = real(ifft2(kx.*fft2(CoMX)./(2*pi*1j*kr.^2))+ifft2(ky.*fft2(CoMY)./(2*pi*1j*kr.^2)));
        % differential center of mass
        app.Image.dCoM = real(ifft2(2*pi*1i*kx.*fft2(CoMX)+2*pi*1i*ky.*fft2(CoMY)));

        debugToc(app, [], "", dbT)

        %% Sub sub function
        function [CoMX,CoMY] = integrateCoM()
          Rscan = rotMatD(sd);  Rdetr = rotMatD(dr);
          % Make pixel array for masks
          [ygrid, xgrid] = meshgrid(((1:app.D.NPxY)-b0(2))*syf, (1:app.D.NPxX)-b0(1));
          im_real = cast(reshape(app.Mask.Ann,1,[]),app.D.DataType)*app.Data;

          % switch between detector types (except annular/round)
          if dmod == "CoMMod"
            % Mask off diffraction pattern: less than outer angle & greater than inner angle
            CoM = zeros(app.D.NFrS, 2, 'like',app.Data);
            % Integrated mass of each diffraction pattern within the mask:
            % Center of Mass adjusted to the center of the diffraction pattern
            CoM(:,1) = cast(reshape(xgrid.*app.Mask.Ann,1,[]), app.D.DataType) * app.Data./im_real;
            CoM(:,2) = cast(reshape(ygrid.*app.Mask.Ann,1,[]), app.D.DataType) * app.Data./im_real;
            % Adjust for scan rotation
            CoM = CoM*Rscan;
          elseif dmod == "DPCMod"
            nrung = app.NRung.Value;  nseg = app.NSeg.Value;  rdist = ygrid.^2 + xgrid.^2;
            % Calculate the atan of all pixel positions within the image
            a = atan2d(ygrid,xgrid);                  % Get atan from -180 to 180
            a = a - dr;                               % subtract off any detector rotation applied
            a = a + 180/nseg;                         % shift atan by half of a segment span
            a(a < 0) = a(a < 0) + 360;                % shift the negative values of atan up by 360
            a(a >= 360) = a(a >= 360)-360;            % Get total range of atan from [0,360)
            % Preallocate a DPC/CoM vector image that will be the sum of all segments (i.e. DPC_A, DPC_B, ...)
            CoM_length = zeros(nrung*nseg,2,app.D.DataType);
            app.Mask.Seg = zeros(nrung*nseg,app.D.NPxS,'logical');
            for j = 1:nrung
              for i = 1:nseg
                % Define vectors k1 and k2 that correspond to the inner and outer angles of the detector for a given
                % number of rungs
                k1 = (j-1)*(ro-ri)/nrung+ri;
                k2 = (j)*(ro-ri)/nrung+ri;
                % less than outer angle & greater than/equal to inner angle & greater than the start of
                % the segment angle & less than the end of the segmenet angle
                app.Mask.Seg(nseg*(j-1)+i,:) = reshape( ...
                  rdist < k2^2 & rdist >= k1^2 & a >= (i-1)*360/nseg & a < (i)*360/nseg, [], 1);

                % Find center of mass of each segment in each rung, and adjust for scan and detector rotation
                t = (i-1)*360/nseg + dr;
                CoM_length(nseg*(j-1)+i,:) = 2*sind(360/nseg/2) / (3*360/nseg/2) ...
                  * (k1^3-k2^3)/(k1^2-k2^2) * [cosd(t) sind(t)] * Rscan * Rdetr;
              end
            end
            % integrated mass of each diffraction pattern within the mask:
            CoM = (app.Mask.Seg*app.Data./im_real)'*CoM_length;
          end
          % Convert to mrad and pull out x and y components of the CoM
          CoM = gather(reshape(CoM, [app.D.NFr 2])*app.mradPx.Value);
          CoMX = CoM(:,:,1);  CoMY = CoM(:,:,2);
        end
      end
        end

        % Callback function: VrApInvert, VrApMirrRot, VrApMirrRot, 
        % ...and 20 other components
        function virtualApertureCallbacks(app, event)
      dbT = tic;  b0 = app.B0;

      switch event.Source
        case app.DetrMode % Entering mode
          limitVrApUI() % Update UI limits
          enableVrApUI() % Enable/Disable UIs
          drawVrApAnnot() % Draw ROIs
          moveVrAp(event.Source, event) % Update ROI/UI
          enableWindows(app,true) % Enable windows
        case app.VrApMirror % Mirror enable/disable
          enableVrApUI() % Enable/Disable UIs
          drawVrApAnnot() % Draw ROIs
          moveVrAp(event.Source, event) % Update ROI/UI
        case app.VrApSymm % Symmetric option
          drawVrApAnnot() % Draw ROIs
          moveVrAp(event.Source, event) % Update ROI/UI
        case app.DCSys % Coordinate options
          limitVrApUI() % Update UI limits
          moveVrAp(event.Source, event) % Update UI coordinate values
        case {app.VrApReset app.VrApMirrRot app.VrApMirrRot_NF app.VrApInvert app.VrApR app.VrApR_NF ...
            app.VrApX app.VrApX_NF app.VrApY app.VrApY_NF app.VrApRotCCW app.VrApRotCW app.UpdateImages}
          moveVrAp(event.Source, event) % Update ROI/UI
      end

      debugToc(app, event, "", dbT)


      %% Sub functions
      % Function to update UI enable/disable states
      function enableVrApUI()
        % Enable/Disable mirror UIs, except `app.VrApMirror`
        set(setdiff(app.VrApMirrGrid.Children,app.VrApMirror),'Enable',switchOnOff(app.VrApMirror.Value))
      end
      % Function to update UIs Limits/Labels for coordinate options
      function limitVrApUI()
        s = 0.25*app.DfPxR;  u = app.DCUnit.Value;
        if app.DCSys.Value == "Polar"
          xl = [0, min([b0 app.D.NPx-b0]*2^.5)*app.DfPxR];  yl = [-1 1]*180;
          xt = 'Distance';  yt = 'Rotation';  yu = '°';  ys = 4;
        else
          xl = (app.TBX.Limits-app.RB0(1))*app.DfPxR;  yl = (app.TBY.Limits-app.RB0(2))*app.DfPxR;
          xt = 'X';  yt = 'Y';  yu = u;  ys = s;
        end
        set([app.VrApX app.VrApX_NF app.VrApY app.VrApY_NF app.VrApR_NF], ...
          {'Limits'},{xl; xl; yl; yl; app.TBR.Limits*app.DfPxR})
        set([app.VrApXLabel app.VrApYLabel app.VrApX_NFLabel app.VrApY_NFLabel app.VrApR_NFLabel], ...
          {'Text'},{xt; yt; u; yu; u})
        set([app.VrApX_NF app.VrApY_NF app.VrApR_NF],{'Step'},{s; ys; s})
      end
      
      % Function to draw virtual apertures
      function drawVrApAnnot()
        delete(findobj(app.Axes.Dfrn,'Tag','VrApertAnnot'))
        % plot the apertures, and olny allow the first one to be interactable
        app.A.VrAp = gobjects(app.VrApSymm.Value*(1+app.VrApMirror.Value), 1);
        for i = 1:numel(app.A.VrAp)
          app.A.VrAp(i) = drawcircle(app.Axes.Dfrn,"Center",app.P.VrApXY,"Radius",app.VrApR.Value,'Color','r', ...
            'FaceAlpha',0,'Deletable',0,'InteractionsAllowed','none','Tag','VrApertAnnot');
        end
        bringToFront(app.A.VrAp(1)); % Make sure the draggable annotations are at the front
        set(app.A.VrAp(1),'InteractionsAllowed','all','DrawingArea','unlimited')
        app.A.VrAp(1).UserData.Move = addlistener(app.A.VrAp(1),'ROIMoved',@moveVrAp);
        addlistener(app.A.VrAp(1),'MovingROI',@moveVrAp);
        % Mirror line/point
        app.A.VrApMirL = drawline(app.Axes.Dfrn,"Position",[0 0; app.D.NPx],"Color",[0 .7 0],'StripeColor','k', ...
          "LineWidth",1.5,"EdgeAlpha",.7,"InteractionsAllowed","none","Visible",app.VrApMirror.Value,"Deletable",0, ...
          'Tag','VrApertAnnot');
        app.A.VrApMirP = drawpoint(app.Axes.Dfrn,"Position",[min(app.D.NPx)/4 0]+b0,"Color","g",'MarkerSize',8, ...
          "Visible",app.VrApMirror.Value,"Deletable",0,'Tag','VrApertAnnot');
        app.A.VrApMirP.UserData.Move = addlistener(app.A.VrApMirP,'ROIMoved',@moveVrAp);
        addlistener(app.A.VrApMirP,'MovingROI',@moveVrAp);
      end

      % live update function for virtual aperture
      function moveVrAp(src, evt)
        % To determine real-time values
        rb0 = app.RB0;  scale = app.DfPxR;  np = app.D.NPx;
        md = app.VrApMirrRot.Value;  r = app.VrApR.Value;  vc = app.P.VrApXY;
        switch src
          case app.A.VrAp(1), r = src.Radius;  vc = src.Center;
          case {app.VrApX app.VrApX_NF app.VrApY app.VrApY_NF}
            % Potentially converting from polar/relative/mrad to cartesian absolute pixel coordinates
            x = app.VrApX.Value;  y = app.VrApY.Value;
            if ismember(src, [app.VrApX app.VrApX_NF]), x = evt.Value; else, y = evt.Value; end
            if app.DCSys.Value == "Cartesian"
              vc = [x y]/scale + rb0;
            else
              [x,y] = pol2cart(deg2rad(y), x/scale);
              vc = app.B0+[x y];
            end
          case app.VrApR, r = evt.Value;
          case app.VrApR_NF, r = evt.Value/scale;
          case app.VrApReset, r = app.TBR.Value;  vc = b0;
          case {app.VrApRotCCW app.VrApRotCW} % Rotation buttons
            % Clockwise if odd numbers of "Reverse X" "Reverse Y" "Rotate Clockwise" are true
            rot = app.VrApRotStep.Value * (1-2*rem(app.RvsXDfrn.Value+app.RvsYDfrn.Value+(src == app.VrApRotCW), 2));
            vc = (vc-b0)*rotMatD(rot)+b0;
          case {app.VrApMirrRot app.VrApMirrRot_NF}, md = evt.Value; % update the mirror line position
          case app.A.VrApMirP, mp = src.Position-b0;  md = atan2d(mp(2), mp(1));
        end
        % Restrict aperture location/size
        r = min(r, app.P.RMax);
        vc(vc > np) = np(vc > np);  vc(vc < 1) = 1;
        app.P.VrApXY = vc;

        % Update GUI with Limits check
        xyl = [app.VrApX.Limits; app.VrApY.Limits]';
        if app.DCSys.Value == "Cartesian"
          xyui = (vc-rb0)*scale;
        else % "Polar"
          xyui = vc-b0;
          [t,rho] = cart2pol(xyui(1), xyui(2));
          xyui = [rho*scale, rad2deg(t)];
        end
        xyui = max(min(xyui, xyl(2,:)), xyl(1,:)); % Limit check
        setExSrc(evt, [app.VrApR; app.VrApR_NF; app.VrApX; app.VrApX_NF; app.VrApY; app.VrApY_NF], ...
          {'Value'},{r; min(r*scale, app.P.RMax*scale); xyui(1); xyui(1); xyui(2); xyui(2)})
        setExSrc(evt, [app.VrApMirrRot app.VrApMirrRot_NF],'Value',md)
        
        if src == app.DCSys, return; end % Early return if only updating for coordinate options

        % Update ROIs
        [t,rho] = cart2pol(vc(1)-b0(1), vc(2)-b0(2));
        deg = rad2deg(t) + (0:360/app.VrApSymm.Value:360*(1-1/app.VrApSymm.Value))';
        vc2 = rho*[cosd(deg) sind(deg)];
        % If mirrored, double the amount of center positions
        if app.VrApMirror.Value
          R_mirror = rotMatD(90-md);
          vc2 = [vc2; vc2*R_mirror.*[-1 1]*(R_mirror')];
        end
        vc2 = vc2 + b0;  % Relative -> Absolute
        set(app.A.VrAp,{'Center'},num2cell(vc2,2),'Radius',r)
        % Update mirror line ROIs, whether visible or not
        app.A.VrApMirL.Position = [[1;app.D.NPxX], tand(md)*([1;app.D.NPxX]-b0(1))+b0(2)];
        [x,y] = pol2cart(deg2rad(md), sqrt(sum((app.A.VrApMirP.Position-b0).^2)));
        xyp = [x y]+b0;  xyp(xyp > np) = np(xyp > np);  xyp(xyp < 1) = 1;  % Restrict point within plot
        setExSrc(evt, app.A.VrApMirP,'Position',xyp)

        % Whether to update images
        if toUpdateImage(app,evt)
          % Generate mask
          mask_vr = false(app.D.NPx);
          for i = 1:numel(app.A.VrAp), mask_vr = mask_vr | createMask(app.A.VrAp(i), app.ImgD.Dfrn)'; end
          if app.VrApInvert.Value, mask_vr = 1 - mask_vr; end % Invert mask?
          app.Image.DfrnMask = mask_vr;
          app.Image.Real = gather(reshape(reshape(mask_vr,1,[])*app.Data, app.D.NFr));
          plotAllPatterns(app,evt)
        end
      end
        end

        % Callback function: CDColor, CDDTable, CDDelMask, CDDelResetMenu, 
        % ...and 18 other components
        function customDetectorCallbacks(app, event)
      b0 = app.B0; % Central beam location
      % Current selected row in Main Table `sel`, and the ROI group `ROI`
      if app.CDT.Selection > height(app.CDT.Data), app.CDT.Selection = []; end
      sel = app.CDT.Data(app.CDT.Selection, :);  ROI = {[]};
      if ~isempty(sel), ROI = app.A.Custom.(sel.ID); end

      switch event.Source
        case app.DCSys % Coordinate options
          limitCustDetrUI() % Update UI coordinate systems
          moveCDROI(ROI{1}, event); % Update ROI/mask/images
          
        case {app.UpdateImages app.CDInterMask app.MathEval}
          moveCDROI(ROI{1}, event); % Update ROI/mask/images
          
        case app.DetrMode % Entering current mode
          if ~isfield(app.A,'Custom'), app.A.Custom = []; end
          limitCustDetrUI() % Update UI coordinate systems
          updateEnableShowROI() % Update Enable/Show states of all ROI groups
          mockUICallbacks(app,app.CDT) % Update for selection change
          enableWindows(app,true) % Enable windows

        case app.CDT % Main table
          if event.EventName == "CellEdit"
            updateEnableShowROI() % Update Enable/Show states of all ROI groups
          end
          updateCustDetrUI();  moveCDROI(ROI{1}, event);  % Update UI and images
          
        case app.CDDelMask % Delete selected mask
          if isempty(sel), return; end % Early return if no mask selected
          % Delete Annotations, remove field from app.A.Custom and any mask associated with the detector
          delete(findobj(app.Axes.Dfrn.Children,'Tag',"Custom "+sel.ID));
          app.A.Custom.(sel.ID) = [];  app.A.Custom = rmfield(app.A.Custom,sel.ID);  
          app.Mask.Custom.(sel.ID) = [];  app.Mask.Custom = rmfield(app.Mask.Custom,sel.ID);
          app.Image.Custom.(sel.ID) = [];  app.Image.Custom = rmfield(app.Image.Custom,sel.ID);
          app.CDT.Data(app.CDT.Selection,:) = []; % Remove item from main table
          % Update selection
          if isempty(app.CDT.Data)
            app.CDT.Selection = [];  ROI = {[]}; % No slection if empty
          elseif isempty(app.CDT.Selection)
              app.CDT.Selection = height(app.CDT.Data);
              ROI = app.A.Custom.(app.CDT.Data.ID(app.CDT.Selection));
          else
            app.CDT.Selection = min(app.CDT.Selection,height(app.CDT.Data)); % Select last if exceeds table
            ROI = app.A.Custom.(app.CDT.Data.ID(app.CDT.Selection));
          end
          mockUICallbacks(app,app.CDT) % Update for selection change

        case app.CDDelResetMenu % Remove all masks; Reset
          delete(findobj(app.Axes.Dfrn.Children,'-regexp','Tag',"Custom "));
          app.CDT.Data(:,:) = [];  app.A.Custom = [];  app.Mask.Custom = [];  app.Image.Custom = [];
          ROI = {[]};  app.CDT.Selection = [];  
          mockUICallbacks(app,app.CDT) % Update for selection change

        case {app.CDNewCircle app.CDNewGrid app.CDNewBandpass app.CDNewWedge app.CDNewPolygon app.CDNewFromFile ...
            app.CDNewMath}
          % Create new mask
          idl = "@"; % Character before 'A'
          if ~isempty(app.CDT.Data), idl = app.CDT.Data(end,:).ID; end  % Last ID characters
          if idl == "ZZ"
            notifDLG(app, 'warn', "Mask ID can not go beyond 'ZZ'!","Maximum Custom Detectors Capacity Reached");
            return
          end
          nidl = double(char(idl))-64; % Serial numbers of Last ID characters, e.g. 3 for "C" or [1 2] for "AB"
          nidl = (numel(nidl)-1)*nidl(1)*26 + nidl(end); % Convert to one single serial number for Last ID
          id = replace(char([floor(nidl/26), rem(nidl, 26)+1]+64),'@',''); % New ID, e.g. 'AA' for 26, 'B' for 1
          % Preset values
          app.CDMirror.Value = 0;  app.CDInvert.Value = 0;  app.CDIntraMask.Value = "Union";
          switch event.Source
            case app.CDNewCircle, typ = "Circle";
            case app.CDNewGrid, typ = "Grid";
            case app.CDNewBandpass, typ = "Bandpass";
            case app.CDNewWedge, typ = "Wedge";  app.CDMirror.Value = 1;
            case app.CDNewPolygon, typ = "Polygon";
            case app.CDNewFromFile, typ = "File";
              im = importMask(app, "Dfrn");
              if isempty(im), return; end % Early return if `[]` (failed/canceled)
              app.Image.Custom.(id) = im;
            case app.CDNewMath, typ = "Math";
          end
          ROI = drawCDROI(id, typ);
          if isempty(ROI), return; end % Early return if draw ROI failed, e.g. polygon canceled.
          app.A.Custom.(id) = ROI; % Store the ROI group
          app.CDT.Data(end+1,:) = {id, typ, id, true, true, 1}; % Add row to Main Table
          app.CDT.Selection = height(app.CDT.Data); % Select the last, just added row
          colorCDTLabel(app.CDT.Selection,app.A.Custom.(id){1}.UserData.Color); % Color the Label in Main Table
          mockUICallbacks(app,app.CDT) % Update for selection change

        case {app.CDIntraMask, app.CDInvert, app.CDMirror} % Intra-mask, Invert Mask, Mirror Mask
          % Update values in `UserData` for current mask
          ROI{1}.UserData.IntraMask = app.CDIntraMask.Value;
          ROI{1}.UserData.Inverted = app.CDInvert.Value;
          ROI{1}.UserData.Mirrored = app.CDMirror.Value;
          ROI = drawCDROI(sel.ID, sel.Type);  app.A.Custom.(sel.ID) = ROI; % Re-drawn ROI
          mockUICallbacks(app,app.CDT) % Update for selection change

        case app.CDColor  % Change the color of mask annotations
          c = uisetcolor(ROI{1}.UserData.Color);  % Open palette
          if isequal(c, ROI{1}.UserData.Color), return; end % If color unchanged
          ROI{1}.UserData.Color = c;
          % make sure all overlays change color with main overlay
          cellfun(@(r) set(findobj(r,'-property','Color'),'Color',c),ROI);
          colorCDTLabel(app.CDT.Selection,c);  updateCustDetrUI() % Update UI

        case {app.CDFlipHorz app.CDFlipVert app.CDTranspose} % Flip and Transpose
          r90 = mod(app.RotDfrn.Value,180) == 90; % Whether diffraction is rotated by +/-90°
          if sel.Type == "File"
            % Transform the imported image array, then update/create mask from the transformed image
            switch event.Source
              case {app.CDFlipHorz app.CDFlipVert} % flip custom mask across horizontal/vertical axis
                if (r90 && event.Source == app.CDFlipHorz) || (~r90 && event.Source == app.CDFlipVert)
                  app.Image.Custom.(sel.ID) = flipud(app.Image.Custom.(sel.ID)); % Visually Flip X
                else
                  app.Image.Custom.(sel.ID) = fliplr(app.Image.Custom.(sel.ID)); % Visually Flip Y
                end
              case app.CDTranspose % transpose custom mask (only available if diffraction pattern is square)
                app.Image.Custom.(sel.ID) = app.Image.Custom.(sel.ID)';
            end
            moveCDROI(ROI{1}, event); % Update Images
          else
            % Convert Detail Table positions to cartesian relative (pixel or mrad)
            DT = app.CDDTable.Data(:, 1:2);
            if app.DCSys.Value == "Cartesian"
              xycr = DT - (app.B0-app.RB0)*app.DfPxR; 
            else
              xycr = DT(:, 1).*[cosd(DT(:, 2)) sind(DT(:, 2))];
            end
            switch event.Source
              case {app.CDFlipHorz app.CDFlipVert} % flip custom mask across horizontal/vertical axis
                if (r90 && event.Source == app.CDFlipHorz) || (~r90 && event.Source == app.CDFlipVert)
                  xycr(:,1) = -xycr(:,1); % Flip X
                else
                  xycr(:,2) = -xycr(:,2); % Flip Y
                end
              case app.CDTranspose % transpose custom mask
                xycr = fliplr(xycr); % Swap X/Y
            end
            % Convert from cartesian relative (pixel or mrad) back to whatever it should be
            if app.DCSys.Value == "Cartesian"
              app.CDDTable.Data(:, 1:2) = xycr + (app.B0-app.RB0)*app.DfPxR;
            else
              app.CDDTable.Data(:, 1:2) = [sqrt(sum(xycr.^2,2)), atan2d(xycr(:,2), xycr(:,1))];
            end
            mockUICallbacks(app, app.CDDTable) % Trigger Detail Table eidting callbacks
          end

        case {app.CDRotCCW, app.CDRotCW} % Rotate detector
          % Clockwise if odd numbers of "Reverse X" "Reverse Y" "Rotate Clockwise" are true
          rot = app.CDRotStep.Value*(1-2*rem(app.RvsXDfrn.Value+app.RvsYDfrn.Value+(event.Source == app.CDRotCW),2));
          if sel.Type == "File"
            % Transform the imported image array, then update/create mask from the transformed image
            app.Image.Custom.(sel.ID) = rot90(app.Image.Custom.(sel.ID), rot/90);
            moveCDROI(ROI{1}, event); % Update Images
          else
            % Edit coordinates in `app.CDDTable` and trigger its callbacks to rotate ROIs
            if app.DCSys.Value == "Cartesian"
              % If absolute then convert to relative then convert back, before/after rotation
              R = rotMatD(rot);  rrb0 = (app.B0-app.RB0)*app.DfPxR;
              app.CDDTable.Data(:, 1:2) = ((app.CDDTable.Data(:, 1:2)-rrb0)*R + rrb0);
            else
              app.CDDTable.Data(:, 2) = mod(app.CDDTable.Data(:, 2)+rot, 360);
            end
            mockUICallbacks(app, app.CDDTable) % Trigger Detail Table eidting callbacks
          end

        case app.CDDTable % Detail Table
          % Determine cartesian absolute pixel position from Detail Table (may be polar/relative/mrad)
          DT = app.CDDTable.Data;
          if app.DCSys.Value == "Cartesian"
            p = DT(:, 1:2)/app.DfPxR + app.RB0;
          else
            p = DT(:, 1)/app.DfPxR.*[cosd(DT(:, 2)) sind(DT(:, 2))] + app.RB0;
          end
          % Sync ROIs positions with the edited Detail Table
          switch sel.Type
            case {'Circle', 'Grid'}
              r = DT(1, 3);
              % If edited the 2nd R ([2 3] in table) then use that, instead of the default 1st R
              if isprop(event, 'Indices') && isequal(event.Indices, [2 3]), r = str2double(event.EditData); end
              ROI{1}.Center = p(1, :);  ROI{1}.Radius = r/app.DfPxR;
              if height(p) > 1, ROI{2}.Center = p(2, :);  ROI{2}.Radius = r/app.DfPxR; end
            case "Bandpass"
              c = p(1, :);
              % If edited the 2nd X or Y ([2 1] or [2 2] in table), then use that value, instead of the default 1st X/Y
              if isprop(event, 'Indices') && event.Indices(1) == 2 && any(event.Indices(2) == [1 2])
                c = p(2, :);
              end
              ROI{1}.Center = c;  ROI{1}.Radius = DT(1, 3)/app.DfPxR;
              ROI{2}.Center = c;  ROI{2}.Radius = DT(2, 3)/app.DfPxR;
            case "Wedge"
              ROI{1}.Position = p(1, :);  ROI{2}.Position = p(2, :);
            case "Polygon"
              ROI{1}.Position = p;
          end
          moveCDROI(ROI{1}, event); % Update Images
        otherwise
          error("Undefined")
      end


      %%% Sub functions
      % Function to return font color (black or white) based on input color
      function fc = fontColor(c)
        fc = [0 0 0] + (c.^2*[0.299;0.587;0.114] < 0.25); % Dark color criterion 
      end
      
      % Function to color Main Table
      function colorCDTLabel(isel,c)
        addStyle(app.CDT,uistyle('BackgroundColor',c,'FontColor',fontColor(c)),'cell',[isel, 3])
      end
      
      % Function to update UI labels; actually Custom Detector UIs have no limits
      function limitCustDetrUI()
        unit = " "+app.DCUnit.Value;
        if app.DCSys.Value == "Polar"
          app.CDDTable.ColumnName(1:3) = {"ρ"+unit, "θ °", "R"+unit};
        else
          app.CDDTable.ColumnName(1:3) = {"X"+unit, "Y"+unit, "R"+unit};
        end
      end
      
      % Function to update enable/show state of ROIs based on Main Table
      function updateEnableShowROI()
        for i = 1:height(app.CDT.Data)
          ri = app.CDT.Data(i, :); 
          cellfun(@(r) set(findobj(r,'-property','Visible'),'Visible',ri.Show && ri.Enable), ...
            app.A.Custom.(ri.ID));
        end
      end
      
      % Function to update UI
      function updateCustDetrUI()
        % Try to resize columns
        app.CDDTable.ColumnWidth = {'1x','1x','1x'};
        app.CDT.ColumnWidth = {'fit', 'fit', '1x', 'fit', 'fit', 'fit'};
        if ~isempty(app.CDT.Data), app.CDT.Data(end+1,:) = app.CDT.Data(end,:);  app.CDT.Data(end,:)=[];  end
        % Disable Detail UI if no ROI selected
        app.CDDetailsPanel.Enable = switchOnOff(~isempty(app.CDT.Selection));
        if isempty(app.CDT.Selection)
          app.CDDTable.Data = [];  set([app.CDDetailsGrid app.CDRotGrid],'BackgroundColor','w');
        else
          % Set component options based on current mask item
          u = app.A.Custom.(app.CDT.Data.ID(app.CDT.Selection)){1}.UserData;
          set([app.CDInvert app.CDIntraMask app.CDMirror],{'Value'},{u.Inverted; u.IntraMask; u.Mirrored})
          % Set Detail UI color; white font if darker background color
          set([app.CDDetailsGrid app.CDRotGrid app.CDDTable],'BackgroundColor',u.Color)
          app.CDIntraCombLabel.FontColor = fontColor(u.Color);  app.CDDTable.ForegroundColor = fontColor(u.Color);
          % Enable/Disable UI
          set([app.CDMirror app.CDIntraMask app.CDRotStep app.CDTranspose],{'Enable'},{0;0;1;1})
          equ = "";
          switch u.Type
            case "Circle", app.CDMirror.Enable = 'on'; app.CDIntraMask.Enable = app.CDMirror.Value;
            case "Wedge", app.CDMirror.Enable = 'on';
            case "Grid", app.CDIntraMask.Enable = 'on';
            case "Bandpass"
            case "Polygon"
            case "File"
              % Allow transpose/rotate 90° if diffraction image is square
              app.CDTranspose.Enable = ~range(app.D.NPx);
              set(app.CDRotStep,'Value',180 - ~range(app.D.NPx)*90, 'Enable','off');
            case "Math"
              equ = u.Math;
          end
          app.MathFormula.Value = equ;  % Put formula on Math UI 
        end
      end
      
      % Function to draw annotations
      function ROI = drawCDROI(id, typ)
        r0 = app.TBR.Value;  xmin = 0;  xmax = app.D.NPxX+1;  ymin = 0;  ymax = app.D.NPxY+1;
        % Initial values
        p1 = []; r1 = []; p2 = []; r2 = [];
        u = struct('ID',id,'Type',typ,'Color',rand(1,3), ...
          'Mirrored',app.CDMirror.Value,'IntraMask',app.CDIntraMask.Value,'Inverted',app.CDInvert.Value);
        % If the ROIs alread exist, get their current color/position/radius & UserData
        if isfield(app.A.Custom, id)
          ROI = app.A.Custom.(id);  u = ROI{1}.UserData;
          if isprop(ROI{1}, 'Position'), p1 = ROI{1}.Position; end
          if isprop(ROI{1}, 'Center'), p1 = ROI{1}.Center; r1 = ROI{1}.Radius; end
          if isprop(ROI{2}, 'Position'), p2 = ROI{2}.Position; end
          if isprop(ROI{2}, 'Center'), p2 = ROI{2}.Center; r2 = ROI{2}.Radius; end
          delete(ROI{1});  delete(ROI{2});  delete(ROI{3}) % Remove old ROIs
        end
        % Draw ROIs
        ROI = cell(3,1);
        switch typ
          case "Circle"
            if isempty(p1), p1 = b0;  r1 = r0; end % Initial disk identical to the central beam 
            ROI{1} = drawcircle(app.Axes.Dfrn,"Center",p1,"Radius",r1);
            if u.Mirrored
              ROI{2} = drawcircle(app.Axes.Dfrn,"Center",-p1+2*b0,"Radius",r1,'InteractionsAllowed','none');
            end
            set([ROI{1} ROI{2}],"FaceAlpha",0,"FaceSelectable",0,"DrawingArea","unlimited")
          case "Grid"
            % draw pair of apertures with starting size of transmitted disk
            if isempty(p2), p1 = b0 + [xmax-xmin 0]/4;  p2 = b0 + [0 ymax-ymin]/4;  r1 = r0; end
            ROI{1} = drawcircle(app.Axes.Dfrn,"Center",p1,"Radius",r1);
            ROI{2} = drawcircle(app.Axes.Dfrn,"Center",p2,"Radius",r1);
            set([ROI{1} ROI{2}],"FaceAlpha",0,"FaceSelectable",0,"DrawingArea","unlimited")
          case "Bandpass"
            % draw two circles for the user to resize, centered on the optic axis
            if isempty(r2), r1 = r0;  r2 = (xmax-xmin)/4 + r0/2; end
            ROI{1} = drawcircle(app.Axes.Dfrn,"Center",b0,"Radius",r1);
            ROI{2} = drawcircle(app.Axes.Dfrn,"Center",b0,"Radius",r2);
            set([ROI{1} ROI{2}],"FaceAlpha",0,"DrawingArea","unlimited","FaceSelectable",0)
            % draw a filled polygon between the two circles that the user cannont interact with, just for reference
            ROI{3} = drawpolygon(app.Axes.Dfrn,"Position",[ROI{1}.Vertices;ROI{2}.Vertices], ...
              "InteractionsAllowed","none","EdgeAlpha",0,"FaceSelectable",false);
          case "Wedge"
            % give polygon temporary set of points, keep invisible. Points will be sorted in moveWedge()
            if isempty(p2), l = min(app.D.NPx)/3; p1 = [l l]; p2 = [l 2*l]; end
            ROI{3} = drawpolygon(app.Axes.Dfrn,"Position",[p1;p2;b0],"InteractionsAllowed","none");
            ROI{1} = drawpoint(app.Axes.Dfrn,"Position",p1);
            ROI{2} = drawpoint(app.Axes.Dfrn,"Position",p2);
          case "Polygon"
            if isempty(p1)
              notifDLG(app,'help',sprintf("Please draw a Polygon ROI on the Diffraction image!\n\n" + ...
                "Press 'Esc' to cancel during drawing. Please refer to MATLAB's 'drawpolygon' for more tips."), ...
                "Draw Polygon ROI");
              % Disable UIs until polygon is drawn
              enableWindows(app,false);  figure(app.Fig.Dfrn);  app.Fig.Dfrn.UserData.grayout.Visible = 'off';
              ROI{1} = drawpolygon(app.Axes.Dfrn,"Color",u.Color);  p1 = ROI{1}.Position;
              enableWindows(app,true)
              % Early return if polygon is not drawn
              if isempty(p1), delete(ROI{1});  ROI = []; return; end
            else
              ROI{1} = drawpolygon(app.Axes.Dfrn,"Position",p1);
            end
            ROI{1}.FaceSelectable = 0;
            ROI{2} = drawpolygon(app.Axes.Dfrn,"Position",p1,"EdgeAlpha",0,"InteractionsAllowed","none");
          case "File"
            % Invisible ROI as placeholder
            ROI{1} = drawrectangle(app.Axes.Dfrn,"Position",[0 0 xmax+1 ymax+1],"InteractionsAllowed",'none', ...
              "EdgeAlpha",0,"FaceAlpha",0);
          case "Math"
            % Invisible ROI as placeholder
            ROI{1} = drawrectangle(app.Axes.Dfrn,"Position",[0 0 xmax+1 ymax+1],"InteractionsAllowed",'none', ...
              "EdgeAlpha",0,"FaceAlpha",0);
            app.MathFormula.Value = "1";  u.Math = "1";
            % Show Math Tab
            figure(app.Fig.Settings);  app.SettingsTabGroup.SelectedTab = app.MathTab;
        end
        % Try to set common properties for all ROI objects
        for i = 1:numel(ROI)
          if ~any(ishandle(ROI{i})), continue; end
          set(ROI{i},'Color',u.Color,'Deletable',false,'Tag',"Custom "+id,'UserData',u)
          ROI{i}.UserData.Move = addlistener(ROI{i},'ROIMoved',@moveCDROI);
          addlistener(ROI{i},'MovingROI',@moveCDROI);
          addlistener(ROI{i},'ROIClicked',@moveCDROI);
        end
      end

      % Function for UI/ROI changes
      function moveCDROI(src, evt)
        dbT = tic;
        % Clear diffraction mask and real images if empty source; early return
        if isempty(src), plotCustomMask(evt, []);  return; end
        
        % Retrieve ROIs of the current interacted-with
        ROI = app.A.Custom.(replace(src.Tag, 'Custom ',''));  u = ROI{1}.UserData; 
        % Change selected mask based on the one the user is interacting with
        if app.CDT.Data.ID(app.CDT.Selection) ~= u.ID
          app.CDT.Selection = find(app.CDT.Data.ID == u.ID);  updateCustDetrUI();
        end
        % Get position etc from ROI
        p1 = []; r1 = []; p2 = []; r2 = []; p1t = []; p2t = [];
        if isprop(ROI{1}, "Position"), p1 = ROI{1}.Position; end
        if isprop(ROI{1}, "Radius"), p1 = ROI{1}.Center; r1 = ROI{1}.Radius; end
        % Types with significant 2nd ROI
        if ismember(u.Type, ["Grid"; "Bandpass"; "Wedge"]) 
          if isprop(ROI{2}, "Position"), p2 = ROI{2}.Position; end
          if isprop(ROI{2}, "Radius"), p2 = ROI{2}.Center; r2 = ROI{2}.Radius; end
        end
        % Update Detail Table with coordinate options, with maybe reduced calculation policy
        if isStaticEvt(evt) || app.CalcPolicy.Value == 2
          if ~isempty(p1), p1t = p1(:, 1:2); end
          if ~isempty(p2), p2t = p2(:, 1:2); end
          xyt = ([p1t; p2t] - app.RB0)*app.DfPxR;
          if app.DCSys.Value == "Polar"
            xyt = [sqrt(sum(xyt.^2, 2)), mod(atan2d(xyt(:, 2), xyt(:, 1)), 360)]; 
          end
          app.CDDTable.Data = [xyt, [r1;r2]*app.DfPxR];
        end
        % Diffraction image size limits
        xmin = 0;  xmax = app.D.NPxX+1;  ymin = 0;  ymax = app.D.NPxY+1;  

        switch u.Type
          case "Circle"
            % Make mask from current detector objects
            mask = createMask(ROI{1}, app.ImgD.Dfrn)';
            if u.Mirrored
              ROI{2}.Center = 2*b0 - p1;  ROI{2}.Radius = r1; % update circle{2} location
              % Mask of mirrored circle
              mask2 = createMask(ROI{2}, app.ImgD.Dfrn)';
              switch u.IntraMask
                case "Additive", mask = mask + mask2;
                case "Union", mask = mask | mask2;
                case "Intersection", mask = mask & mask2;
              end
            end

          case "Grid"
            if isprop(evt, "CurrentRadius"), r1 = evt.CurrentRadius; end % Either from ROI{1} or ROI{2}
            ROI{1}.Radius = r1;  ROI{2}.Radius = r1; % Sync radii of both ROIs
            % Find position of all circles in the grid
            nRep = 100; % hard definition for max number of repeats (anything larger gets laggy)
            [repsy,repsx] = meshgrid(-nRep:nRep,-nRep:nRep);
            reps = [reshape(repsx,[],1), reshape(repsy,[],1)];
            reps = reps*([p1; p2]-b0)+b0; % apply basis vectors to each circle
            reps = uniquetol(reps,eps('single'),'ByRows',true); % Remove duplicates within single precision
            % filter out any grid points outside the diffraction pattern
            reps(reps(:,1) < -r1 | reps(:,2) < -r1 | reps(:,1) > xmax+r1 | reps(:,2) > ymax+r1, :) = [];
            % Draw circles for grid
            delete(ROI{3})
            ROI{3} = viscircles(app.Axes.Dfrn,reps,r1+reps(:,1)*0,'EnhanceVisibility',false,'Color',u.Color);
            ROI{3}.Tag = ROI{1}.Tag;  ROI{3}.Visible = ROI{1}.Visible; % Copy properties
            % Make mask from current detector grid
            [ygrid,xgrid] = meshgrid(1:app.D.NPxY, 1:app.D.NPxX);
            mask = reshape(sum(sqrt((xgrid(:)-reps(:,1)').^2+(ygrid(:)-reps(:,2)').^2) <= r1, 2), app.D.NPx);
            switch u.IntraMask
              case "Additive"
              case "Union", mask = logical(mask);
              case "Intersection", mask = mask > 1;
            end

          case "Bandpass"
            % Sync centers if moved
            if isprop(evt, "CurrentCenter")
              p1 = evt.CurrentCenter;  setExSrc(evt,[ROI{1} ROI{2}],'Center',p1)
            end
            % Generate mask
            pos = [ROI{2}.Vertices; ROI{1}.Vertices];
            ROI{3}.Position = pos;
            mask = createMask(ROI{3}, app.ImgD.Dfrn)';
            % Invert only ROI appearance here
            if u.Inverted
              ROI{3}.Position = [pos;[xmax,pos(end,2);xmax,ymax;xmin,ymax;xmin,ymin;xmax,ymin;xmax,pos(end,2)]];
            end

          case "Wedge"
            % Get polar degrees of the two Point ROIs in `dp`, and sort as `dp(1)` < `dp(2)`
            dp = [p1;p2]-b0;
            dp = sort(mod(atan2d(dp(:,2), dp(:,1)), 360));
            % Make sure the in-between angle < 180
            if dp(2)-dp(1) > 180, dp = [dp(2) dp(1)+360]; end
            % `d1` & `d2` are for degrees of vertices of the two symmetric sectors, `dp` as initials
            d1 = dp;  d2 = dp + 180;
            % Extra logics for inverted/mirrored mask
            if u.Inverted, d1 = [dp(2) dp(1)+360]; end
            if u.Inverted && u.Mirrored, d1 = [dp(2) dp(1)+180];  d2 = [dp(2)+180 dp(1)+360]; end
            % Insert diagonal degrees to cover the corners
            cnr = 45:90:720;
            d1 = [d1(1), cnr(cnr >= d1(1) & cnr <= d1(2)), d1(2)];
            d2 = [d2(1), cnr(cnr >= d2(1) & cnr <= d2(2)), d2(2)];
            % Ignore `d2` for single-sided mask, then convert to X/Y and insert the center [0 0] as starting point
            if u.Mirrored, d = [d1 fliplr(d2)]'; else, d = d1'; end
            ROI{3}.Position = [0 0; 2*max(ymax,xmax).*[cosd(d) sind(d)]] + b0;
            % Generate mask
            mask = createMask(ROI{3}, app.ImgD.Dfrn)';
            % Extra inversion, because it'll be inverted universally at the end
            if u.Inverted, mask = 1 - mask; end

          case "Polygon"
            % Invert only ROI appearance here
            if u.Inverted
              endPt = p1(end,:);
              endPtAng = atan2d(endPt(2)-b0(2),endPt(1)-b0(1));
              if endPtAng < 135 && endPtAng >= 45 % top edge
                corners = [endPt;endPt(1),ymax; xmax,ymax; xmax,ymin; xmin,ymin; xmin,ymax; endPt(1),ymax;endPt];
              elseif endPtAng < 45 && endPtAng >= -45 % right edge
                corners = [endPt;xmax,endPt(2); xmax,ymax; xmin,ymax; xmin,ymin; xmax,ymin; xmax,endPt(2);endPt];
              elseif endPtAng < -45 && endPtAng >= -135 % bottom edge
                corners = [endPt;endPt(1),ymin; xmin,ymin; xmin,ymax; xmax,ymax; xmax,ymin; endPt(1),ymin;endPt];
              else % left edge
                corners = [endPt;xmin,endPt(2); xmin,ymax; xmax,ymax; xmax,ymin; xmin,ymin; xmin,endPt(2);endPt];
              end
              pos2 = [corners;p1];
              faceAlpha = 0;
            else
              pos2 = p1;
              faceAlpha = 0.2;
            end
            % update poly2 points and faceAlpha for both. set max alpha to 0.2
            ROI{1}.FaceAlpha = faceAlpha;  ROI{2}.FaceAlpha = 0.2-faceAlpha;  ROI{2}.Position = pos2;
            mask = createMask(ROI{1}, app.ImgD.Dfrn)'; % generate mask

          case "File"
            % Only deal with visual here
            im0 = app.Image.Custom.(u.ID);
            if u.Inverted, im0 = max(im0,[],'all') - im0; end  % Invert only ROI appearance here
            delete(ROI{2})
            try % Draw boundaries of imported file mask
              visb = visboundaries(app.Axes.Dfrn,bwboundaries(im0'),'Color',u.Color,"EnhanceVisibility",0);
              if ~isempty(visb) % If some boundary is drawn
                visb.Tag = ROI{1}.Tag;  visb.Visible = ROI{1}.Visible;  ROI{2} = visb;  % Copy properties
              end
            catch
            end
            % Actual mask is already updated before
            mask = app.Image.Custom.(u.ID);
            
          case "Math"
            msg = strings(0);  
            equ0 = string(strjoin(app.MathFormula.Value));  ROI{1}.UserData.Math = equ0; % Get/Store formula
            ms = unique(string(regexp(equ0,"\<[A-Z]+\>",'match')));  % Extract "A" "AB" etc
            ids = string(fieldnames(app.A.Custom));  unk = setdiff(ms,ids); % Existing IDs and Unknown IDs
            % Check IDs
            if numel(unk), msg(end+1) = sprintf("Unknown IDs: %s !",strjoin(unk,", ")); end
            if ismember(u.ID, ms), msg(end+1) = sprintf("Self ID (%s) encountered!",u.ID); end
            % Try to evaluate 
            if isempty(msg)
              equ = regexprep(equ0,"\<"+ms+"\>","app.Mask.Custom."+ms);  mask_t = [];
              try
                mask_t = eval(equ);
                mask = zeros(app.D.NPx)+mask_t;
              catch ME
                msg(end+1) = sprintf('%s\n%s\n%s',ME.identifier,ME.message,ME.Correction);
                % Check result size
                if ~isempty(mask_t), msg(end+1) = sprintf("Resulted mask size is %d×%d (X×Y).",size(mask_t)); end
              end
            end
            % Check real/complex
            if isempty(msg) && ~isreal(mask),  msg(end+1) = sprintf("Resulted mask is a complex array!"); end
            % Early return if any error
            if ~isempty(msg)
              notifDLG(app,'warn',"Calculation failed!"+sprintf("\n%s",msg),"Evaluation Failed");
              return
            end
            delete(ROI{2})
            try % Draw boundaries of calculated mask
              visb = visboundaries(app.Axes.Dfrn,bwboundaries(mask'),'Color',u.Color,"EnhanceVisibility",0);
              if ~isempty(visb) % If some boundary is drawn
                visb.Tag = ROI{1}.Tag;  visb.Visible = ROI{1}.Visible;  ROI{2} = visb;  % Copy properties
              end
            catch
            end

        end
        % bring ROIs to the front
        if ismethod(ROI{3},'bringToFront'), bringToFront(ROI{3}); end
        if ismethod(ROI{2},'bringToFront'), bringToFront(ROI{2}); end
        bringToFront(ROI{1});
        app.A.Custom.(u.ID) = ROI; % Assign the created ROIs back to the global handle
        if u.Inverted, mask = max(mask,[],'all') - mask; end % Invert mask
        app.Mask.Custom.(u.ID) = mask; % Store mask

        plotCustomMask(evt, u.ID)
        debugToc(app, evt, "", dbT)
      end

      function plotCustomMask(evt, id)
        dbT = tic;
        % Whether to update images
        if toUpdateImage(app,evt)
          % start with a clear mask
          mask_cus = zeros(app.D.NPx,app.D.DataType);
          % Go through all enabled AND non-zero-weighting masks; add/intersect them accordingly
          cds = app.CDT.Data(app.CDT.Data.Enable & app.CDT.Data.Weight, :);
          for i = 1:height(cds)
            seli = cds(i, :);
            maski = app.Mask.Custom.(seli.ID)*seli.Weight;
            switch app.CDInterMask.Value
              case "Additive"
                mask_cus = mask_cus + maski;
              case "Current-only"
                if seli.ID == id, mask_cus = maski; end
              case "Intersection"
                if i == 1, mask_cus = maski; else, mask_cus = mask_cus & maski; end
              case "Union"
                mask_cus = mask_cus | maski;
            end
          end

          % Update images if the mask actually changed OR not a changing event
          if ~isequal(app.Image.DfrnMask, mask_cus) || isStaticEvt(evt)
            app.Image.DfrnMask = mask_cus;
            app.Image.Real = gather(reshape(reshape(mask_cus,1,[])*app.Data, app.D.NFr));
            plotAllPatterns(app,evt)
          end
        end
        debugToc(app, evt, "", dbT)
      end
        end

        % Button pushed function: MathEval
        function mathCallbacks(app, event)
      if app.DetrMode.Value == "CustMod"
        customDetectorCallbacks(app, event)
      end
        end

        % Menu selected function: SaveVecMenu
        function firstMoment(app, event)
      switch event.Source
        case app.SaveVecMenu % save vector field as image and figure
          saveVect();
      end
      
      
      function saveVect()
        % Create temporary figure with axes - saveas() is not supported as of r2019a in AppDesigner
        fig = figure;
        fig.Visible = 'off';
        figAxes = axes(fig);
        figAxes.NextPlot = 'replace';
        imagesc(figAxes,app.Image.CoMPh,'AlphaData',app.Image.CoMMagNorm);
        set(figAxes,'DataAspectRatio',[1 1 1],'XTick',[],'Ytick',[],'YDir','reverse','Color','k');
        axis(figAxes,app.P.RealAxLim);
        colormap(figAxes,hsv);
  
        vec = app.Axes.CoMPhMag.vecField;
  
        set(figAxes,'NextPlot','add');
        quiver(figAxes,1:vec:app.D.NFrX,...
          1:vec:app.D.NFrY,...
          -app.Image.CoMX(1:vec:end,1:vec:end)./vec,...
          -app.Image.CoMY(1:vec:end,1:vec:end)./vec,...
          1/vec,'w');
        set(figAxes,'DataAspectRatio',[1 1 1],'XTick',[],'Ytick',[],'YDir','reverse','NextPlot','replace');
        axis(figAxes,app.P.RealAxLim);
  
        % Save as a .png, .fig, and .eps (vector image, not pixelated)
        set(fig, 'Renderer', 'Painters');
        fig.InvertHardcopy = 'off';
        saveas(fig,strcat(app.SaveImgPrefix.Value,'VectField.png'),'png');
        fig.Visible = 'on';
        savefig(fig,strcat(app.SaveImgPrefix.Value,'VectField.fig'));
        fig.Visible = 'off';
        %saveas(fig,strcat(app.SaveImgPrefix.Value,'VectField.svg'),'svg');
  
        csvwrite(strcat(app.SaveImgPrefix.Value,'vector_field.txt'), ...
          [-app.Image.CoMX(1:vec:end,1:vec:end)./vec ...
          -app.Image.CoMY(1:vec:end,1:vec:end)./vec])
      end
        end

        % Button pushed function: ShowCoMMagWdw, ShowCoMPhMagWdw, 
        % ...and 16 other components
        function showWindowCallbacks(app, event)
      dbT = tic;

      id = app.DispImage.Value;
      switch event.Source
        case app.ShowImageWdw % Show selected image
          figure(app.Fig.(id));  movegui(app.Fig.(id))
        case app.ShowMaskWdw % Show diffraction or Real `space` mask for the selected image
          id = app.Axes.(id).UserData.space + "Mask";
          figure(app.Fig.(id));  movegui(app.Fig.(id))
        otherwise % All other `app.Show***Wdw`
          id = event.Source.Tag;
          figure(app.Fig.(id))
          movegui(app.Fig.(id))
          % If `id` is one of the available images, select it
          if ~app.DispLock.Value && ~strcmp(app.DispImage.Value, id) && ismember(id, app.DispImage.ItemsData)
            mockUICallbacks(app, app.DispImage, id)
          end
      end

      debugToc(app, event, "", dbT)
        end

        % Callback function: WdwHDfrn, WdwHReal, WdwSetAllDfrn, 
        % ...and 5 other components
        function resizeWindowCallbacks(app, event)
      sp = event.Source.Tag; % `Dfrn` or `Real` space from source Tag
      switch event.Source
        case {app.WdwSetDfrn app.WdwSetReal} % Set size for just one image window
          id = app.DispImage.Value; % Default image window to resize
          % If the selected image is not of that space, then resize that space's primary image window instead
          if app.Axes.(id).UserData.space ~= sp, id = sp; end
          app.Fig.(id).Position(3:4) = [app.("WdwW"+sp).Value app.("WdwH"+sp).Value];
          movegui(app.Fig.(id))
        case {app.WdwSetAllDfrn app.WdwSetAllReal} % Set all image windows of the given space to the same size
          for fig = app.G.ImgFig(app.G.ImgSp == sp)
            fig.Position(3:4) = [app.("WdwW"+sp).Value app.("WdwH"+sp).Value];
            movegui(fig)
          end
      end

        end

        % Callback function: CalcPolicy, UpdateImages
        function updateImagesCallbacks(app, event)
      switch event.Source
        case app.CalcPolicy
          % Update once if not passive
          if event.Value, mockUICallbacks(app,app.UpdateImages); end

        case app.UpdateImages % Calculate and update all images
          % Trigger detector callbacks 
          switch app.DetrMode.Value
            case "PrvwMod"
              previewCallbacks(app, event)
            case "AlignMod"
              transBeamCallbacks(app, event)
            case {'AnnMod' 'CoMMod' 'DPCMod'}
              annularDetectorCallbacks(app, event)
            case "VrApMod"
              virtualApertureCallbacks(app, event)
            case "CustMod"
              customDetectorCallbacks(app, event)
          end
          % Trigger real-space ROI callbacks
          if app.DetrMode.Value ~= "PrvwMod"
            realSpaceROICallbacks(app, event)
          end
      end
        end

        % Menu selected function: ResetQuant4DMenu
        function resetQuant4DCallbacks(app, event)
      % A state like just start-up without import
      unloadData(app)
      mockUICallbacks(app,app.DetrMode,"PrvwMod")
        end

        % Menu selected function: EnableallUIsMenu
        function enableAllUICallbacks(app, event)
      try delete(app.T.progDLG); catch; end % Try to delete any progress window
      enableWindows(app,true) % Enable all windows
        end

        % Menu selected function: Test1Menu
        function test1(app, event)
            
        end

        % Menu selected function: Test2Menu
        function test2(app, event)
        999 % Can be used for debuging or interfacing with internal data.
            % Just right click on the "Import" button and select Test2
        end
    end

    % Component initialization
    methods (Access = private)

        % Create UIFigure and components
        function createComponents(app)

            % Create Quant4D_Fig and hide until all components are created
            app.Quant4D_Fig = uifigure('Visible', 'off');
            app.Quant4D_Fig.AutoResizeChildren = 'off';
            app.Quant4D_Fig.Position = [1 1 262 472];
            app.Quant4D_Fig.Name = 'Quant4D';

            % Create SavePanel
            app.SavePanel = uipanel(app.Quant4D_Fig);
            app.SavePanel.AutoResizeChildren = 'off';
            app.SavePanel.BorderType = 'none';
            app.SavePanel.FontWeight = 'bold';
            app.SavePanel.Position = [-697 -35 424 500];

            % Create SaveGrid
            app.SaveGrid = uigridlayout(app.SavePanel);
            app.SaveGrid.ColumnWidth = {'1x'};
            app.SaveGrid.RowHeight = {'fit', '1x', 'fit'};
            app.SaveGrid.ColumnSpacing = 4;
            app.SaveGrid.RowSpacing = 0;
            app.SaveGrid.Padding = [0 0 0 0];

            % Create SaveDirGrid
            app.SaveDirGrid = uigridlayout(app.SaveGrid);
            app.SaveDirGrid.ColumnWidth = {'fit', '1x'};
            app.SaveDirGrid.RowHeight = {24};
            app.SaveDirGrid.ColumnSpacing = 4;
            app.SaveDirGrid.RowSpacing = 4;
            app.SaveDirGrid.Padding = [4 4 4 4];
            app.SaveDirGrid.Layout.Row = 1;
            app.SaveDirGrid.Layout.Column = 1;

            % Create SaveDirButton
            app.SaveDirButton = uibutton(app.SaveDirGrid, 'push');
            app.SaveDirButton.ButtonPushedFcn = createCallbackFcn(app, @saveCallbacks, true);
            app.SaveDirButton.BackgroundColor = [0.702 1 0.702];
            app.SaveDirButton.FontWeight = 'bold';
            app.SaveDirButton.Tooltip = {'Select saving/export directory'};
            app.SaveDirButton.Layout.Row = 1;
            app.SaveDirButton.Layout.Column = 1;
            app.SaveDirButton.Text = 'Directory';

            % Create SaveDir
            app.SaveDir = uieditfield(app.SaveDirGrid, 'text');
            app.SaveDir.ValueChangedFcn = createCallbackFcn(app, @saveCallbacks, true);
            app.SaveDir.Tooltip = {'Saving/Export directory'};
            app.SaveDir.Layout.Row = 1;
            app.SaveDir.Layout.Column = 2;

            % Create SaveTabGroup
            app.SaveTabGroup = uitabgroup(app.SaveGrid);
            app.SaveTabGroup.AutoResizeChildren = 'off';
            app.SaveTabGroup.SelectionChangedFcn = createCallbackFcn(app, @exportCallbacks, true);
            app.SaveTabGroup.Layout.Row = 2;
            app.SaveTabGroup.Layout.Column = 1;

            % Create SaveImgTab
            app.SaveImgTab = uitab(app.SaveTabGroup);
            app.SaveImgTab.AutoResizeChildren = 'off';
            app.SaveImgTab.Title = 'Save Images';

            % Create SaveImgGrid
            app.SaveImgGrid = uigridlayout(app.SaveImgTab);
            app.SaveImgGrid.ColumnWidth = {'1x'};
            app.SaveImgGrid.RowHeight = {'fit', 'fit', '1x', 'fit'};
            app.SaveImgGrid.ColumnSpacing = 4;
            app.SaveImgGrid.RowSpacing = 4;
            app.SaveImgGrid.Padding = [4 4 4 4];

            % Create SaveImgAngleGrid
            app.SaveImgAngleGrid = uigridlayout(app.SaveImgGrid);
            app.SaveImgAngleGrid.ColumnWidth = {'fit', 'fit', 'fit', '1x'};
            app.SaveImgAngleGrid.RowHeight = {'1x'};
            app.SaveImgAngleGrid.ColumnSpacing = 6;
            app.SaveImgAngleGrid.Padding = [0 0 0 0];
            app.SaveImgAngleGrid.Layout.Row = 2;
            app.SaveImgAngleGrid.Layout.Column = 1;

            % Create SavePrfxRi
            app.SavePrfxRi = uicheckbox(app.SaveImgAngleGrid);
            app.SavePrfxRi.ValueChangedFcn = createCallbackFcn(app, @saveCallbacks, true);
            app.SavePrfxRi.Text = 'Inner';
            app.SavePrfxRi.Layout.Row = 1;
            app.SavePrfxRi.Layout.Column = 2;

            % Create SavePrfxRo
            app.SavePrfxRo = uicheckbox(app.SaveImgAngleGrid);
            app.SavePrfxRo.ValueChangedFcn = createCallbackFcn(app, @saveCallbacks, true);
            app.SavePrfxRo.Text = 'Outer';
            app.SavePrfxRo.Layout.Row = 1;
            app.SavePrfxRo.Layout.Column = 3;

            % Create PrefixLabel
            app.PrefixLabel = uilabel(app.SaveImgAngleGrid);
            app.PrefixLabel.HorizontalAlignment = 'right';
            app.PrefixLabel.Layout.Row = 1;
            app.PrefixLabel.Layout.Column = 1;
            app.PrefixLabel.Text = 'Include Annular Detector Angles in Filename';

            % Create SaveImgDirGrid
            app.SaveImgDirGrid = uigridlayout(app.SaveImgGrid);
            app.SaveImgDirGrid.ColumnWidth = {'fit', '1x'};
            app.SaveImgDirGrid.RowHeight = {24};
            app.SaveImgDirGrid.ColumnSpacing = 4;
            app.SaveImgDirGrid.RowSpacing = 4;
            app.SaveImgDirGrid.Padding = [0 0 0 0];
            app.SaveImgDirGrid.Layout.Row = 1;
            app.SaveImgDirGrid.Layout.Column = 1;

            % Create FilenamePrefixLabel
            app.FilenamePrefixLabel = uilabel(app.SaveImgDirGrid);
            app.FilenamePrefixLabel.HorizontalAlignment = 'right';
            app.FilenamePrefixLabel.Layout.Row = 1;
            app.FilenamePrefixLabel.Layout.Column = 1;
            app.FilenamePrefixLabel.Text = 'Filename Prefix';

            % Create SaveImgPrefix
            app.SaveImgPrefix = uieditfield(app.SaveImgDirGrid, 'text');
            app.SaveImgPrefix.ValueChangedFcn = createCallbackFcn(app, @saveCallbacks, true);
            app.SaveImgPrefix.Layout.Row = 1;
            app.SaveImgPrefix.Layout.Column = 2;

            % Create SaveImgListGrid
            app.SaveImgListGrid = uigridlayout(app.SaveImgGrid);
            app.SaveImgListGrid.ColumnWidth = {'1x', 'fit'};
            app.SaveImgListGrid.RowHeight = {'fit', '1x'};
            app.SaveImgListGrid.ColumnSpacing = 4;
            app.SaveImgListGrid.RowSpacing = 4;
            app.SaveImgListGrid.Padding = [0 0 0 0];
            app.SaveImgListGrid.Layout.Row = 3;
            app.SaveImgListGrid.Layout.Column = 1;

            % Create SaveImgList
            app.SaveImgList = uilistbox(app.SaveImgListGrid);
            app.SaveImgList.Items = {};
            app.SaveImgList.Multiselect = 'on';
            app.SaveImgList.ValueChangedFcn = createCallbackFcn(app, @saveCallbacks, true);
            app.SaveImgList.Layout.Row = 2;
            app.SaveImgList.Layout.Column = [1 2];
            app.SaveImgList.Value = {};

            % Create ImagestoSaveMultiselectwithCtrlShiftLabel
            app.ImagestoSaveMultiselectwithCtrlShiftLabel = uilabel(app.SaveImgListGrid);
            app.ImagestoSaveMultiselectwithCtrlShiftLabel.HorizontalAlignment = 'center';
            app.ImagestoSaveMultiselectwithCtrlShiftLabel.VerticalAlignment = 'bottom';
            app.ImagestoSaveMultiselectwithCtrlShiftLabel.FontWeight = 'bold';
            app.ImagestoSaveMultiselectwithCtrlShiftLabel.Layout.Row = 1;
            app.ImagestoSaveMultiselectwithCtrlShiftLabel.Layout.Column = [1 2];
            app.ImagestoSaveMultiselectwithCtrlShiftLabel.Text = 'Images to Save (Multi-select with Ctrl/Shift)';

            % Create SaveImgSelectAll
            app.SaveImgSelectAll = uicheckbox(app.SaveImgListGrid);
            app.SaveImgSelectAll.ValueChangedFcn = createCallbackFcn(app, @saveCallbacks, true);
            app.SaveImgSelectAll.Text = 'Select All';
            app.SaveImgSelectAll.Layout.Row = 1;
            app.SaveImgSelectAll.Layout.Column = 2;

            % Create SaveImgFormatGrid
            app.SaveImgFormatGrid = uigridlayout(app.SaveImgGrid);
            app.SaveImgFormatGrid.ColumnWidth = {'1x'};
            app.SaveImgFormatGrid.RowHeight = {20, 20};
            app.SaveImgFormatGrid.ColumnSpacing = 4;
            app.SaveImgFormatGrid.RowSpacing = 2;
            app.SaveImgFormatGrid.Padding = [0 0 0 0];
            app.SaveImgFormatGrid.Layout.Row = 4;
            app.SaveImgFormatGrid.Layout.Column = 1;

            % Create SaveImgTIF
            app.SaveImgTIF = uicheckbox(app.SaveImgFormatGrid);
            app.SaveImgTIF.ValueChangedFcn = createCallbackFcn(app, @saveCallbacks, true);
            app.SaveImgTIF.Text = 'Raw data (single-precision), TIFF';
            app.SaveImgTIF.Layout.Row = 1;
            app.SaveImgTIF.Layout.Column = 1;
            app.SaveImgTIF.Value = true;

            % Create SaveImgPNGGrid
            app.SaveImgPNGGrid = uigridlayout(app.SaveImgFormatGrid);
            app.SaveImgPNGGrid.ColumnWidth = {'fit', 'fit', 'fit', 40, '1x'};
            app.SaveImgPNGGrid.RowHeight = {'1x'};
            app.SaveImgPNGGrid.ColumnSpacing = 0;
            app.SaveImgPNGGrid.RowSpacing = 4;
            app.SaveImgPNGGrid.Padding = [0 0 0 0];
            app.SaveImgPNGGrid.Layout.Row = 2;
            app.SaveImgPNGGrid.Layout.Column = 1;

            % Create SaveImgAnnotDPI
            app.SaveImgAnnotDPI = uieditfield(app.SaveImgPNGGrid, 'numeric');
            app.SaveImgAnnotDPI.Limits = [1 Inf];
            app.SaveImgAnnotDPI.RoundFractionalValues = 'on';
            app.SaveImgAnnotDPI.ValueDisplayFormat = '%d';
            app.SaveImgAnnotDPI.ValueChangedFcn = createCallbackFcn(app, @saveCallbacks, true);
            app.SaveImgAnnotDPI.Layout.Row = 1;
            app.SaveImgAnnotDPI.Layout.Column = 4;
            app.SaveImgAnnotDPI.Value = 72;

            % Create SaveImgAnnotDPILabel
            app.SaveImgAnnotDPILabel = uilabel(app.SaveImgPNGGrid);
            app.SaveImgAnnotDPILabel.Layout.Row = 1;
            app.SaveImgAnnotDPILabel.Layout.Column = 3;
            app.SaveImgAnnotDPILabel.Text = 'DPI';

            % Create SaveImgPNGAnnot
            app.SaveImgPNGAnnot = uicheckbox(app.SaveImgPNGGrid);
            app.SaveImgPNGAnnot.ValueChangedFcn = createCallbackFcn(app, @saveCallbacks, true);
            app.SaveImgPNGAnnot.Text = 'with annotations, e.g. ROIs,';
            app.SaveImgPNGAnnot.Layout.Row = 1;
            app.SaveImgPNGAnnot.Layout.Column = 2;
            app.SaveImgPNGAnnot.Value = true;

            % Create SaveImgPNG
            app.SaveImgPNG = uicheckbox(app.SaveImgPNGGrid);
            app.SaveImgPNG.ValueChangedFcn = createCallbackFcn(app, @saveCallbacks, true);
            app.SaveImgPNG.Text = 'As-displayed, PNG; ';
            app.SaveImgPNG.Layout.Row = 1;
            app.SaveImgPNG.Layout.Column = 1;
            app.SaveImgPNG.Value = true;

            % Create ExportTab
            app.ExportTab = uitab(app.SaveTabGroup);
            app.ExportTab.AutoResizeChildren = 'off';
            app.ExportTab.Title = 'Export Dataset';

            % Create ExportGrid
            app.ExportGrid = uigridlayout(app.ExportTab);
            app.ExportGrid.RowHeight = {'fit', 24, 'fit', 'fit', 'fit', '1x'};
            app.ExportGrid.ColumnSpacing = 6;
            app.ExportGrid.RowSpacing = 4;
            app.ExportGrid.Padding = [4 4 4 4];

            % Create ExportFileGrid
            app.ExportFileGrid = uigridlayout(app.ExportGrid);
            app.ExportFileGrid.ColumnWidth = {'fit', '1x', 'fit'};
            app.ExportFileGrid.RowHeight = {24};
            app.ExportFileGrid.ColumnSpacing = 4;
            app.ExportFileGrid.RowSpacing = 4;
            app.ExportFileGrid.Padding = [0 0 0 0];
            app.ExportFileGrid.Layout.Row = 1;
            app.ExportFileGrid.Layout.Column = [1 2];

            % Create ExpDimSuff
            app.ExpDimSuff = uicheckbox(app.ExportFileGrid);
            app.ExpDimSuff.ValueChangedFcn = createCallbackFcn(app, @exportCallbacks, true);
            app.ExpDimSuff.Tooltip = {'To suffix the filename with image stack''s dimensions'};
            app.ExpDimSuff.Text = 'Dimensions suffix';
            app.ExpDimSuff.Layout.Row = 1;
            app.ExpDimSuff.Layout.Column = 3;

            % Create ExpFilename
            app.ExpFilename = uieditfield(app.ExportFileGrid, 'text');
            app.ExpFilename.ValueChangedFcn = createCallbackFcn(app, @exportCallbacks, true);
            app.ExpFilename.Layout.Row = 1;
            app.ExpFilename.Layout.Column = 2;

            % Create FilenameLabel
            app.FilenameLabel = uilabel(app.ExportFileGrid);
            app.FilenameLabel.HorizontalAlignment = 'right';
            app.FilenameLabel.Layout.Row = 1;
            app.FilenameLabel.Layout.Column = 1;
            app.FilenameLabel.Text = 'Filename';

            % Create ExpNotes
            app.ExpNotes = uitextarea(app.ExportGrid);
            app.ExpNotes.Editable = 'off';
            app.ExpNotes.Layout.Row = 6;
            app.ExpNotes.Layout.Column = [1 2];

            % Create SummaryLabel
            app.SummaryLabel = uilabel(app.ExportGrid);
            app.SummaryLabel.HorizontalAlignment = 'center';
            app.SummaryLabel.VerticalAlignment = 'bottom';
            app.SummaryLabel.FontWeight = 'bold';
            app.SummaryLabel.Layout.Row = 5;
            app.SummaryLabel.Layout.Column = [1 2];
            app.SummaryLabel.Text = 'Summary';

            % Create ExpFormat
            app.ExpFormat = uidropdown(app.ExportGrid);
            app.ExpFormat.Items = {'HDF5 (*.h5)', 'Raw binary (*.raw)'};
            app.ExpFormat.ItemsData = {'h5', 'raw'};
            app.ExpFormat.ValueChangedFcn = createCallbackFcn(app, @exportCallbacks, true);
            app.ExpFormat.Layout.Row = 2;
            app.ExpFormat.Layout.Column = 1;
            app.ExpFormat.Value = 'h5';

            % Create ExpByteOrder
            app.ExpByteOrder = uidropdown(app.ExportGrid);
            app.ExpByteOrder.Items = {'Little Endian', 'Big Endian'};
            app.ExpByteOrder.ItemsData = {'l', 'b'};
            app.ExpByteOrder.ValueChangedFcn = createCallbackFcn(app, @exportCallbacks, true);
            app.ExpByteOrder.Layout.Row = 2;
            app.ExpByteOrder.Layout.Column = 2;
            app.ExpByteOrder.Value = 'l';

            % Create ExpFrPart
            app.ExpFrPart = uicheckbox(app.ExportGrid);
            app.ExpFrPart.ValueChangedFcn = createCallbackFcn(app, @exportCallbacks, true);
            app.ExpFrPart.Tag = 'Export Real';
            app.ExpFrPart.Text = '    Real-space Partial Export';
            app.ExpFrPart.FontWeight = 'bold';
            app.ExpFrPart.Layout.Row = 3;
            app.ExpFrPart.Layout.Column = 2;

            % Create ExpPxPart
            app.ExpPxPart = uicheckbox(app.ExportGrid);
            app.ExpPxPart.ValueChangedFcn = createCallbackFcn(app, @exportCallbacks, true);
            app.ExpPxPart.Tag = 'Export Dfrn';
            app.ExpPxPart.Text = '    Diffraction Partial Export';
            app.ExpPxPart.FontWeight = 'bold';
            app.ExpPxPart.Layout.Row = 3;
            app.ExpPxPart.Layout.Column = 1;

            % Create ExportFrRangeGrid
            app.ExportFrRangeGrid = uigridlayout(app.ExportGrid);
            app.ExportFrRangeGrid.ColumnWidth = {'1x', 80, '1x', 80};
            app.ExportFrRangeGrid.RowHeight = {24, 24, 24};
            app.ExportFrRangeGrid.ColumnSpacing = 4;
            app.ExportFrRangeGrid.RowSpacing = 2;
            app.ExportFrRangeGrid.Padding = [0 0 0 0];
            app.ExportFrRangeGrid.Layout.Row = 4;
            app.ExportFrRangeGrid.Layout.Column = 2;

            % Create xsub1Label_4
            app.xsub1Label_4 = uilabel(app.ExportFrRangeGrid);
            app.xsub1Label_4.HorizontalAlignment = 'right';
            app.xsub1Label_4.Layout.Row = 2;
            app.xsub1Label_4.Layout.Column = 1;
            app.xsub1Label_4.Text = 'x<sub>1';

            % Create EFrX1
            app.EFrX1 = uispinner(app.ExportFrRangeGrid);
            app.EFrX1.ValueChangingFcn = createCallbackFcn(app, @exportCallbacks, true);
            app.EFrX1.RoundFractionalValues = 'on';
            app.EFrX1.ValueDisplayFormat = '%.0f';
            app.EFrX1.ValueChangedFcn = createCallbackFcn(app, @exportCallbacks, true);
            app.EFrX1.Tag = 'Export Real';
            app.EFrX1.Tooltip = {'Starting frame on X (3rd dimension of image stack) to import'};
            app.EFrX1.Layout.Row = 2;
            app.EFrX1.Layout.Column = 2;
            app.EFrX1.Value = 1;

            % Create ENFrXl
            app.ENFrXl = uilabel(app.ExportFrRangeGrid);
            app.ENFrXl.HorizontalAlignment = 'right';
            app.ENFrXl.Layout.Row = 3;
            app.ENFrXl.Layout.Column = 1;
            app.ENFrXl.Text = 'X';

            % Create ENFrX
            app.ENFrX = uispinner(app.ExportFrRangeGrid);
            app.ENFrX.ValueChangingFcn = createCallbackFcn(app, @exportCallbacks, true);
            app.ENFrX.RoundFractionalValues = 'on';
            app.ENFrX.ValueDisplayFormat = '%.0f';
            app.ENFrX.ValueChangedFcn = createCallbackFcn(app, @exportCallbacks, true);
            app.ENFrX.Tag = 'Export Real';
            app.ENFrX.Tooltip = {'Total frames after sampling on X (3rd dimension of image stack)'};
            app.ENFrX.Layout.Row = 3;
            app.ENFrX.Layout.Column = 2;
            app.ENFrX.Value = 1;

            % Create ysub1Label_4
            app.ysub1Label_4 = uilabel(app.ExportFrRangeGrid);
            app.ysub1Label_4.HorizontalAlignment = 'right';
            app.ysub1Label_4.Layout.Row = 2;
            app.ysub1Label_4.Layout.Column = 3;
            app.ysub1Label_4.Text = 'y<sub>1';

            % Create EFrY1
            app.EFrY1 = uispinner(app.ExportFrRangeGrid);
            app.EFrY1.ValueChangingFcn = createCallbackFcn(app, @exportCallbacks, true);
            app.EFrY1.RoundFractionalValues = 'on';
            app.EFrY1.ValueDisplayFormat = '%.0f';
            app.EFrY1.ValueChangedFcn = createCallbackFcn(app, @exportCallbacks, true);
            app.EFrY1.Tag = 'Export Real';
            app.EFrY1.Tooltip = {'Starting frame on Y (4th dimension of image stack) to import'};
            app.EFrY1.Layout.Row = 2;
            app.EFrY1.Layout.Column = 4;
            app.EFrY1.Value = 1;

            % Create ENFrYl
            app.ENFrYl = uilabel(app.ExportFrRangeGrid);
            app.ENFrYl.HorizontalAlignment = 'right';
            app.ENFrYl.Layout.Row = 3;
            app.ENFrYl.Layout.Column = 3;
            app.ENFrYl.Text = 'Y';

            % Create ENFrY
            app.ENFrY = uispinner(app.ExportFrRangeGrid);
            app.ENFrY.ValueChangingFcn = createCallbackFcn(app, @exportCallbacks, true);
            app.ENFrY.RoundFractionalValues = 'on';
            app.ENFrY.ValueDisplayFormat = '%.0f';
            app.ENFrY.ValueChangedFcn = createCallbackFcn(app, @exportCallbacks, true);
            app.ENFrY.Tag = 'Export Real';
            app.ENFrY.Tooltip = {'Total frames after sampling on Y (4th dimension of image stack)'};
            app.ENFrY.Layout.Row = 3;
            app.ENFrY.Layout.Column = 4;
            app.ENFrY.Value = 1;

            % Create EFrD
            app.EFrD = uispinner(app.ExportFrRangeGrid);
            app.EFrD.ValueChangingFcn = createCallbackFcn(app, @exportCallbacks, true);
            app.EFrD.RoundFractionalValues = 'on';
            app.EFrD.ValueDisplayFormat = '%.0f';
            app.EFrD.ValueChangedFcn = createCallbackFcn(app, @exportCallbacks, true);
            app.EFrD.Tag = 'Export Real';
            app.EFrD.Tooltip = {'Distance between sampling frames in both X & Y directions (neighboring frames have distance of 1)'};
            app.EFrD.Layout.Row = 1;
            app.EFrD.Layout.Column = 4;
            app.EFrD.Value = 1;

            % Create SamplingIntervalLabel
            app.SamplingIntervalLabel = uilabel(app.ExportFrRangeGrid);
            app.SamplingIntervalLabel.HorizontalAlignment = 'right';
            app.SamplingIntervalLabel.Layout.Row = 1;
            app.SamplingIntervalLabel.Layout.Column = [1 3];
            app.SamplingIntervalLabel.Text = 'Sampling Interval';

            % Create ExportPxRangeGrid
            app.ExportPxRangeGrid = uigridlayout(app.ExportGrid);
            app.ExportPxRangeGrid.ColumnWidth = {'1x', 80, '1x', 80};
            app.ExportPxRangeGrid.RowHeight = {24, 24, 24};
            app.ExportPxRangeGrid.ColumnSpacing = 4;
            app.ExportPxRangeGrid.RowSpacing = 2;
            app.ExportPxRangeGrid.Padding = [0 0 0 0];
            app.ExportPxRangeGrid.Layout.Row = 4;
            app.ExportPxRangeGrid.Layout.Column = 1;

            % Create EPxX1
            app.EPxX1 = uispinner(app.ExportPxRangeGrid);
            app.EPxX1.ValueChangingFcn = createCallbackFcn(app, @exportCallbacks, true);
            app.EPxX1.RoundFractionalValues = 'on';
            app.EPxX1.ValueDisplayFormat = '%.0f';
            app.EPxX1.ValueChangedFcn = createCallbackFcn(app, @exportCallbacks, true);
            app.EPxX1.Tag = 'Export Dfrn';
            app.EPxX1.Tooltip = {'Starting pixel on X (1st dimension of image stack) to import, in each frame'};
            app.EPxX1.Layout.Row = 2;
            app.EPxX1.Layout.Column = 2;
            app.EPxX1.Value = 1;

            % Create xsub1Label_3
            app.xsub1Label_3 = uilabel(app.ExportPxRangeGrid);
            app.xsub1Label_3.HorizontalAlignment = 'right';
            app.xsub1Label_3.Layout.Row = 2;
            app.xsub1Label_3.Layout.Column = 1;
            app.xsub1Label_3.Text = 'x<sub>1';

            % Create ENPxX
            app.ENPxX = uispinner(app.ExportPxRangeGrid);
            app.ENPxX.ValueChangingFcn = createCallbackFcn(app, @exportCallbacks, true);
            app.ENPxX.RoundFractionalValues = 'on';
            app.ENPxX.ValueDisplayFormat = '%.0f';
            app.ENPxX.ValueChangedFcn = createCallbackFcn(app, @exportCallbacks, true);
            app.ENPxX.Tag = 'Export Dfrn';
            app.ENPxX.Tooltip = {'Total pixels after binning on X (1st dimension of image stack), in each frame'};
            app.ENPxX.Layout.Row = 3;
            app.ENPxX.Layout.Column = 2;
            app.ENPxX.Value = 1;

            % Create ENPxXl
            app.ENPxXl = uilabel(app.ExportPxRangeGrid);
            app.ENPxXl.HorizontalAlignment = 'right';
            app.ENPxXl.Layout.Row = 3;
            app.ENPxXl.Layout.Column = 1;
            app.ENPxXl.Text = 'X';

            % Create EPxY1
            app.EPxY1 = uispinner(app.ExportPxRangeGrid);
            app.EPxY1.ValueChangingFcn = createCallbackFcn(app, @exportCallbacks, true);
            app.EPxY1.RoundFractionalValues = 'on';
            app.EPxY1.ValueDisplayFormat = '%.0f';
            app.EPxY1.ValueChangedFcn = createCallbackFcn(app, @exportCallbacks, true);
            app.EPxY1.Tag = 'Export Dfrn';
            app.EPxY1.Tooltip = {'Starting pixel on Y (2nd dimension of image stack) to import, in each frame'};
            app.EPxY1.Layout.Row = 2;
            app.EPxY1.Layout.Column = 4;
            app.EPxY1.Value = 1;

            % Create ysub1Label_3
            app.ysub1Label_3 = uilabel(app.ExportPxRangeGrid);
            app.ysub1Label_3.HorizontalAlignment = 'right';
            app.ysub1Label_3.Layout.Row = 2;
            app.ysub1Label_3.Layout.Column = 3;
            app.ysub1Label_3.Text = 'y<sub>1';

            % Create ENPxY
            app.ENPxY = uispinner(app.ExportPxRangeGrid);
            app.ENPxY.ValueChangingFcn = createCallbackFcn(app, @exportCallbacks, true);
            app.ENPxY.RoundFractionalValues = 'on';
            app.ENPxY.ValueDisplayFormat = '%.0f';
            app.ENPxY.ValueChangedFcn = createCallbackFcn(app, @exportCallbacks, true);
            app.ENPxY.Tag = 'Export Dfrn';
            app.ENPxY.Tooltip = {'Total pixels after binning on Y (2nd dimension of image stack), in each frame'};
            app.ENPxY.Layout.Row = 3;
            app.ENPxY.Layout.Column = 4;
            app.ENPxY.Value = 1;

            % Create ENPxYl
            app.ENPxYl = uilabel(app.ExportPxRangeGrid);
            app.ENPxYl.HorizontalAlignment = 'right';
            app.ENPxYl.Layout.Row = 3;
            app.ENPxYl.Layout.Column = 3;
            app.ENPxYl.Text = 'Y';

            % Create EPxD
            app.EPxD = uispinner(app.ExportPxRangeGrid);
            app.EPxD.ValueChangingFcn = createCallbackFcn(app, @exportCallbacks, true);
            app.EPxD.RoundFractionalValues = 'on';
            app.EPxD.ValueDisplayFormat = '%.0f';
            app.EPxD.ValueChangedFcn = createCallbackFcn(app, @exportCallbacks, true);
            app.EPxD.Tag = 'Export Dfrn';
            app.EPxD.Tooltip = {'To bin n×n pixels into one (by averaging)'};
            app.EPxD.Layout.Row = 1;
            app.EPxD.Layout.Column = 4;
            app.EPxD.Value = 1;

            % Create BinningDistanceLabel_2
            app.BinningDistanceLabel_2 = uilabel(app.ExportPxRangeGrid);
            app.BinningDistanceLabel_2.HorizontalAlignment = 'right';
            app.BinningDistanceLabel_2.Layout.Row = 1;
            app.BinningDistanceLabel_2.Layout.Column = [1 3];
            app.BinningDistanceLabel_2.Text = 'Binning Distance';

            % Create SaveExportButtonGrid
            app.SaveExportButtonGrid = uigridlayout(app.SaveGrid);
            app.SaveExportButtonGrid.ColumnWidth = {120, '1x', 120};
            app.SaveExportButtonGrid.RowHeight = {'1x'};
            app.SaveExportButtonGrid.ColumnSpacing = 8;
            app.SaveExportButtonGrid.Padding = [4 4 4 4];
            app.SaveExportButtonGrid.Layout.Row = 3;
            app.SaveExportButtonGrid.Layout.Column = 1;

            % Create SaveCloseButton
            app.SaveCloseButton = uibutton(app.SaveExportButtonGrid, 'push');
            app.SaveCloseButton.ButtonPushedFcn = createCallbackFcn(app, @exportCallbacks, true);
            app.SaveCloseButton.FontWeight = 'bold';
            app.SaveCloseButton.Layout.Row = 1;
            app.SaveCloseButton.Layout.Column = 3;
            app.SaveCloseButton.Text = 'Close';

            % Create SaveExport
            app.SaveExport = uibutton(app.SaveExportButtonGrid, 'push');
            app.SaveExport.ButtonPushedFcn = createCallbackFcn(app, @saveCallbacks, true);
            app.SaveExport.FontWeight = 'bold';
            app.SaveExport.Layout.Row = 1;
            app.SaveExport.Layout.Column = 1;
            app.SaveExport.Text = 'Save Images';

            % Create Quant4D_FigGrid
            app.Quant4D_FigGrid = uigridlayout(app.Quant4D_Fig);
            app.Quant4D_FigGrid.ColumnWidth = {'1x'};
            app.Quant4D_FigGrid.RowHeight = {'fit', 'fit', '1x', 'fit'};
            app.Quant4D_FigGrid.ColumnSpacing = 0;
            app.Quant4D_FigGrid.RowSpacing = 0;
            app.Quant4D_FigGrid.Padding = [0 0 0 0];

            % Create ShortcutButtonGrid
            app.ShortcutButtonGrid = uigridlayout(app.Quant4D_FigGrid);
            app.ShortcutButtonGrid.ColumnWidth = {'1x', 24, 24, 24, 24, 24, 24};
            app.ShortcutButtonGrid.RowHeight = {24};
            app.ShortcutButtonGrid.ColumnSpacing = 4;
            app.ShortcutButtonGrid.RowSpacing = 4;
            app.ShortcutButtonGrid.Padding = [4 4 4 4];
            app.ShortcutButtonGrid.Layout.Row = 1;
            app.ShortcutButtonGrid.Layout.Column = 1;

            % Create AutoSaveImg
            app.AutoSaveImg = uibutton(app.ShortcutButtonGrid, 'push');
            app.AutoSaveImg.ButtonPushedFcn = createCallbackFcn(app, @saveCallbacks, true);
            app.AutoSaveImg.Icon = 'autoSave.png';
            app.AutoSaveImg.Tooltip = {'Repeat Previous Image Saving Operation'};
            app.AutoSaveImg.Layout.Row = 1;
            app.AutoSaveImg.Layout.Column = 3;
            app.AutoSaveImg.Text = '';

            % Create UpdateImages
            app.UpdateImages = uibutton(app.ShortcutButtonGrid, 'push');
            app.UpdateImages.ButtonPushedFcn = createCallbackFcn(app, @updateImagesCallbacks, true);
            app.UpdateImages.Icon = 'refresh.png';
            app.UpdateImages.Tooltip = {'Update Images (F5)'};
            app.UpdateImages.Layout.Row = 1;
            app.UpdateImages.Layout.Column = 4;
            app.UpdateImages.Text = '';

            % Create ShowSaveWdw
            app.ShowSaveWdw = uibutton(app.ShortcutButtonGrid, 'push');
            app.ShowSaveWdw.ButtonPushedFcn = createCallbackFcn(app, @saveCallbacks, true);
            app.ShowSaveWdw.Icon = 'save.png';
            app.ShowSaveWdw.Tooltip = {'Open the Saving/Export window'};
            app.ShowSaveWdw.Layout.Row = 1;
            app.ShowSaveWdw.Layout.Column = 2;
            app.ShowSaveWdw.Text = '';

            % Create ShowImportWdw
            app.ShowImportWdw = uibutton(app.ShortcutButtonGrid, 'push');
            app.ShowImportWdw.ButtonPushedFcn = createCallbackFcn(app, @importCallbacks, true);
            app.ShowImportWdw.Icon = 'import.png';
            app.ShowImportWdw.BackgroundColor = [0.702 1 0.702];
            app.ShowImportWdw.FontWeight = 'bold';
            app.ShowImportWdw.Tooltip = {'Import Data'};
            app.ShowImportWdw.Layout.Row = 1;
            app.ShowImportWdw.Layout.Column = 1;
            app.ShowImportWdw.Text = 'Import';

            % Create ShowSettingsWdw
            app.ShowSettingsWdw = uibutton(app.ShortcutButtonGrid, 'push');
            app.ShowSettingsWdw.ButtonPushedFcn = createCallbackFcn(app, @showWindowCallbacks, true);
            app.ShowSettingsWdw.Tag = 'Settings';
            app.ShowSettingsWdw.Icon = 'settings.png';
            app.ShowSettingsWdw.Tooltip = {'Show Detector Controls'};
            app.ShowSettingsWdw.Layout.Row = 1;
            app.ShowSettingsWdw.Layout.Column = 7;
            app.ShowSettingsWdw.Text = '';

            % Create DetectorModeGrid
            app.DetectorModeGrid = uigridlayout(app.Quant4D_FigGrid);
            app.DetectorModeGrid.ColumnWidth = {'1x', 'fit', 'fit', '1x'};
            app.DetectorModeGrid.RowHeight = {24};
            app.DetectorModeGrid.ColumnSpacing = 4;
            app.DetectorModeGrid.RowSpacing = 4;
            app.DetectorModeGrid.Padding = [0 0 0 0];
            app.DetectorModeGrid.Layout.Row = 2;
            app.DetectorModeGrid.Layout.Column = 1;

            % Create DetrMode
            app.DetrMode = uidropdown(app.DetectorModeGrid);
            app.DetrMode.Items = {'Import Preview', 'Alignment', 'Annular/Round', 'Segmented (DPC)', 'Center of Mass', 'Virtual Aperture', 'Custom Detectors'};
            app.DetrMode.ItemsData = {'PrvwMod', 'AlignMod', 'AnnMod', 'DPCMod', 'CoMMod', 'VrApMod', 'CustMod'};
            app.DetrMode.ValueChangedFcn = createCallbackFcn(app, @detectorModeCallbacks, true);
            app.DetrMode.Tooltip = {'Diffraction Detector Mode'};
            app.DetrMode.FontSize = 14;
            app.DetrMode.FontWeight = 'bold';
            app.DetrMode.Layout.Row = 1;
            app.DetrMode.Layout.Column = 3;
            app.DetrMode.Value = 'AlignMod';

            % Create DiffractionLabel
            app.DiffractionLabel = uilabel(app.DetectorModeGrid);
            app.DiffractionLabel.HorizontalAlignment = 'right';
            app.DiffractionLabel.FontSize = 14;
            app.DiffractionLabel.FontWeight = 'bold';
            app.DiffractionLabel.Layout.Row = 1;
            app.DiffractionLabel.Layout.Column = 2;
            app.DiffractionLabel.Text = 'Diffraction';

            % Create RealSpacePadGrid
            app.RealSpacePadGrid = uigridlayout(app.Quant4D_FigGrid);
            app.RealSpacePadGrid.ColumnWidth = {'1x'};
            app.RealSpacePadGrid.RowHeight = {'1x'};
            app.RealSpacePadGrid.ColumnSpacing = 4;
            app.RealSpacePadGrid.RowSpacing = 4;
            app.RealSpacePadGrid.Padding = [4 4 4 0];
            app.RealSpacePadGrid.Layout.Row = 4;
            app.RealSpacePadGrid.Layout.Column = 1;

            % Create RealSpacePanel
            app.RealSpacePanel = uipanel(app.RealSpacePadGrid);
            app.RealSpacePanel.AutoResizeChildren = 'off';
            app.RealSpacePanel.Tooltip = {'Real-space region of interest (ROI)'};
            app.RealSpacePanel.BorderType = 'none';
            app.RealSpacePanel.TitlePosition = 'centertop';
            app.RealSpacePanel.Title = 'Real-space Controls';
            app.RealSpacePanel.Layout.Row = 1;
            app.RealSpacePanel.Layout.Column = 1;
            app.RealSpacePanel.FontWeight = 'bold';
            app.RealSpacePanel.FontSize = 14;

            % Create RealSpaceGrid
            app.RealSpaceGrid = uigridlayout(app.RealSpacePanel);
            app.RealSpaceGrid.ColumnWidth = {'fit', '1x', 24, 24};
            app.RealSpaceGrid.RowHeight = {24, 24, 24};
            app.RealSpaceGrid.ColumnSpacing = 4;
            app.RealSpaceGrid.RowSpacing = 4;
            app.RealSpaceGrid.Padding = [0 0 0 4];

            % Create RealROIShape
            app.RealROIShape = uidropdown(app.RealSpaceGrid);
            app.RealROIShape.Items = {'Full Image', 'Point', 'Ellipse', 'Rectangle', 'Draw Polygon', 'From File'};
            app.RealROIShape.ItemsData = {'full', 'point', 'ellipse', 'rectangle', 'poly', 'file'};
            app.RealROIShape.ValueChangedFcn = createCallbackFcn(app, @realSpaceROICallbacks, true);
            app.RealROIShape.Layout.Row = 1;
            app.RealROIShape.Layout.Column = 2;
            app.RealROIShape.Value = 'full';

            % Create ROIShapeLabel
            app.ROIShapeLabel = uilabel(app.RealSpaceGrid);
            app.ROIShapeLabel.HorizontalAlignment = 'right';
            app.ROIShapeLabel.Layout.Row = 1;
            app.ROIShapeLabel.Layout.Column = 1;
            app.ROIShapeLabel.Text = 'ROI Shape';

            % Create ShowRealMaskWdw
            app.ShowRealMaskWdw = uibutton(app.RealSpaceGrid, 'push');
            app.ShowRealMaskWdw.ButtonPushedFcn = createCallbackFcn(app, @showWindowCallbacks, true);
            app.ShowRealMaskWdw.Tag = 'RealMask';
            app.ShowRealMaskWdw.Icon = 'Aperture.png';
            app.ShowRealMaskWdw.Tooltip = {'Show Real-space Mask'};
            app.ShowRealMaskWdw.Layout.Row = 1;
            app.ShowRealMaskWdw.Layout.Column = 4;
            app.ShowRealMaskWdw.Text = '';

            % Create RealROIInvert
            app.RealROIInvert = uibutton(app.RealSpaceGrid, 'state');
            app.RealROIInvert.ValueChangedFcn = createCallbackFcn(app, @realSpaceROICallbacks, true);
            app.RealROIInvert.Tooltip = {'Invert real-space mask'};
            app.RealROIInvert.Icon = 'invertColors.png';
            app.RealROIInvert.Text = '';
            app.RealROIInvert.Layout.Row = 1;
            app.RealROIInvert.Layout.Column = 3;

            % Create ShowColorWheelWdw
            app.ShowColorWheelWdw = uibutton(app.RealSpaceGrid, 'push');
            app.ShowColorWheelWdw.ButtonPushedFcn = createCallbackFcn(app, @showWindowCallbacks, true);
            app.ShowColorWheelWdw.Tag = 'ColorWheel';
            app.ShowColorWheelWdw.Icon = 'colorwheel.png';
            app.ShowColorWheelWdw.Tooltip = {'Show Color Wheel for Phase Vector Field Direction'};
            app.ShowColorWheelWdw.Layout.Row = 3;
            app.ShowColorWheelWdw.Layout.Column = 4;
            app.ShowColorWheelWdw.Text = '';

            % Create DispVecColor
            app.DispVecColor = uibutton(app.RealSpaceGrid, 'push');
            app.DispVecColor.ButtonPushedFcn = createCallbackFcn(app, @displayCallbacks, true);
            app.DispVecColor.Icon = 'colorPicker.png';
            app.DispVecColor.Tooltip = {'Change Vector Field color'};
            app.DispVecColor.Layout.Row = 3;
            app.DispVecColor.Layout.Column = 3;
            app.DispVecColor.Text = '';

            % Create DispVecFieldLabel
            app.DispVecFieldLabel = uilabel(app.RealSpaceGrid);
            app.DispVecFieldLabel.HorizontalAlignment = 'right';
            app.DispVecFieldLabel.Layout.Row = 3;
            app.DispVecFieldLabel.Layout.Column = 1;
            app.DispVecFieldLabel.Text = 'Vector Field';

            % Create DispVecField
            app.DispVecField = uidropdown(app.RealSpaceGrid);
            app.DispVecField.Items = {'None', '1:1', '1:2', '1:4', '1:8', '1:16'};
            app.DispVecField.ItemsData = [0 1 2 4 8 16];
            app.DispVecField.ValueChangedFcn = createCallbackFcn(app, @displayCallbacks, true);
            app.DispVecField.Tooltip = {'Plot vector field on the current selected Real-space image'};
            app.DispVecField.Layout.Row = 3;
            app.DispVecField.Layout.Column = 2;
            app.DispVecField.Value = 0;

            % Create FramePosLabel
            app.FramePosLabel = uilabel(app.RealSpaceGrid);
            app.FramePosLabel.HorizontalAlignment = 'right';
            app.FramePosLabel.Layout.Row = 2;
            app.FramePosLabel.Layout.Column = 1;
            app.FramePosLabel.Text = 'Frame';

            % Create RealSpacePosGrid
            app.RealSpacePosGrid = uigridlayout(app.RealSpaceGrid);
            app.RealSpacePosGrid.ColumnWidth = {'fit', '1x', 'fit', '1x'};
            app.RealSpacePosGrid.RowHeight = {24};
            app.RealSpacePosGrid.ColumnSpacing = 4;
            app.RealSpacePosGrid.RowSpacing = 4;
            app.RealSpacePosGrid.Padding = [0 0 0 0];
            app.RealSpacePosGrid.Layout.Row = 2;
            app.RealSpacePosGrid.Layout.Column = [2 4];

            % Create RealXLabel
            app.RealXLabel = uilabel(app.RealSpacePosGrid);
            app.RealXLabel.HorizontalAlignment = 'right';
            app.RealXLabel.Layout.Row = 1;
            app.RealXLabel.Layout.Column = 1;
            app.RealXLabel.Text = 'X';

            % Create FrameX
            app.FrameX = uispinner(app.RealSpacePosGrid);
            app.FrameX.ValueChangingFcn = createCallbackFcn(app, @realSpaceROICallbacks, true);
            app.FrameX.RoundFractionalValues = 'on';
            app.FrameX.ValueDisplayFormat = '%.0f';
            app.FrameX.ValueChangedFcn = createCallbackFcn(app, @realSpaceROICallbacks, true);
            app.FrameX.Layout.Row = 1;
            app.FrameX.Layout.Column = 2;

            % Create RealYLabel
            app.RealYLabel = uilabel(app.RealSpacePosGrid);
            app.RealYLabel.HorizontalAlignment = 'right';
            app.RealYLabel.Layout.Row = 1;
            app.RealYLabel.Layout.Column = 3;
            app.RealYLabel.Text = 'Y';

            % Create FrameY
            app.FrameY = uispinner(app.RealSpacePosGrid);
            app.FrameY.ValueChangingFcn = createCallbackFcn(app, @realSpaceROICallbacks, true);
            app.FrameY.RoundFractionalValues = 'on';
            app.FrameY.ValueDisplayFormat = '%.0f';
            app.FrameY.ValueChangedFcn = createCallbackFcn(app, @realSpaceROICallbacks, true);
            app.FrameY.Layout.Row = 1;
            app.FrameY.Layout.Column = 4;

            % Create DfrnDetrPanel
            app.DfrnDetrPanel = uipanel(app.Quant4D_FigGrid);
            app.DfrnDetrPanel.BorderType = 'none';
            app.DfrnDetrPanel.TitlePosition = 'centertop';
            app.DfrnDetrPanel.Layout.Row = 3;
            app.DfrnDetrPanel.Layout.Column = 1;

            % Create ImportPanel
            app.ImportPanel = uipanel(app.Quant4D_Fig);
            app.ImportPanel.AutoResizeChildren = 'off';
            app.ImportPanel.BorderType = 'none';
            app.ImportPanel.FontWeight = 'bold';
            app.ImportPanel.Position = [548 -27 600 500];

            % Create ImportGrid
            app.ImportGrid = uigridlayout(app.ImportPanel);
            app.ImportGrid.ColumnWidth = {'1x', '1.8x'};
            app.ImportGrid.RowHeight = {24, '1x', 24};
            app.ImportGrid.ColumnSpacing = 8;
            app.ImportGrid.RowSpacing = 4;
            app.ImportGrid.Padding = [4 4 4 4];

            % Create ImpFileGrid
            app.ImpFileGrid = uigridlayout(app.ImportGrid);
            app.ImpFileGrid.ColumnWidth = {'fit', '1x'};
            app.ImpFileGrid.RowHeight = {'1x'};
            app.ImpFileGrid.ColumnSpacing = 4;
            app.ImpFileGrid.Padding = [0 0 0 0];
            app.ImpFileGrid.Layout.Row = 1;
            app.ImpFileGrid.Layout.Column = [1 2];

            % Create ImpFileSelect
            app.ImpFileSelect = uibutton(app.ImpFileGrid, 'push');
            app.ImpFileSelect.ButtonPushedFcn = createCallbackFcn(app, @importSelectFile, true);
            app.ImpFileSelect.IconAlignment = 'center';
            app.ImpFileSelect.BackgroundColor = [0.702 1 0.702];
            app.ImpFileSelect.FontWeight = 'bold';
            app.ImpFileSelect.Layout.Row = 1;
            app.ImpFileSelect.Layout.Column = 1;
            app.ImpFileSelect.Text = 'Select';

            % Create ImpFilePath
            app.ImpFilePath = uieditfield(app.ImpFileGrid, 'text');
            app.ImpFilePath.ValueChangedFcn = createCallbackFcn(app, @importSelectFile, true);
            app.ImpFilePath.Layout.Row = 1;
            app.ImpFilePath.Layout.Column = 2;

            % Create ImpDatasetInfoPanel
            app.ImpDatasetInfoPanel = uipanel(app.ImportGrid);
            app.ImpDatasetInfoPanel.AutoResizeChildren = 'off';
            app.ImpDatasetInfoPanel.BorderType = 'none';
            app.ImpDatasetInfoPanel.TitlePosition = 'centertop';
            app.ImpDatasetInfoPanel.Title = 'Dataset Info';
            app.ImpDatasetInfoPanel.Layout.Row = [2 3];
            app.ImpDatasetInfoPanel.Layout.Column = 1;
            app.ImpDatasetInfoPanel.FontWeight = 'bold';
            app.ImpDatasetInfoPanel.FontSize = 14;

            % Create ImpDatasetInfoGrid
            app.ImpDatasetInfoGrid = uigridlayout(app.ImpDatasetInfoPanel);
            app.ImpDatasetInfoGrid.ColumnWidth = {'1x'};
            app.ImpDatasetInfoGrid.RowHeight = {48, 'fit', 'fit', 'fit', 'fit', '1x'};
            app.ImpDatasetInfoGrid.ColumnSpacing = 4;
            app.ImpDatasetInfoGrid.RowSpacing = 4;
            app.ImpDatasetInfoGrid.Padding = [0 0 0 4];

            % Create ImpFileTypeButtonGroup
            app.ImpFileTypeButtonGroup = uibuttongroup(app.ImpDatasetInfoGrid);
            app.ImpFileTypeButtonGroup.AutoResizeChildren = 'off';
            app.ImpFileTypeButtonGroup.SelectionChangedFcn = createCallbackFcn(app, @importFileType, true);
            app.ImpFileTypeButtonGroup.Tooltip = {'EMPAD'; '128x128 pixels'; 'Header: 0 bytes'; 'Footer: 1024 bytes'; '32-bit Real, Little endian'; ''; 'MEDIPIX'; '256x256 pixels'; 'Header: 384 bytes'; 'Footer: 0 bytes'; 'Unsigned integer, Big endian'; ''; 'MRC'; 'variable # of pixels'; 'Header: 1024 bytes'; 'Footer: 0 bytes'; 'Signed integer, Little endian'};
            app.ImpFileTypeButtonGroup.BorderType = 'none';
            app.ImpFileTypeButtonGroup.TitlePosition = 'centertop';
            app.ImpFileTypeButtonGroup.Layout.Row = 1;
            app.ImpFileTypeButtonGroup.Layout.Column = 1;
            app.ImpFileTypeButtonGroup.FontWeight = 'bold';

            % Create EMPADButton
            app.EMPADButton = uitogglebutton(app.ImpFileTypeButtonGroup);
            app.EMPADButton.Tooltip = {'*.raw'; '128x128 pixels'; 'Data Offset: 0 bytes'; 'Frame Header: 0 bytes'; 'Frame Footer: 1024 bytes'; '32-bit Real, Little Endian'};
            app.EMPADButton.Text = 'EMPAD';
            app.EMPADButton.Position = [3 27 68 22];
            app.EMPADButton.Value = true;

            % Create MedipixButton
            app.MedipixButton = uitogglebutton(app.ImpFileTypeButtonGroup);
            app.MedipixButton.Tooltip = {'*.mib'; '256x256 pixels'; 'Data Offset: 0 bytes'; 'Frame Header: 384 bytes'; 'Frame Footer: 0 bytes'; 'Unsigned integer, Big Endian'};
            app.MedipixButton.Text = 'Medipix';
            app.MedipixButton.Position = [71 27 68 22];

            % Create CustomButton
            app.CustomButton = uitogglebutton(app.ImpFileTypeButtonGroup);
            app.CustomButton.Tooltip = {'E.g. simulated/raw data'};
            app.CustomButton.Text = 'Custom';
            app.CustomButton.Position = [139 5 68 22];

            % Create MRCButton
            app.MRCButton = uitogglebutton(app.ImpFileTypeButtonGroup);
            app.MRCButton.Tooltip = {'*.mrc'; 'Data Offset: 1024 bytes'; 'Frame Header: 0 bytes'; 'Frame Footer: 0 bytes'; 'Signed integer, Little Endian'};
            app.MRCButton.Text = 'MRC';
            app.MRCButton.Position = [139 27 68 22];

            % Create DM34Button
            app.DM34Button = uitogglebutton(app.ImpFileTypeButtonGroup);
            app.DM34Button.Tooltip = {'Gatan *.dm3/*.dm4'};
            app.DM34Button.Text = 'DM3/4';
            app.DM34Button.Position = [3 5 68 22];

            % Create HDF5Button
            app.HDF5Button = uitogglebutton(app.ImpFileTypeButtonGroup);
            app.HDF5Button.Tooltip = {'*.h5/*.hdf5'};
            app.HDF5Button.Text = 'HDF5';
            app.HDF5Button.Position = [71 5 68 22];

            % Create ImpDatasetStructGrid
            app.ImpDatasetStructGrid = uigridlayout(app.ImpDatasetInfoGrid);
            app.ImpDatasetStructGrid.ColumnWidth = {'fit', '1x'};
            app.ImpDatasetStructGrid.RowHeight = {24, 24, 24, 24, 24, 24};
            app.ImpDatasetStructGrid.ColumnSpacing = 4;
            app.ImpDatasetStructGrid.RowSpacing = 2;
            app.ImpDatasetStructGrid.Padding = [0 0 0 0];
            app.ImpDatasetStructGrid.Layout.Row = 2;
            app.ImpDatasetStructGrid.Layout.Column = 1;

            % Create FrHead
            app.FrHead = uieditfield(app.ImpDatasetStructGrid, 'numeric');
            app.FrHead.Limits = [0 Inf];
            app.FrHead.ValueDisplayFormat = '%d bytes';
            app.FrHead.ValueChangedFcn = createCallbackFcn(app, @importBoxInput, true);
            app.FrHead.Tooltip = {'Number of bytes before the actual pattern in each frame (e.g. for metadata)'};
            app.FrHead.Layout.Row = 3;
            app.FrHead.Layout.Column = 2;

            % Create FrameHeaderLabel
            app.FrameHeaderLabel = uilabel(app.ImpDatasetStructGrid);
            app.FrameHeaderLabel.HorizontalAlignment = 'right';
            app.FrameHeaderLabel.Layout.Row = 3;
            app.FrameHeaderLabel.Layout.Column = 1;
            app.FrameHeaderLabel.Text = 'Frame Header';

            % Create FrFoot
            app.FrFoot = uieditfield(app.ImpDatasetStructGrid, 'numeric');
            app.FrFoot.Limits = [0 Inf];
            app.FrFoot.ValueDisplayFormat = '%d bytes';
            app.FrFoot.ValueChangedFcn = createCallbackFcn(app, @importBoxInput, true);
            app.FrFoot.Tooltip = {'Number of bytes after the actual pattern in each frame (e.g. for metadata)'};
            app.FrFoot.Layout.Row = 4;
            app.FrFoot.Layout.Column = 2;

            % Create FrameFooterLabel
            app.FrameFooterLabel = uilabel(app.ImpDatasetStructGrid);
            app.FrameFooterLabel.HorizontalAlignment = 'right';
            app.FrameFooterLabel.Layout.Row = 4;
            app.FrameFooterLabel.Layout.Column = 1;
            app.FrameFooterLabel.Text = 'Frame Footer';

            % Create DataOffset
            app.DataOffset = uieditfield(app.ImpDatasetStructGrid, 'numeric');
            app.DataOffset.Limits = [0 Inf];
            app.DataOffset.ValueDisplayFormat = '%d bytes';
            app.DataOffset.ValueChangedFcn = createCallbackFcn(app, @importBoxInput, true);
            app.DataOffset.Tooltip = {'Number of bytes before the image stack in file (e.g. for metadata)'};
            app.DataOffset.Layout.Row = 2;
            app.DataOffset.Layout.Column = 2;

            % Create DataOffsetLabel
            app.DataOffsetLabel = uilabel(app.ImpDatasetStructGrid);
            app.DataOffsetLabel.HorizontalAlignment = 'right';
            app.DataOffsetLabel.Layout.Row = 2;
            app.DataOffsetLabel.Layout.Column = 1;
            app.DataOffsetLabel.Text = 'Data Offset';

            % Create ImpDataType
            app.ImpDataType = uidropdown(app.ImpDatasetStructGrid);
            app.ImpDataType.Items = {};
            app.ImpDataType.ValueChangedFcn = createCallbackFcn(app, @importBoxInput, true);
            app.ImpDataType.Layout.Row = 5;
            app.ImpDataType.Layout.Column = 2;
            app.ImpDataType.Value = {};

            % Create DataTypeLabel
            app.DataTypeLabel = uilabel(app.ImpDatasetStructGrid);
            app.DataTypeLabel.HorizontalAlignment = 'right';
            app.DataTypeLabel.Layout.Row = 5;
            app.DataTypeLabel.Layout.Column = 1;
            app.DataTypeLabel.Text = 'Data Type';

            % Create ImpByteOrder
            app.ImpByteOrder = uidropdown(app.ImpDatasetStructGrid);
            app.ImpByteOrder.Items = {'Little Endian', 'Big Endian'};
            app.ImpByteOrder.ItemsData = {'l', 'b'};
            app.ImpByteOrder.ValueChangedFcn = createCallbackFcn(app, @importBoxInput, true);
            app.ImpByteOrder.Layout.Row = 6;
            app.ImpByteOrder.Layout.Column = 2;
            app.ImpByteOrder.Value = 'l';

            % Create ByteOrderDropDownLabel
            app.ByteOrderDropDownLabel = uilabel(app.ImpDatasetStructGrid);
            app.ByteOrderDropDownLabel.HorizontalAlignment = 'right';
            app.ByteOrderDropDownLabel.Layout.Row = 6;
            app.ByteOrderDropDownLabel.Layout.Column = 1;
            app.ByteOrderDropDownLabel.Text = 'Byte Order';

            % Create ImpSubImg
            app.ImpSubImg = uidropdown(app.ImpDatasetStructGrid);
            app.ImpSubImg.Items = {};
            app.ImpSubImg.ValueChangedFcn = createCallbackFcn(app, @importFileType, true);
            app.ImpSubImg.Tooltip = {'Some file formats (e.g. DM3, DM4 or HDF5) can contain multiple image-stacks in one file'};
            app.ImpSubImg.Layout.Row = 1;
            app.ImpSubImg.Layout.Column = 2;
            app.ImpSubImg.Value = {};

            % Create SubdatasetDropDownLabel
            app.SubdatasetDropDownLabel = uilabel(app.ImpDatasetStructGrid);
            app.SubdatasetDropDownLabel.HorizontalAlignment = 'right';
            app.SubdatasetDropDownLabel.Layout.Row = 1;
            app.SubdatasetDropDownLabel.Layout.Column = 1;
            app.SubdatasetDropDownLabel.Text = 'Sub-dataset';

            % Create ImpDimensionGrid
            app.ImpDimensionGrid = uigridlayout(app.ImpDatasetInfoGrid);
            app.ImpDimensionGrid.ColumnWidth = {'fit', 'fit', '1x', 'fit', '1x'};
            app.ImpDimensionGrid.RowHeight = {24, 24};
            app.ImpDimensionGrid.ColumnSpacing = 4;
            app.ImpDimensionGrid.RowSpacing = 4;
            app.ImpDimensionGrid.Padding = [0 0 0 0];
            app.ImpDimensionGrid.Layout.Row = 3;
            app.ImpDimensionGrid.Layout.Column = 1;

            % Create DNPxX
            app.DNPxX = uieditfield(app.ImpDimensionGrid, 'numeric');
            app.DNPxX.Limits = [1 Inf];
            app.DNPxX.RoundFractionalValues = 'on';
            app.DNPxX.ValueDisplayFormat = '%d';
            app.DNPxX.ValueChangedFcn = createCallbackFcn(app, @importBoxInput, true);
            app.DNPxX.Tag = 'Import Dfrn';
            app.DNPxX.HorizontalAlignment = 'center';
            app.DNPxX.Tooltip = {'Number of pixels on X axis in each frame (1st dimension of image stack)'};
            app.DNPxX.Layout.Row = 1;
            app.DNPxX.Layout.Column = 3;
            app.DNPxX.Value = 1;

            % Create XLabel_2
            app.XLabel_2 = uilabel(app.ImpDimensionGrid);
            app.XLabel_2.HorizontalAlignment = 'right';
            app.XLabel_2.Layout.Row = 1;
            app.XLabel_2.Layout.Column = 2;
            app.XLabel_2.Text = 'X';

            % Create DNPxY
            app.DNPxY = uieditfield(app.ImpDimensionGrid, 'numeric');
            app.DNPxY.Limits = [1 Inf];
            app.DNPxY.RoundFractionalValues = 'on';
            app.DNPxY.ValueDisplayFormat = '%d';
            app.DNPxY.ValueChangedFcn = createCallbackFcn(app, @importBoxInput, true);
            app.DNPxY.Tag = 'Import Dfrn';
            app.DNPxY.HorizontalAlignment = 'center';
            app.DNPxY.Tooltip = {'Number of pixels on Y axis in each frame (2nd dimension of image stack)'};
            app.DNPxY.Layout.Row = 1;
            app.DNPxY.Layout.Column = 5;
            app.DNPxY.Value = 1;

            % Create YLabel_2
            app.YLabel_2 = uilabel(app.ImpDimensionGrid);
            app.YLabel_2.HorizontalAlignment = 'right';
            app.YLabel_2.Layout.Row = 1;
            app.YLabel_2.Layout.Column = 4;
            app.YLabel_2.Text = ' Y';

            % Create ImpDfrnResolutionLabel
            app.ImpDfrnResolutionLabel = uilabel(app.ImpDimensionGrid);
            app.ImpDfrnResolutionLabel.HorizontalAlignment = 'center';
            app.ImpDfrnResolutionLabel.FontWeight = 'bold';
            app.ImpDfrnResolutionLabel.Layout.Row = 1;
            app.ImpDfrnResolutionLabel.Layout.Column = 1;
            app.ImpDfrnResolutionLabel.Text = 'Pixels';

            % Create ImpNumFramesLabel
            app.ImpNumFramesLabel = uilabel(app.ImpDimensionGrid);
            app.ImpNumFramesLabel.HorizontalAlignment = 'center';
            app.ImpNumFramesLabel.FontWeight = 'bold';
            app.ImpNumFramesLabel.Layout.Row = 2;
            app.ImpNumFramesLabel.Layout.Column = 1;
            app.ImpNumFramesLabel.Text = 'Frames';

            % Create XLabel
            app.XLabel = uilabel(app.ImpDimensionGrid);
            app.XLabel.HorizontalAlignment = 'right';
            app.XLabel.Layout.Row = 2;
            app.XLabel.Layout.Column = 2;
            app.XLabel.Text = 'X';

            % Create DNFrX
            app.DNFrX = uieditfield(app.ImpDimensionGrid, 'numeric');
            app.DNFrX.Limits = [1 Inf];
            app.DNFrX.RoundFractionalValues = 'on';
            app.DNFrX.ValueDisplayFormat = '%d';
            app.DNFrX.ValueChangedFcn = createCallbackFcn(app, @importBoxInput, true);
            app.DNFrX.Tag = 'Import Real';
            app.DNFrX.HorizontalAlignment = 'center';
            app.DNFrX.Tooltip = {'Number of frames on X axis (3rd dimension of image stack)'};
            app.DNFrX.Layout.Row = 2;
            app.DNFrX.Layout.Column = 3;
            app.DNFrX.Value = 1;

            % Create YLabel
            app.YLabel = uilabel(app.ImpDimensionGrid);
            app.YLabel.HorizontalAlignment = 'right';
            app.YLabel.Layout.Row = 2;
            app.YLabel.Layout.Column = 4;
            app.YLabel.Text = ' Y';

            % Create DNFrY
            app.DNFrY = uieditfield(app.ImpDimensionGrid, 'numeric');
            app.DNFrY.Limits = [1 Inf];
            app.DNFrY.RoundFractionalValues = 'on';
            app.DNFrY.ValueDisplayFormat = '%d';
            app.DNFrY.ValueChangedFcn = createCallbackFcn(app, @importBoxInput, true);
            app.DNFrY.Tag = 'Import Real';
            app.DNFrY.HorizontalAlignment = 'center';
            app.DNFrY.Tooltip = {'Number of frames on Y axis (4th dimension of image stack)'};
            app.DNFrY.Layout.Row = 2;
            app.DNFrY.Layout.Column = 5;
            app.DNFrY.Value = 1;

            % Create ImpFileSizeGrid
            app.ImpFileSizeGrid = uigridlayout(app.ImpDatasetInfoGrid);
            app.ImpFileSizeGrid.ColumnWidth = {'fit', '1x'};
            app.ImpFileSizeGrid.RowHeight = {'fit', 'fit'};
            app.ImpFileSizeGrid.ColumnSpacing = 4;
            app.ImpFileSizeGrid.RowSpacing = 2;
            app.ImpFileSizeGrid.Padding = [0 0 0 0];
            app.ImpFileSizeGrid.Layout.Row = 4;
            app.ImpFileSizeGrid.Layout.Column = 1;

            % Create ImpEstFilesizeLabel
            app.ImpEstFilesizeLabel = uilabel(app.ImpFileSizeGrid);
            app.ImpEstFilesizeLabel.HorizontalAlignment = 'right';
            app.ImpEstFilesizeLabel.Layout.Row = 2;
            app.ImpEstFilesizeLabel.Layout.Column = 1;
            app.ImpEstFilesizeLabel.Text = 'Est.:';

            % Create ImpActualFilesizeLabel
            app.ImpActualFilesizeLabel = uilabel(app.ImpFileSizeGrid);
            app.ImpActualFilesizeLabel.HorizontalAlignment = 'right';
            app.ImpActualFilesizeLabel.Layout.Row = 1;
            app.ImpActualFilesizeLabel.Layout.Column = 1;
            app.ImpActualFilesizeLabel.Text = 'Size:';

            % Create ImpEstFilesize
            app.ImpEstFilesize = uilabel(app.ImpFileSizeGrid);
            app.ImpEstFilesize.HorizontalAlignment = 'center';
            app.ImpEstFilesize.Tooltip = {'File size calculated from info above. Size after the image stack (the "data tail") is implicit, thus may not be accurate'};
            app.ImpEstFilesize.Layout.Row = 2;
            app.ImpEstFilesize.Layout.Column = 2;
            app.ImpEstFilesize.Text = '';

            % Create ImpActualFilesize
            app.ImpActualFilesize = uilabel(app.ImpFileSizeGrid);
            app.ImpActualFilesize.HorizontalAlignment = 'center';
            app.ImpActualFilesize.Tooltip = {'Actual physical file size'};
            app.ImpActualFilesize.Layout.Row = 1;
            app.ImpActualFilesize.Layout.Column = 2;
            app.ImpActualFilesize.Text = '';

            % Create DatasetInfofromMetadataLabel
            app.DatasetInfofromMetadataLabel = uilabel(app.ImpDatasetInfoGrid);
            app.DatasetInfofromMetadataLabel.HorizontalAlignment = 'center';
            app.DatasetInfofromMetadataLabel.VerticalAlignment = 'bottom';
            app.DatasetInfofromMetadataLabel.FontWeight = 'bold';
            app.DatasetInfofromMetadataLabel.Layout.Row = 5;
            app.DatasetInfofromMetadataLabel.Layout.Column = 1;
            app.DatasetInfofromMetadataLabel.Text = 'Dataset Info from Metadata';

            % Create ImpFileMetaNotes
            app.ImpFileMetaNotes = uitextarea(app.ImpDatasetInfoGrid);
            app.ImpFileMetaNotes.Editable = 'off';
            app.ImpFileMetaNotes.Layout.Row = 6;
            app.ImpFileMetaNotes.Layout.Column = 1;

            % Create ImportOptionsPanel
            app.ImportOptionsPanel = uipanel(app.ImportGrid);
            app.ImportOptionsPanel.AutoResizeChildren = 'off';
            app.ImportOptionsPanel.BorderType = 'none';
            app.ImportOptionsPanel.TitlePosition = 'centertop';
            app.ImportOptionsPanel.Title = 'Import Options';
            app.ImportOptionsPanel.Layout.Row = 2;
            app.ImportOptionsPanel.Layout.Column = 2;
            app.ImportOptionsPanel.FontWeight = 'bold';
            app.ImportOptionsPanel.FontSize = 14;

            % Create ImportOptionsGrid
            app.ImportOptionsGrid = uigridlayout(app.ImportOptionsPanel);
            app.ImportOptionsGrid.RowHeight = {24, 'fit', 'fit', 'fit', '1x'};
            app.ImportOptionsGrid.ColumnSpacing = 6;
            app.ImportOptionsGrid.RowSpacing = 6;
            app.ImportOptionsGrid.Padding = [0 0 0 4];

            % Create ImpNotes
            app.ImpNotes = uitextarea(app.ImportOptionsGrid);
            app.ImpNotes.Editable = 'off';
            app.ImpNotes.Layout.Row = 5;
            app.ImpNotes.Layout.Column = [1 2];

            % Create ImportSummaryLabel
            app.ImportSummaryLabel = uilabel(app.ImportOptionsGrid);
            app.ImportSummaryLabel.HorizontalAlignment = 'center';
            app.ImportSummaryLabel.VerticalAlignment = 'bottom';
            app.ImportSummaryLabel.FontWeight = 'bold';
            app.ImportSummaryLabel.Layout.Row = 4;
            app.ImportSummaryLabel.Layout.Column = [1 2];
            app.ImportSummaryLabel.Text = 'Import Summary';

            % Create ImportPxRangeGrid
            app.ImportPxRangeGrid = uigridlayout(app.ImportOptionsGrid);
            app.ImportPxRangeGrid.ColumnWidth = {'fit', '1x', 'fit', '1x'};
            app.ImportPxRangeGrid.RowHeight = {24, 24, 24};
            app.ImportPxRangeGrid.ColumnSpacing = 4;
            app.ImportPxRangeGrid.RowSpacing = 2;
            app.ImportPxRangeGrid.Padding = [0 0 0 0];
            app.ImportPxRangeGrid.Layout.Row = 3;
            app.ImportPxRangeGrid.Layout.Column = 1;

            % Create xsub1Label_5
            app.xsub1Label_5 = uilabel(app.ImportPxRangeGrid);
            app.xsub1Label_5.HorizontalAlignment = 'right';
            app.xsub1Label_5.Layout.Row = 2;
            app.xsub1Label_5.Layout.Column = 1;
            app.xsub1Label_5.Text = 'x<sub>1';

            % Create IPxX1
            app.IPxX1 = uispinner(app.ImportPxRangeGrid);
            app.IPxX1.ValueChangingFcn = createCallbackFcn(app, @importBoxInput, true);
            app.IPxX1.RoundFractionalValues = 'on';
            app.IPxX1.ValueDisplayFormat = '%.0f';
            app.IPxX1.ValueChangedFcn = createCallbackFcn(app, @importBoxInput, true);
            app.IPxX1.Tag = 'Import Dfrn';
            app.IPxX1.Tooltip = {'Starting pixel on X (1st dimension of image stack) to import, in each frame'};
            app.IPxX1.Layout.Row = 2;
            app.IPxX1.Layout.Column = 2;
            app.IPxX1.Value = 1;

            % Create XLabel_3
            app.XLabel_3 = uilabel(app.ImportPxRangeGrid);
            app.XLabel_3.HorizontalAlignment = 'right';
            app.XLabel_3.Layout.Row = 3;
            app.XLabel_3.Layout.Column = 1;
            app.XLabel_3.Text = 'X';

            % Create INPxX
            app.INPxX = uispinner(app.ImportPxRangeGrid);
            app.INPxX.ValueChangingFcn = createCallbackFcn(app, @importBoxInput, true);
            app.INPxX.RoundFractionalValues = 'on';
            app.INPxX.ValueDisplayFormat = '%.0f';
            app.INPxX.ValueChangedFcn = createCallbackFcn(app, @importBoxInput, true);
            app.INPxX.Tag = 'Import Dfrn';
            app.INPxX.Tooltip = {'Total pixels after binning on X (1st dimension of image stack), in each frame'};
            app.INPxX.Layout.Row = 3;
            app.INPxX.Layout.Column = 2;
            app.INPxX.Value = 1;

            % Create ysub1Label_5
            app.ysub1Label_5 = uilabel(app.ImportPxRangeGrid);
            app.ysub1Label_5.HorizontalAlignment = 'right';
            app.ysub1Label_5.Layout.Row = 2;
            app.ysub1Label_5.Layout.Column = 3;
            app.ysub1Label_5.Text = 'y<sub>1';

            % Create IPxY1
            app.IPxY1 = uispinner(app.ImportPxRangeGrid);
            app.IPxY1.ValueChangingFcn = createCallbackFcn(app, @importBoxInput, true);
            app.IPxY1.RoundFractionalValues = 'on';
            app.IPxY1.ValueDisplayFormat = '%.0f';
            app.IPxY1.ValueChangedFcn = createCallbackFcn(app, @importBoxInput, true);
            app.IPxY1.Tag = 'Import Dfrn';
            app.IPxY1.Tooltip = {'Starting pixel on Y (2nd dimension of image stack) to import, in each frame'};
            app.IPxY1.Layout.Row = 2;
            app.IPxY1.Layout.Column = 4;
            app.IPxY1.Value = 1;

            % Create YLabel_3
            app.YLabel_3 = uilabel(app.ImportPxRangeGrid);
            app.YLabel_3.HorizontalAlignment = 'right';
            app.YLabel_3.Layout.Row = 3;
            app.YLabel_3.Layout.Column = 3;
            app.YLabel_3.Text = 'Y';

            % Create INPxY
            app.INPxY = uispinner(app.ImportPxRangeGrid);
            app.INPxY.ValueChangingFcn = createCallbackFcn(app, @importBoxInput, true);
            app.INPxY.RoundFractionalValues = 'on';
            app.INPxY.ValueDisplayFormat = '%.0f';
            app.INPxY.ValueChangedFcn = createCallbackFcn(app, @importBoxInput, true);
            app.INPxY.Tag = 'Import Dfrn';
            app.INPxY.Tooltip = {'Total pixels after binning on Y (2nd dimension of image stack), in each frame'};
            app.INPxY.Layout.Row = 3;
            app.INPxY.Layout.Column = 4;
            app.INPxY.Value = 1;

            % Create IPxD
            app.IPxD = uispinner(app.ImportPxRangeGrid);
            app.IPxD.ValueChangingFcn = createCallbackFcn(app, @importBoxInput, true);
            app.IPxD.RoundFractionalValues = 'on';
            app.IPxD.ValueDisplayFormat = '%.0f';
            app.IPxD.ValueChangedFcn = createCallbackFcn(app, @importBoxInput, true);
            app.IPxD.Tag = 'Import Dfrn';
            app.IPxD.Tooltip = {'To bin n×n pixels into one (by averaging)'};
            app.IPxD.Layout.Row = 1;
            app.IPxD.Layout.Column = 4;
            app.IPxD.Value = 1;

            % Create BinningDistanceLabel
            app.BinningDistanceLabel = uilabel(app.ImportPxRangeGrid);
            app.BinningDistanceLabel.HorizontalAlignment = 'right';
            app.BinningDistanceLabel.Layout.Row = 1;
            app.BinningDistanceLabel.Layout.Column = [1 3];
            app.BinningDistanceLabel.Text = 'Binning Distance';

            % Create ImportFrRangeGrid
            app.ImportFrRangeGrid = uigridlayout(app.ImportOptionsGrid);
            app.ImportFrRangeGrid.ColumnWidth = {'fit', '1x', 'fit', '1x'};
            app.ImportFrRangeGrid.RowHeight = {24, 24, 24};
            app.ImportFrRangeGrid.ColumnSpacing = 4;
            app.ImportFrRangeGrid.RowSpacing = 2;
            app.ImportFrRangeGrid.Padding = [0 0 0 0];
            app.ImportFrRangeGrid.Layout.Row = 3;
            app.ImportFrRangeGrid.Layout.Column = 2;

            % Create INFrYl
            app.INFrYl = uilabel(app.ImportFrRangeGrid);
            app.INFrYl.HorizontalAlignment = 'right';
            app.INFrYl.Layout.Row = 3;
            app.INFrYl.Layout.Column = 3;
            app.INFrYl.Text = 'Y';

            % Create INFrY
            app.INFrY = uispinner(app.ImportFrRangeGrid);
            app.INFrY.ValueChangingFcn = createCallbackFcn(app, @importBoxInput, true);
            app.INFrY.RoundFractionalValues = 'on';
            app.INFrY.ValueDisplayFormat = '%.0f';
            app.INFrY.ValueChangedFcn = createCallbackFcn(app, @importBoxInput, true);
            app.INFrY.Tag = 'Import Real';
            app.INFrY.Tooltip = {'Total frames after sampling on Y (4th dimension of image stack)'};
            app.INFrY.Layout.Row = 3;
            app.INFrY.Layout.Column = 4;
            app.INFrY.Value = 1;

            % Create xsub1Label_6
            app.xsub1Label_6 = uilabel(app.ImportFrRangeGrid);
            app.xsub1Label_6.HorizontalAlignment = 'right';
            app.xsub1Label_6.Layout.Row = 2;
            app.xsub1Label_6.Layout.Column = 1;
            app.xsub1Label_6.Text = 'x<sub>1';

            % Create IFrX1
            app.IFrX1 = uispinner(app.ImportFrRangeGrid);
            app.IFrX1.ValueChangingFcn = createCallbackFcn(app, @importBoxInput, true);
            app.IFrX1.RoundFractionalValues = 'on';
            app.IFrX1.ValueDisplayFormat = '%.0f';
            app.IFrX1.ValueChangedFcn = createCallbackFcn(app, @importBoxInput, true);
            app.IFrX1.Tag = 'Import Real';
            app.IFrX1.Tooltip = {'Starting frame on X (3rd dimension of image stack) to import'};
            app.IFrX1.Layout.Row = 2;
            app.IFrX1.Layout.Column = 2;
            app.IFrX1.Value = 1;

            % Create INFrXl
            app.INFrXl = uilabel(app.ImportFrRangeGrid);
            app.INFrXl.HorizontalAlignment = 'right';
            app.INFrXl.Layout.Row = 3;
            app.INFrXl.Layout.Column = 1;
            app.INFrXl.Text = 'X';

            % Create INFrX
            app.INFrX = uispinner(app.ImportFrRangeGrid);
            app.INFrX.ValueChangingFcn = createCallbackFcn(app, @importBoxInput, true);
            app.INFrX.RoundFractionalValues = 'on';
            app.INFrX.ValueDisplayFormat = '%.0f';
            app.INFrX.ValueChangedFcn = createCallbackFcn(app, @importBoxInput, true);
            app.INFrX.Tag = 'Import Real';
            app.INFrX.Tooltip = {'Total frames after sampling on X (3rd dimension of image stack)'};
            app.INFrX.Layout.Row = 3;
            app.INFrX.Layout.Column = 2;
            app.INFrX.Value = 1;

            % Create ysub1Label_6
            app.ysub1Label_6 = uilabel(app.ImportFrRangeGrid);
            app.ysub1Label_6.HorizontalAlignment = 'right';
            app.ysub1Label_6.Layout.Row = 2;
            app.ysub1Label_6.Layout.Column = 3;
            app.ysub1Label_6.Text = 'y<sub>1';

            % Create IFrY1
            app.IFrY1 = uispinner(app.ImportFrRangeGrid);
            app.IFrY1.ValueChangingFcn = createCallbackFcn(app, @importBoxInput, true);
            app.IFrY1.RoundFractionalValues = 'on';
            app.IFrY1.ValueDisplayFormat = '%.0f';
            app.IFrY1.ValueChangedFcn = createCallbackFcn(app, @importBoxInput, true);
            app.IFrY1.Tag = 'Import Real';
            app.IFrY1.Tooltip = {'Starting frame on Y (4th dimension of image stack) to import'};
            app.IFrY1.Layout.Row = 2;
            app.IFrY1.Layout.Column = 4;
            app.IFrY1.Value = 1;

            % Create IFrD
            app.IFrD = uispinner(app.ImportFrRangeGrid);
            app.IFrD.ValueChangingFcn = createCallbackFcn(app, @importBoxInput, true);
            app.IFrD.RoundFractionalValues = 'on';
            app.IFrD.ValueDisplayFormat = '%.0f';
            app.IFrD.ValueChangedFcn = createCallbackFcn(app, @importBoxInput, true);
            app.IFrD.Tag = 'Import Real';
            app.IFrD.Tooltip = {'Distance between sampling frames in both X & Y directions (neighboring frames have distance of 1)'};
            app.IFrD.Layout.Row = 1;
            app.IFrD.Layout.Column = 4;
            app.IFrD.Value = 1;

            % Create SamplingIntervalLabel_2
            app.SamplingIntervalLabel_2 = uilabel(app.ImportFrRangeGrid);
            app.SamplingIntervalLabel_2.HorizontalAlignment = 'right';
            app.SamplingIntervalLabel_2.Layout.Row = 1;
            app.SamplingIntervalLabel_2.Layout.Column = [1 3];
            app.SamplingIntervalLabel_2.Text = 'Sampling Interval';

            % Create ImpPxPart
            app.ImpPxPart = uicheckbox(app.ImportOptionsGrid);
            app.ImpPxPart.ValueChangedFcn = createCallbackFcn(app, @importBoxInput, true);
            app.ImpPxPart.Tag = 'Import Dfrn';
            app.ImpPxPart.Text = '    Pixels Partial Import';
            app.ImpPxPart.FontWeight = 'bold';
            app.ImpPxPart.Layout.Row = 2;
            app.ImpPxPart.Layout.Column = 1;

            % Create ImpFrPart
            app.ImpFrPart = uicheckbox(app.ImportOptionsGrid);
            app.ImpFrPart.ValueChangedFcn = createCallbackFcn(app, @importBoxInput, true);
            app.ImpFrPart.Tag = 'Import Real';
            app.ImpFrPart.Text = '    Frames Partial Import';
            app.ImpFrPart.FontWeight = 'bold';
            app.ImpFrPart.Layout.Row = 2;
            app.ImpFrPart.Layout.Column = 2;

            % Create ImpMemGrid
            app.ImpMemGrid = uigridlayout(app.ImportOptionsGrid);
            app.ImpMemGrid.ColumnWidth = {'fit', '1x'};
            app.ImpMemGrid.RowHeight = {'1x'};
            app.ImpMemGrid.ColumnSpacing = 8;
            app.ImpMemGrid.RowSpacing = 4;
            app.ImpMemGrid.Padding = [0 0 0 0];
            app.ImpMemGrid.Layout.Row = 1;
            app.ImpMemGrid.Layout.Column = [1 2];

            % Create ImpGPU
            app.ImpGPU = uidropdown(app.ImpMemGrid);
            app.ImpGPU.Items = {'GPU off'};
            app.ImpGPU.ValueChangedFcn = createCallbackFcn(app, @importBoxInput, true);
            app.ImpGPU.Tooltip = {'GPU acceleration'};
            app.ImpGPU.Layout.Row = 1;
            app.ImpGPU.Layout.Column = 2;
            app.ImpGPU.Value = 'GPU off';

            % Create ImpMemType
            app.ImpMemType = uidropdown(app.ImpMemGrid);
            app.ImpMemType.Items = {'Physical Memory', 'Virtual Mapping'};
            app.ImpMemType.Tooltip = {'VIRTUAL MEMORY is best for most large datasets as it does not physically load the dataset into RAM. This can be significantly faster depending on drive speed and file size. HOWEVER - it is currently only beneficial for datasets with no header of footer.'; ''; 'Virtual mapping to the GPU is not recommended at this point. It is extremely fast to load, but still requires significant GPU memory resources.'};
            app.ImpMemType.Layout.Row = 1;
            app.ImpMemType.Layout.Column = 1;
            app.ImpMemType.Value = 'Physical Memory';

            % Create ImportButtonGrid
            app.ImportButtonGrid = uigridlayout(app.ImportGrid);
            app.ImportButtonGrid.ColumnWidth = {'1x', '1x', '1x'};
            app.ImportButtonGrid.RowHeight = {24};
            app.ImportButtonGrid.ColumnSpacing = 4;
            app.ImportButtonGrid.RowSpacing = 4;
            app.ImportButtonGrid.Padding = [0 0 0 0];
            app.ImportButtonGrid.Layout.Row = 3;
            app.ImportButtonGrid.Layout.Column = 2;

            % Create ImportDataButton
            app.ImportDataButton = uibutton(app.ImportButtonGrid, 'push');
            app.ImportDataButton.ButtonPushedFcn = createCallbackFcn(app, @importCallbacks, true);
            app.ImportDataButton.FontWeight = 'bold';
            app.ImportDataButton.Layout.Row = 1;
            app.ImportDataButton.Layout.Column = 1;
            app.ImportDataButton.Text = 'Import Data';

            % Create ImportCancelButton
            app.ImportCancelButton = uibutton(app.ImportButtonGrid, 'push');
            app.ImportCancelButton.ButtonPushedFcn = createCallbackFcn(app, @importCallbacks, true);
            app.ImportCancelButton.FontWeight = 'bold';
            app.ImportCancelButton.Layout.Row = 1;
            app.ImportCancelButton.Layout.Column = 3;
            app.ImportCancelButton.Text = 'Cancel';

            % Create ImpKeepP
            app.ImpKeepP = uicheckbox(app.ImportButtonGrid);
            app.ImpKeepP.ValueChangedFcn = createCallbackFcn(app, @importBoxInput, true);
            app.ImpKeepP.Tooltip = {'Keep all current parameters/alignments/setups, and swap the already-imported dataset with another with exact (import) dimensions/datatype'};
            app.ImpKeepP.Text = 'Swap Dataset';
            app.ImpKeepP.Layout.Row = 1;
            app.ImpKeepP.Layout.Column = 2;

            % Create SettingsPanel
            app.SettingsPanel = uipanel(app.Quant4D_Fig);
            app.SettingsPanel.AutoResizeChildren = 'off';
            app.SettingsPanel.BorderType = 'none';
            app.SettingsPanel.TitlePosition = 'centertop';
            app.SettingsPanel.FontWeight = 'bold';
            app.SettingsPanel.Position = [280 61 260 408];

            % Create SettingsGrid
            app.SettingsGrid = uigridlayout(app.SettingsPanel);
            app.SettingsGrid.ColumnWidth = {'1x'};
            app.SettingsGrid.RowHeight = {'1x'};
            app.SettingsGrid.ColumnSpacing = 4;
            app.SettingsGrid.RowSpacing = 4;
            app.SettingsGrid.Padding = [0 0 0 0];

            % Create SettingsTabGroup
            app.SettingsTabGroup = uitabgroup(app.SettingsGrid);
            app.SettingsTabGroup.AutoResizeChildren = 'off';
            app.SettingsTabGroup.Layout.Row = 1;
            app.SettingsTabGroup.Layout.Column = 1;

            % Create DisplayTab
            app.DisplayTab = uitab(app.SettingsTabGroup);
            app.DisplayTab.Title = 'Display';

            % Create DisplayGrid
            app.DisplayGrid = uigridlayout(app.DisplayTab);
            app.DisplayGrid.ColumnWidth = {'1x'};
            app.DisplayGrid.RowHeight = {'fit', 46, '1x', 'fit'};
            app.DisplayGrid.ColumnSpacing = 4;
            app.DisplayGrid.RowSpacing = 4;
            app.DisplayGrid.Padding = [4 4 4 4];

            % Create DisplayDropDownGrid
            app.DisplayDropDownGrid = uigridlayout(app.DisplayGrid);
            app.DisplayDropDownGrid.ColumnWidth = {24, 'fit', '1x', 24};
            app.DisplayDropDownGrid.RowHeight = {24, 24};
            app.DisplayDropDownGrid.ColumnSpacing = 4;
            app.DisplayDropDownGrid.RowSpacing = 4;
            app.DisplayDropDownGrid.Padding = [0 0 0 0];
            app.DisplayDropDownGrid.Layout.Row = 1;
            app.DisplayDropDownGrid.Layout.Column = 1;

            % Create DispCMap
            app.DispCMap = uidropdown(app.DisplayDropDownGrid);
            app.DispCMap.Items = {'gray', 'hsv', 'jet', 'parula', 'hot', 'cool', 'spring', 'summer', 'autumn', 'winter', 'bone', 'copper', 'pink'};
            app.DispCMap.ValueChangedFcn = createCallbackFcn(app, @displayCallbacks, true);
            app.DispCMap.Layout.Row = 2;
            app.DispCMap.Layout.Column = 3;
            app.DispCMap.Value = 'gray';

            % Create ColormapLabel
            app.ColormapLabel = uilabel(app.DisplayDropDownGrid);
            app.ColormapLabel.HorizontalAlignment = 'right';
            app.ColormapLabel.Layout.Row = 2;
            app.ColormapLabel.Layout.Column = [1 2];
            app.ColormapLabel.Text = 'Colormap';

            % Create DispCMapInvert
            app.DispCMapInvert = uibutton(app.DisplayDropDownGrid, 'state');
            app.DispCMapInvert.ValueChangedFcn = createCallbackFcn(app, @displayCallbacks, true);
            app.DispCMapInvert.Tooltip = {'Invert colormap'};
            app.DispCMapInvert.Icon = 'invertColors.png';
            app.DispCMapInvert.Text = '';
            app.DispCMapInvert.Layout.Row = 2;
            app.DispCMapInvert.Layout.Column = 4;

            % Create DispImage
            app.DispImage = uidropdown(app.DisplayDropDownGrid);
            app.DispImage.Items = {};
            app.DispImage.ValueChangedFcn = createCallbackFcn(app, @displayCallbacks, true);
            app.DispImage.Layout.Row = 1;
            app.DispImage.Layout.Column = 3;
            app.DispImage.Value = {};

            % Create ImageLabel
            app.ImageLabel = uilabel(app.DisplayDropDownGrid);
            app.ImageLabel.HorizontalAlignment = 'right';
            app.ImageLabel.FontWeight = 'bold';
            app.ImageLabel.Layout.Row = 1;
            app.ImageLabel.Layout.Column = 2;
            app.ImageLabel.Text = 'Image';

            % Create DispLock
            app.DispLock = uibutton(app.DisplayDropDownGrid, 'state');
            app.DispLock.ValueChangedFcn = createCallbackFcn(app, @displayCallbacks, true);
            app.DispLock.Tooltip = {'Stop changing the selected image when clicking on a new image'};
            app.DispLock.Icon = 'link.png';
            app.DispLock.Text = '';
            app.DispLock.Layout.Row = 1;
            app.DispLock.Layout.Column = 4;

            % Create ShowImageWdw
            app.ShowImageWdw = uibutton(app.DisplayDropDownGrid, 'push');
            app.ShowImageWdw.ButtonPushedFcn = createCallbackFcn(app, @showWindowCallbacks, true);
            app.ShowImageWdw.Icon = 'frontWindow.png';
            app.ShowImageWdw.FontWeight = 'bold';
            app.ShowImageWdw.Tooltip = {'Bring selected image to front'};
            app.ShowImageWdw.Layout.Row = 1;
            app.ShowImageWdw.Layout.Column = 1;
            app.ShowImageWdw.Text = '';

            % Create DispContrastsGrid
            app.DispContrastsGrid = uigridlayout(app.DisplayGrid);
            app.DispContrastsGrid.ColumnWidth = {24, '1x', 72};
            app.DispContrastsGrid.RowHeight = {24, 24, 24, 24};
            app.DispContrastsGrid.ColumnSpacing = 4;
            app.DispContrastsGrid.RowSpacing = 4;
            app.DispContrastsGrid.Padding = [0 0 0 0];
            app.DispContrastsGrid.Layout.Row = 4;
            app.DispContrastsGrid.Layout.Column = 1;

            % Create DispBrightness
            app.DispBrightness = uislider(app.DispContrastsGrid);
            app.DispBrightness.MajorTicks = [];
            app.DispBrightness.MajorTickLabels = {};
            app.DispBrightness.ValueChangedFcn = createCallbackFcn(app, @displayCallbacks, true);
            app.DispBrightness.ValueChangingFcn = createCallbackFcn(app, @displayCallbacks, true);
            app.DispBrightness.MinorTicks = [];
            app.DispBrightness.Layout.Row = 1;
            app.DispBrightness.Layout.Column = 2;
            app.DispBrightness.Value = 50;

            % Create DispContrast
            app.DispContrast = uislider(app.DispContrastsGrid);
            app.DispContrast.MajorTicks = [];
            app.DispContrast.MajorTickLabels = {};
            app.DispContrast.ValueChangedFcn = createCallbackFcn(app, @displayCallbacks, true);
            app.DispContrast.ValueChangingFcn = createCallbackFcn(app, @displayCallbacks, true);
            app.DispContrast.MinorTicks = [];
            app.DispContrast.Layout.Row = 2;
            app.DispContrast.Layout.Column = 2;
            app.DispContrast.Value = 50;

            % Create DispGamma
            app.DispGamma = uislider(app.DispContrastsGrid);
            app.DispGamma.Limits = [0 2];
            app.DispGamma.MajorTicks = [];
            app.DispGamma.MajorTickLabels = {};
            app.DispGamma.ValueChangedFcn = createCallbackFcn(app, @displayCallbacks, true);
            app.DispGamma.ValueChangingFcn = createCallbackFcn(app, @displayCallbacks, true);
            app.DispGamma.MinorTicks = [];
            app.DispGamma.Layout.Row = 3;
            app.DispGamma.Layout.Column = 2;
            app.DispGamma.Value = 1;

            % Create DispGammaReset
            app.DispGammaReset = uibutton(app.DispContrastsGrid, 'push');
            app.DispGammaReset.ButtonPushedFcn = createCallbackFcn(app, @displayCallbacks, true);
            app.DispGammaReset.Icon = 'gamma.png';
            app.DispGammaReset.FontWeight = 'bold';
            app.DispGammaReset.Tooltip = {'Reset Gamma'};
            app.DispGammaReset.Layout.Row = 3;
            app.DispGammaReset.Layout.Column = 1;
            app.DispGammaReset.Text = '';

            % Create DispContrastReset
            app.DispContrastReset = uibutton(app.DispContrastsGrid, 'push');
            app.DispContrastReset.ButtonPushedFcn = createCallbackFcn(app, @displayCallbacks, true);
            app.DispContrastReset.Icon = 'contrast.png';
            app.DispContrastReset.FontWeight = 'bold';
            app.DispContrastReset.Tooltip = {'Reset Contrast'};
            app.DispContrastReset.Layout.Row = 2;
            app.DispContrastReset.Layout.Column = 1;
            app.DispContrastReset.Text = '';

            % Create DispBrightnessReset
            app.DispBrightnessReset = uibutton(app.DispContrastsGrid, 'push');
            app.DispBrightnessReset.ButtonPushedFcn = createCallbackFcn(app, @displayCallbacks, true);
            app.DispBrightnessReset.Icon = 'brightness.png';
            app.DispBrightnessReset.FontWeight = 'bold';
            app.DispBrightnessReset.Tooltip = {'Reset Brightness'};
            app.DispBrightnessReset.Layout.Row = 1;
            app.DispBrightnessReset.Layout.Column = 1;
            app.DispBrightnessReset.Text = '';

            % Create DispBrightness_NF
            app.DispBrightness_NF = uispinner(app.DispContrastsGrid);
            app.DispBrightness_NF.ValueChangingFcn = createCallbackFcn(app, @displayCallbacks, true);
            app.DispBrightness_NF.Limits = [0 100];
            app.DispBrightness_NF.ValueDisplayFormat = '%.4g%%';
            app.DispBrightness_NF.ValueChangedFcn = createCallbackFcn(app, @displayCallbacks, true);
            app.DispBrightness_NF.Layout.Row = 1;
            app.DispBrightness_NF.Layout.Column = 3;
            app.DispBrightness_NF.Value = 50;

            % Create DispContrast_NF
            app.DispContrast_NF = uispinner(app.DispContrastsGrid);
            app.DispContrast_NF.ValueChangingFcn = createCallbackFcn(app, @displayCallbacks, true);
            app.DispContrast_NF.Limits = [0 100];
            app.DispContrast_NF.ValueDisplayFormat = '%.4g%%';
            app.DispContrast_NF.ValueChangedFcn = createCallbackFcn(app, @displayCallbacks, true);
            app.DispContrast_NF.Layout.Row = 2;
            app.DispContrast_NF.Layout.Column = 3;
            app.DispContrast_NF.Value = 50;

            % Create DispGamma_NF
            app.DispGamma_NF = uispinner(app.DispContrastsGrid);
            app.DispGamma_NF.Step = 0.01;
            app.DispGamma_NF.ValueChangingFcn = createCallbackFcn(app, @displayCallbacks, true);
            app.DispGamma_NF.Limits = [0 2];
            app.DispGamma_NF.ValueDisplayFormat = '%.5g';
            app.DispGamma_NF.ValueChangedFcn = createCallbackFcn(app, @displayCallbacks, true);
            app.DispGamma_NF.Layout.Row = 3;
            app.DispGamma_NF.Layout.Column = 3;
            app.DispGamma_NF.Value = 1;

            % Create DispMaskOpa
            app.DispMaskOpa = uislider(app.DispContrastsGrid);
            app.DispMaskOpa.MajorTicks = [];
            app.DispMaskOpa.ValueChangedFcn = createCallbackFcn(app, @displayCallbacks, true);
            app.DispMaskOpa.ValueChangingFcn = createCallbackFcn(app, @displayCallbacks, true);
            app.DispMaskOpa.MinorTicks = [];
            app.DispMaskOpa.Tooltip = {'Mask opacity displayed on pattern'};
            app.DispMaskOpa.Layout.Row = 4;
            app.DispMaskOpa.Layout.Column = 2;

            % Create DispMaskOpa_NF
            app.DispMaskOpa_NF = uispinner(app.DispContrastsGrid);
            app.DispMaskOpa_NF.ValueChangingFcn = createCallbackFcn(app, @displayCallbacks, true);
            app.DispMaskOpa_NF.Limits = [0 100];
            app.DispMaskOpa_NF.ValueDisplayFormat = '%.4g%%';
            app.DispMaskOpa_NF.ValueChangedFcn = createCallbackFcn(app, @displayCallbacks, true);
            app.DispMaskOpa_NF.Layout.Row = 4;
            app.DispMaskOpa_NF.Layout.Column = 3;

            % Create ShowMaskWdw
            app.ShowMaskWdw = uibutton(app.DispContrastsGrid, 'push');
            app.ShowMaskWdw.ButtonPushedFcn = createCallbackFcn(app, @showWindowCallbacks, true);
            app.ShowMaskWdw.Icon = 'Aperture.png';
            app.ShowMaskWdw.Tooltip = {'Show Mask Image'};
            app.ShowMaskWdw.Layout.Row = 4;
            app.ShowMaskWdw.Layout.Column = 1;
            app.ShowMaskWdw.Text = '';

            % Create DispHistGrid
            app.DispHistGrid = uigridlayout(app.DisplayGrid);
            app.DispHistGrid.ColumnWidth = {'1x', 'fit', 6};
            app.DispHistGrid.RowHeight = {6, 'fit', '1x'};
            app.DispHistGrid.ColumnSpacing = 4;
            app.DispHistGrid.RowSpacing = 4;
            app.DispHistGrid.Padding = [0 0 0 0];
            app.DispHistGrid.Layout.Row = 3;
            app.DispHistGrid.Layout.Column = 1;

            % Create HistAxes
            app.HistAxes = uiaxes(app.DispHistGrid);
            app.HistAxes.Toolbar.Visible = 'off';
            app.HistAxes.XTick = [];
            app.HistAxes.YTick = [];
            app.HistAxes.ZTick = [];
            app.HistAxes.Box = 'on';
            app.HistAxes.TickDir = 'in';
            app.HistAxes.NextPlot = 'add';
            app.HistAxes.Layout.Row = [1 3];
            app.HistAxes.Layout.Column = [1 3];

            % Create HistLog
            app.HistLog = uibutton(app.DispHistGrid, 'state');
            app.HistLog.ValueChangedFcn = createCallbackFcn(app, @displayCallbacks, true);
            app.HistLog.Text = 'log';
            app.HistLog.FontWeight = 'bold';
            app.HistLog.Layout.Row = 2;
            app.HistLog.Layout.Column = 2;

            % Create ImStatsNotes
            app.ImStatsNotes = uitextarea(app.DisplayGrid);
            app.ImStatsNotes.Editable = 'off';
            app.ImStatsNotes.FontName = 'Monospaced';
            app.ImStatsNotes.FontSize = 11;
            app.ImStatsNotes.FontWeight = 'bold';
            app.ImStatsNotes.Layout.Row = 2;
            app.ImStatsNotes.Layout.Column = 1;

            % Create MiscTab
            app.MiscTab = uitab(app.SettingsTabGroup);
            app.MiscTab.AutoResizeChildren = 'off';
            app.MiscTab.Title = 'Misc';

            % Create MiscGrid
            app.MiscGrid = uigridlayout(app.MiscTab);
            app.MiscGrid.ColumnWidth = {'1x'};
            app.MiscGrid.RowHeight = {20, 20, 'fit', 'fit', 'fit', 'fit'};
            app.MiscGrid.ColumnSpacing = 4;
            app.MiscGrid.RowSpacing = 4;
            app.MiscGrid.Padding = [4 4 4 4];

            % Create DiffractionImageWindowsPanel
            app.DiffractionImageWindowsPanel = uipanel(app.MiscGrid);
            app.DiffractionImageWindowsPanel.AutoResizeChildren = 'off';
            app.DiffractionImageWindowsPanel.BorderType = 'none';
            app.DiffractionImageWindowsPanel.TitlePosition = 'centertop';
            app.DiffractionImageWindowsPanel.Title = 'Diffraction Image Windows';
            app.DiffractionImageWindowsPanel.Layout.Row = 4;
            app.DiffractionImageWindowsPanel.Layout.Column = 1;
            app.DiffractionImageWindowsPanel.FontName = 'MS Sans Serif';
            app.DiffractionImageWindowsPanel.FontWeight = 'bold';

            % Create DiffractionWindowGrid
            app.DiffractionWindowGrid = uigridlayout(app.DiffractionImageWindowsPanel);
            app.DiffractionWindowGrid.ColumnWidth = {12, 60, 12, 60, '1x', 'fit', 'fit'};
            app.DiffractionWindowGrid.RowHeight = {24, 24};
            app.DiffractionWindowGrid.ColumnSpacing = 4;
            app.DiffractionWindowGrid.RowSpacing = 4;
            app.DiffractionWindowGrid.Padding = [0 0 0 4];

            % Create WEditFieldLabel
            app.WEditFieldLabel = uilabel(app.DiffractionWindowGrid);
            app.WEditFieldLabel.HorizontalAlignment = 'right';
            app.WEditFieldLabel.Layout.Row = 2;
            app.WEditFieldLabel.Layout.Column = 1;
            app.WEditFieldLabel.Text = 'W';

            % Create WdwWDfrn
            app.WdwWDfrn = uieditfield(app.DiffractionWindowGrid, 'numeric');
            app.WdwWDfrn.Limits = [1 Inf];
            app.WdwWDfrn.RoundFractionalValues = 'on';
            app.WdwWDfrn.ValueDisplayFormat = '%.0f';
            app.WdwWDfrn.ValueChangedFcn = createCallbackFcn(app, @resizeWindowCallbacks, true);
            app.WdwWDfrn.Tag = 'Dfrn';
            app.WdwWDfrn.Layout.Row = 2;
            app.WdwWDfrn.Layout.Column = 2;
            app.WdwWDfrn.Value = 400;

            % Create HEditFieldLabel
            app.HEditFieldLabel = uilabel(app.DiffractionWindowGrid);
            app.HEditFieldLabel.HorizontalAlignment = 'right';
            app.HEditFieldLabel.Layout.Row = 2;
            app.HEditFieldLabel.Layout.Column = 3;
            app.HEditFieldLabel.Text = 'H';

            % Create WdwHDfrn
            app.WdwHDfrn = uieditfield(app.DiffractionWindowGrid, 'numeric');
            app.WdwHDfrn.Limits = [1 Inf];
            app.WdwHDfrn.RoundFractionalValues = 'on';
            app.WdwHDfrn.ValueDisplayFormat = '%.0f';
            app.WdwHDfrn.ValueChangedFcn = createCallbackFcn(app, @resizeWindowCallbacks, true);
            app.WdwHDfrn.Tag = 'Dfrn';
            app.WdwHDfrn.Layout.Row = 2;
            app.WdwHDfrn.Layout.Column = 4;
            app.WdwHDfrn.Value = 400;

            % Create WdwSetDfrn
            app.WdwSetDfrn = uibutton(app.DiffractionWindowGrid, 'push');
            app.WdwSetDfrn.ButtonPushedFcn = createCallbackFcn(app, @resizeWindowCallbacks, true);
            app.WdwSetDfrn.Tag = 'Dfrn';
            app.WdwSetDfrn.Layout.Row = 2;
            app.WdwSetDfrn.Layout.Column = 6;
            app.WdwSetDfrn.Text = 'Set';

            % Create DiffractionAxesGrid
            app.DiffractionAxesGrid = uigridlayout(app.DiffractionWindowGrid);
            app.DiffractionAxesGrid.ColumnWidth = {'1x', 24, 24, 24, '1x', 20, 'fit', '1x'};
            app.DiffractionAxesGrid.RowHeight = {24};
            app.DiffractionAxesGrid.ColumnSpacing = 4;
            app.DiffractionAxesGrid.RowSpacing = 4;
            app.DiffractionAxesGrid.Padding = [0 0 0 0];
            app.DiffractionAxesGrid.Layout.Row = 1;
            app.DiffractionAxesGrid.Layout.Column = [1 7];

            % Create ShowDfrnAxes
            app.ShowDfrnAxes = uibutton(app.DiffractionAxesGrid, 'state');
            app.ShowDfrnAxes.ValueChangedFcn = createCallbackFcn(app, @axeDirCallbacks, true);
            app.ShowDfrnAxes.Tag = 'Dfrn';
            app.ShowDfrnAxes.Tooltip = {'Show Axis Directions on Images'};
            app.ShowDfrnAxes.Icon = 'axes.png';
            app.ShowDfrnAxes.Text = '';
            app.ShowDfrnAxes.Layout.Row = 1;
            app.ShowDfrnAxes.Layout.Column = 2;
            app.ShowDfrnAxes.Value = true;

            % Create RvsXDfrn
            app.RvsXDfrn = uibutton(app.DiffractionAxesGrid, 'state');
            app.RvsXDfrn.ValueChangedFcn = createCallbackFcn(app, @axeDirCallbacks, true);
            app.RvsXDfrn.Tag = 'Dfrn';
            app.RvsXDfrn.Tooltip = {'Reverse X-axis Direction'};
            app.RvsXDfrn.Icon = 'axis-x.png';
            app.RvsXDfrn.Text = '';
            app.RvsXDfrn.FontWeight = 'bold';
            app.RvsXDfrn.Layout.Row = 1;
            app.RvsXDfrn.Layout.Column = 3;

            % Create RvsYDfrn
            app.RvsYDfrn = uibutton(app.DiffractionAxesGrid, 'state');
            app.RvsYDfrn.ValueChangedFcn = createCallbackFcn(app, @axeDirCallbacks, true);
            app.RvsYDfrn.Tag = 'Dfrn';
            app.RvsYDfrn.Tooltip = {'Reverse Y-axis Direction'};
            app.RvsYDfrn.Icon = 'axis-y.png';
            app.RvsYDfrn.Text = '';
            app.RvsYDfrn.FontWeight = 'bold';
            app.RvsYDfrn.Layout.Row = 1;
            app.RvsYDfrn.Layout.Column = 4;
            app.RvsYDfrn.Value = true;

            % Create RotDfrn
            app.RotDfrn = uidropdown(app.DiffractionAxesGrid);
            app.RotDfrn.Items = {'0°', '90°', '180°', '-90°'};
            app.RotDfrn.ItemsData = [0 90 180 -90];
            app.RotDfrn.ValueChangedFcn = createCallbackFcn(app, @axeDirCallbacks, true);
            app.RotDfrn.Tag = 'Dfrn';
            app.RotDfrn.Tooltip = {'Rotate Image Display'};
            app.RotDfrn.Layout.Row = 1;
            app.RotDfrn.Layout.Column = 7;
            app.RotDfrn.Value = 0;

            % Create RotDfrnIcon
            app.RotDfrnIcon = uiimage(app.DiffractionAxesGrid);
            app.RotDfrnIcon.Tooltip = {'Rotate View'};
            app.RotDfrnIcon.Layout.Row = 1;
            app.RotDfrnIcon.Layout.Column = 6;
            app.RotDfrnIcon.ImageSource = 'right_rotate.png';

            % Create WdwSetAllDfrn
            app.WdwSetAllDfrn = uibutton(app.DiffractionWindowGrid, 'push');
            app.WdwSetAllDfrn.ButtonPushedFcn = createCallbackFcn(app, @resizeWindowCallbacks, true);
            app.WdwSetAllDfrn.Tag = 'Dfrn';
            app.WdwSetAllDfrn.Layout.Row = 2;
            app.WdwSetAllDfrn.Layout.Column = 7;
            app.WdwSetAllDfrn.Text = 'Set All';

            % Create DetectorCoordinatePanel
            app.DetectorCoordinatePanel = uipanel(app.MiscGrid);
            app.DetectorCoordinatePanel.AutoResizeChildren = 'off';
            app.DetectorCoordinatePanel.BorderType = 'none';
            app.DetectorCoordinatePanel.TitlePosition = 'centertop';
            app.DetectorCoordinatePanel.Title = 'Detector Coordinate Options';
            app.DetectorCoordinatePanel.Layout.Row = 3;
            app.DetectorCoordinatePanel.Layout.Column = 1;
            app.DetectorCoordinatePanel.FontName = 'MS Sans Serif';
            app.DetectorCoordinatePanel.FontWeight = 'bold';

            % Create DetectorCoordinateGrid
            app.DetectorCoordinateGrid = uigridlayout(app.DetectorCoordinatePanel);
            app.DetectorCoordinateGrid.ColumnWidth = {'1x', 'fit', '1x', 'fit', '1x', 'fit', '1x'};
            app.DetectorCoordinateGrid.RowHeight = {24};
            app.DetectorCoordinateGrid.ColumnSpacing = 4;
            app.DetectorCoordinateGrid.RowSpacing = 4;
            app.DetectorCoordinateGrid.Padding = [0 0 0 4];

            % Create DCSys
            app.DCSys = uidropdown(app.DetectorCoordinateGrid);
            app.DCSys.Items = {'Polar', 'Cartesian'};
            app.DCSys.ValueChangedFcn = createCallbackFcn(app, @detrCoordCallbacks, true);
            app.DCSys.Tooltip = {'Display diffraction coordinates with a Cartesian or polar system'};
            app.DCSys.Layout.Row = 1;
            app.DCSys.Layout.Column = 2;
            app.DCSys.Value = 'Polar';

            % Create DCPos
            app.DCPos = uidropdown(app.DetectorCoordinateGrid);
            app.DCPos.Items = {'Relative', 'Absolute'};
            app.DCPos.ValueChangedFcn = createCallbackFcn(app, @detrCoordCallbacks, true);
            app.DCPos.Tooltip = {'Display diffraction coordinates as absolute positions or relative to the transmitted beam'};
            app.DCPos.Layout.Row = 1;
            app.DCPos.Layout.Column = 4;
            app.DCPos.Value = 'Relative';

            % Create DCUnit
            app.DCUnit = uidropdown(app.DetectorCoordinateGrid);
            app.DCUnit.Items = {'mrad', 'Pixel'};
            app.DCUnit.ItemsData = {'mrad', 'px'};
            app.DCUnit.ValueChangedFcn = createCallbackFcn(app, @detrCoordCallbacks, true);
            app.DCUnit.Tooltip = {'Display diffraction coordinates in mrad or pixel'};
            app.DCUnit.Layout.Row = 1;
            app.DCUnit.Layout.Column = 6;
            app.DCUnit.Value = 'mrad';

            % Create RealSpaceWindowPanel
            app.RealSpaceWindowPanel = uipanel(app.MiscGrid);
            app.RealSpaceWindowPanel.AutoResizeChildren = 'off';
            app.RealSpaceWindowPanel.BorderType = 'none';
            app.RealSpaceWindowPanel.TitlePosition = 'centertop';
            app.RealSpaceWindowPanel.Title = 'Real-space Image Windows';
            app.RealSpaceWindowPanel.Layout.Row = 5;
            app.RealSpaceWindowPanel.Layout.Column = 1;
            app.RealSpaceWindowPanel.FontName = 'MS Sans Serif';
            app.RealSpaceWindowPanel.FontWeight = 'bold';

            % Create RealSpaceWindowGrid
            app.RealSpaceWindowGrid = uigridlayout(app.RealSpaceWindowPanel);
            app.RealSpaceWindowGrid.ColumnWidth = {12, 60, 12, 60, '1x', 'fit', 'fit'};
            app.RealSpaceWindowGrid.RowHeight = {24, 24};
            app.RealSpaceWindowGrid.ColumnSpacing = 4;
            app.RealSpaceWindowGrid.RowSpacing = 4;
            app.RealSpaceWindowGrid.Padding = [0 0 0 4];

            % Create WdwWReal
            app.WdwWReal = uieditfield(app.RealSpaceWindowGrid, 'numeric');
            app.WdwWReal.Limits = [1 Inf];
            app.WdwWReal.RoundFractionalValues = 'on';
            app.WdwWReal.ValueDisplayFormat = '%.0f';
            app.WdwWReal.ValueChangedFcn = createCallbackFcn(app, @resizeWindowCallbacks, true);
            app.WdwWReal.Tag = 'Real';
            app.WdwWReal.Layout.Row = 2;
            app.WdwWReal.Layout.Column = 2;
            app.WdwWReal.Value = 400;

            % Create WEditField_2Label
            app.WEditField_2Label = uilabel(app.RealSpaceWindowGrid);
            app.WEditField_2Label.HorizontalAlignment = 'right';
            app.WEditField_2Label.Layout.Row = 2;
            app.WEditField_2Label.Layout.Column = 1;
            app.WEditField_2Label.Text = 'W';

            % Create HEditField_2Label
            app.HEditField_2Label = uilabel(app.RealSpaceWindowGrid);
            app.HEditField_2Label.HorizontalAlignment = 'right';
            app.HEditField_2Label.Layout.Row = 2;
            app.HEditField_2Label.Layout.Column = 3;
            app.HEditField_2Label.Text = 'H';

            % Create WdwHReal
            app.WdwHReal = uieditfield(app.RealSpaceWindowGrid, 'numeric');
            app.WdwHReal.Limits = [1 Inf];
            app.WdwHReal.RoundFractionalValues = 'on';
            app.WdwHReal.ValueDisplayFormat = '%.0f';
            app.WdwHReal.ValueChangedFcn = createCallbackFcn(app, @resizeWindowCallbacks, true);
            app.WdwHReal.Tag = 'Real';
            app.WdwHReal.Layout.Row = 2;
            app.WdwHReal.Layout.Column = 4;
            app.WdwHReal.Value = 400;

            % Create WdwSetReal
            app.WdwSetReal = uibutton(app.RealSpaceWindowGrid, 'push');
            app.WdwSetReal.ButtonPushedFcn = createCallbackFcn(app, @resizeWindowCallbacks, true);
            app.WdwSetReal.Tag = 'Real';
            app.WdwSetReal.Layout.Row = 2;
            app.WdwSetReal.Layout.Column = 6;
            app.WdwSetReal.Text = 'Set';

            % Create RealSpaceAxesGrid
            app.RealSpaceAxesGrid = uigridlayout(app.RealSpaceWindowGrid);
            app.RealSpaceAxesGrid.ColumnWidth = {'1x', 24, 24, 24, '1x', 20, 'fit', '1x'};
            app.RealSpaceAxesGrid.RowHeight = {24};
            app.RealSpaceAxesGrid.ColumnSpacing = 4;
            app.RealSpaceAxesGrid.RowSpacing = 4;
            app.RealSpaceAxesGrid.Padding = [0 0 0 0];
            app.RealSpaceAxesGrid.Layout.Row = 1;
            app.RealSpaceAxesGrid.Layout.Column = [1 7];

            % Create RotReal
            app.RotReal = uidropdown(app.RealSpaceAxesGrid);
            app.RotReal.Items = {'0°', '90°', '180°', '-90°'};
            app.RotReal.ItemsData = [0 90 180 -90];
            app.RotReal.ValueChangedFcn = createCallbackFcn(app, @axeDirCallbacks, true);
            app.RotReal.Tag = 'Real';
            app.RotReal.Tooltip = {'Rotate Image Display'};
            app.RotReal.Layout.Row = 1;
            app.RotReal.Layout.Column = 7;
            app.RotReal.Value = 0;

            % Create RotRealIcon
            app.RotRealIcon = uiimage(app.RealSpaceAxesGrid);
            app.RotRealIcon.Tooltip = {'Rotate View'};
            app.RotRealIcon.Layout.Row = 1;
            app.RotRealIcon.Layout.Column = 6;
            app.RotRealIcon.ImageSource = 'right_rotate.png';

            % Create RvsYReal
            app.RvsYReal = uibutton(app.RealSpaceAxesGrid, 'state');
            app.RvsYReal.ValueChangedFcn = createCallbackFcn(app, @axeDirCallbacks, true);
            app.RvsYReal.Tag = 'Real';
            app.RvsYReal.Tooltip = {'Reverse Y-axis Direction'};
            app.RvsYReal.Icon = 'axis-y.png';
            app.RvsYReal.Text = '';
            app.RvsYReal.FontWeight = 'bold';
            app.RvsYReal.Layout.Row = 1;
            app.RvsYReal.Layout.Column = 4;
            app.RvsYReal.Value = true;

            % Create RvsXReal
            app.RvsXReal = uibutton(app.RealSpaceAxesGrid, 'state');
            app.RvsXReal.ValueChangedFcn = createCallbackFcn(app, @axeDirCallbacks, true);
            app.RvsXReal.Tag = 'Real';
            app.RvsXReal.Tooltip = {'Reverse X-axis Direction'};
            app.RvsXReal.Icon = 'axis-x.png';
            app.RvsXReal.Text = '';
            app.RvsXReal.FontWeight = 'bold';
            app.RvsXReal.Layout.Row = 1;
            app.RvsXReal.Layout.Column = 3;

            % Create ShowRealAxes
            app.ShowRealAxes = uibutton(app.RealSpaceAxesGrid, 'state');
            app.ShowRealAxes.ValueChangedFcn = createCallbackFcn(app, @axeDirCallbacks, true);
            app.ShowRealAxes.Tag = 'Real';
            app.ShowRealAxes.Tooltip = {'Show Axis Directions on Images'};
            app.ShowRealAxes.Icon = 'axes.png';
            app.ShowRealAxes.Text = '';
            app.ShowRealAxes.Layout.Row = 1;
            app.ShowRealAxes.Layout.Column = 2;
            app.ShowRealAxes.Value = true;

            % Create WdwSetAllReal
            app.WdwSetAllReal = uibutton(app.RealSpaceWindowGrid, 'push');
            app.WdwSetAllReal.ButtonPushedFcn = createCallbackFcn(app, @resizeWindowCallbacks, true);
            app.WdwSetAllReal.Tag = 'Real';
            app.WdwSetAllReal.Layout.Row = 2;
            app.WdwSetAllReal.Layout.Column = 7;
            app.WdwSetAllReal.Text = 'Set All';

            % Create ShowImageWindowsPanel
            app.ShowImageWindowsPanel = uipanel(app.MiscGrid);
            app.ShowImageWindowsPanel.AutoResizeChildren = 'off';
            app.ShowImageWindowsPanel.BorderType = 'none';
            app.ShowImageWindowsPanel.TitlePosition = 'centertop';
            app.ShowImageWindowsPanel.Title = 'Show Image Windows';
            app.ShowImageWindowsPanel.Layout.Row = 6;
            app.ShowImageWindowsPanel.Layout.Column = 1;
            app.ShowImageWindowsPanel.FontName = 'MS Sans Serif';
            app.ShowImageWindowsPanel.FontWeight = 'bold';

            % Create ShowImageWindowsGrid
            app.ShowImageWindowsGrid = uigridlayout(app.ShowImageWindowsPanel);
            app.ShowImageWindowsGrid.ColumnWidth = {'1x', '1x', '1x', '1x'};
            app.ShowImageWindowsGrid.RowHeight = {24, 24, 24};
            app.ShowImageWindowsGrid.ColumnSpacing = 0;
            app.ShowImageWindowsGrid.RowSpacing = 0;
            app.ShowImageWindowsGrid.Padding = [0 0 0 4];

            % Create ShowCoMXWdw
            app.ShowCoMXWdw = uibutton(app.ShowImageWindowsGrid, 'push');
            app.ShowCoMXWdw.ButtonPushedFcn = createCallbackFcn(app, @showWindowCallbacks, true);
            app.ShowCoMXWdw.Tag = 'CoMX';
            app.ShowCoMXWdw.Tooltip = {'Show CoM/DPC X Image'};
            app.ShowCoMXWdw.Layout.Row = 3;
            app.ShowCoMXWdw.Layout.Column = 1;
            app.ShowCoMXWdw.Text = 'CoM X';

            % Create ShowCoMYWdw
            app.ShowCoMYWdw = uibutton(app.ShowImageWindowsGrid, 'push');
            app.ShowCoMYWdw.ButtonPushedFcn = createCallbackFcn(app, @showWindowCallbacks, true);
            app.ShowCoMYWdw.Tag = 'CoMY';
            app.ShowCoMYWdw.Tooltip = {'Show CoM/DPC Y Image'};
            app.ShowCoMYWdw.Layout.Row = 3;
            app.ShowCoMYWdw.Layout.Column = 2;
            app.ShowCoMYWdw.Text = 'CoM Y';

            % Create ShowdCoMWdw
            app.ShowdCoMWdw = uibutton(app.ShowImageWindowsGrid, 'push');
            app.ShowdCoMWdw.ButtonPushedFcn = createCallbackFcn(app, @showWindowCallbacks, true);
            app.ShowdCoMWdw.Tag = 'dCoM';
            app.ShowdCoMWdw.Tooltip = {'Show dCoM/dDPC Image'};
            app.ShowdCoMWdw.Layout.Row = 3;
            app.ShowdCoMWdw.Layout.Column = 3;
            app.ShowdCoMWdw.Text = 'dCoM';

            % Create ShowiCoMWdw
            app.ShowiCoMWdw = uibutton(app.ShowImageWindowsGrid, 'push');
            app.ShowiCoMWdw.ButtonPushedFcn = createCallbackFcn(app, @showWindowCallbacks, true);
            app.ShowiCoMWdw.Tag = 'iCoM';
            app.ShowiCoMWdw.Tooltip = {'Show iCoM/iDPC Image'};
            app.ShowiCoMWdw.Layout.Row = 3;
            app.ShowiCoMWdw.Layout.Column = 4;
            app.ShowiCoMWdw.Text = 'iCoM';

            % Create ShowDfrnMaskWdw_2
            app.ShowDfrnMaskWdw_2 = uibutton(app.ShowImageWindowsGrid, 'push');
            app.ShowDfrnMaskWdw_2.ButtonPushedFcn = createCallbackFcn(app, @showWindowCallbacks, true);
            app.ShowDfrnMaskWdw_2.Tag = 'DfrnMask';
            app.ShowDfrnMaskWdw_2.Icon = 'Aperture.png';
            app.ShowDfrnMaskWdw_2.Tooltip = {'Show Diffraction Mask'};
            app.ShowDfrnMaskWdw_2.Layout.Row = 1;
            app.ShowDfrnMaskWdw_2.Layout.Column = 2;
            app.ShowDfrnMaskWdw_2.Text = 'Dfrn';

            % Create ShowDfrnWdw
            app.ShowDfrnWdw = uibutton(app.ShowImageWindowsGrid, 'push');
            app.ShowDfrnWdw.ButtonPushedFcn = createCallbackFcn(app, @showWindowCallbacks, true);
            app.ShowDfrnWdw.Tag = 'Dfrn';
            app.ShowDfrnWdw.Tooltip = {'Show Diffraction Pattern'};
            app.ShowDfrnWdw.Layout.Row = 1;
            app.ShowDfrnWdw.Layout.Column = 1;
            app.ShowDfrnWdw.Text = 'Diffraction';

            % Create ShowRealWdw
            app.ShowRealWdw = uibutton(app.ShowImageWindowsGrid, 'push');
            app.ShowRealWdw.ButtonPushedFcn = createCallbackFcn(app, @showWindowCallbacks, true);
            app.ShowRealWdw.Tag = 'Real';
            app.ShowRealWdw.Tooltip = {'Show Real-space Image'};
            app.ShowRealWdw.Layout.Row = 1;
            app.ShowRealWdw.Layout.Column = 3;
            app.ShowRealWdw.Text = 'BF/DF';

            % Create ShowCoMPhMagWdw
            app.ShowCoMPhMagWdw = uibutton(app.ShowImageWindowsGrid, 'push');
            app.ShowCoMPhMagWdw.ButtonPushedFcn = createCallbackFcn(app, @showWindowCallbacks, true);
            app.ShowCoMPhMagWdw.Tag = 'CoMPhMag';
            app.ShowCoMPhMagWdw.Tooltip = {'Show CoM/DPC Phase (Magnitude-shaded) Image'};
            app.ShowCoMPhMagWdw.Layout.Row = 2;
            app.ShowCoMPhMagWdw.Layout.Column = 2;
            app.ShowCoMPhMagWdw.Text = '|CoM| φ';

            % Create ShowCoMPhWdw
            app.ShowCoMPhWdw = uibutton(app.ShowImageWindowsGrid, 'push');
            app.ShowCoMPhWdw.ButtonPushedFcn = createCallbackFcn(app, @showWindowCallbacks, true);
            app.ShowCoMPhWdw.Tag = 'CoMPh';
            app.ShowCoMPhWdw.Tooltip = {'Show CoM/DPC Phase Image'};
            app.ShowCoMPhWdw.Layout.Row = 2;
            app.ShowCoMPhWdw.Layout.Column = 3;
            app.ShowCoMPhWdw.Text = 'CoM φ';

            % Create ShowCoMMagWdw
            app.ShowCoMMagWdw = uibutton(app.ShowImageWindowsGrid, 'push');
            app.ShowCoMMagWdw.ButtonPushedFcn = createCallbackFcn(app, @showWindowCallbacks, true);
            app.ShowCoMMagWdw.Tag = 'CoMMag';
            app.ShowCoMMagWdw.Tooltip = {'Show CoM/DPC Magnitude Image'};
            app.ShowCoMMagWdw.Layout.Row = 2;
            app.ShowCoMMagWdw.Layout.Column = 4;
            app.ShowCoMMagWdw.Text = '|CoM|';

            % Create ShowColorWheelWdw_2
            app.ShowColorWheelWdw_2 = uibutton(app.ShowImageWindowsGrid, 'push');
            app.ShowColorWheelWdw_2.ButtonPushedFcn = createCallbackFcn(app, @showWindowCallbacks, true);
            app.ShowColorWheelWdw_2.Tag = 'ColorWheel';
            app.ShowColorWheelWdw_2.Icon = 'colorwheel.png';
            app.ShowColorWheelWdw_2.Tooltip = {'Show Color Wheel for Phase Vector Field Direction'};
            app.ShowColorWheelWdw_2.Layout.Row = 2;
            app.ShowColorWheelWdw_2.Layout.Column = 1;
            app.ShowColorWheelWdw_2.Text = 'φ';

            % Create ShowRealMaskWdw_2
            app.ShowRealMaskWdw_2 = uibutton(app.ShowImageWindowsGrid, 'push');
            app.ShowRealMaskWdw_2.ButtonPushedFcn = createCallbackFcn(app, @showWindowCallbacks, true);
            app.ShowRealMaskWdw_2.Tag = 'RealMask';
            app.ShowRealMaskWdw_2.Icon = 'Aperture.png';
            app.ShowRealMaskWdw_2.FontSize = 10;
            app.ShowRealMaskWdw_2.Tooltip = {'Show Real-space Mask'};
            app.ShowRealMaskWdw_2.Layout.Row = 1;
            app.ShowRealMaskWdw_2.Layout.Column = 4;
            app.ShowRealMaskWdw_2.Text = 'BF/DF';

            % Create LiveUpdateImagesGrid
            app.LiveUpdateImagesGrid = uigridlayout(app.MiscGrid);
            app.LiveUpdateImagesGrid.ColumnWidth = {'1x', 18, 'fit', 'fit', '1x'};
            app.LiveUpdateImagesGrid.RowHeight = {20};
            app.LiveUpdateImagesGrid.ColumnSpacing = 4;
            app.LiveUpdateImagesGrid.RowSpacing = 4;
            app.LiveUpdateImagesGrid.Padding = [0 0 0 0];
            app.LiveUpdateImagesGrid.Layout.Row = 1;
            app.LiveUpdateImagesGrid.Layout.Column = 1;

            % Create CalcPolicy
            app.CalcPolicy = uidropdown(app.LiveUpdateImagesGrid);
            app.CalcPolicy.Items = {'Active', 'Reduced', 'Passive'};
            app.CalcPolicy.ItemsData = [2 1 0];
            app.CalcPolicy.ValueChangedFcn = createCallbackFcn(app, @updateImagesCallbacks, true);
            app.CalcPolicy.Tooltip = {'Policy to calculate/update images:'; '  1) Active - update in real-time.'; '  2) Reduced - update when interactions finish.'; '  3) Passive - update only when the "Update Images" Button (or F5) is pressed or "Diffraction Detector Mode" changes.'};
            app.CalcPolicy.Layout.Row = 1;
            app.CalcPolicy.Layout.Column = 4;
            app.CalcPolicy.Value = 2;

            % Create CalculationPolicyDropDownLabel
            app.CalculationPolicyDropDownLabel = uilabel(app.LiveUpdateImagesGrid);
            app.CalculationPolicyDropDownLabel.HorizontalAlignment = 'right';
            app.CalculationPolicyDropDownLabel.FontWeight = 'bold';
            app.CalculationPolicyDropDownLabel.Tooltip = {''};
            app.CalculationPolicyDropDownLabel.Layout.Row = 1;
            app.CalculationPolicyDropDownLabel.Layout.Column = 3;
            app.CalculationPolicyDropDownLabel.Text = 'Calculation Policy';

            % Create LiveUpdateImageIcon
            app.LiveUpdateImageIcon = uiimage(app.LiveUpdateImagesGrid);
            app.LiveUpdateImageIcon.Tooltip = {''};
            app.LiveUpdateImageIcon.Layout.Row = 1;
            app.LiveUpdateImageIcon.Layout.Column = 2;
            app.LiveUpdateImageIcon.ImageSource = 'refresh.png';

            % Create annularStepGrid
            app.annularStepGrid = uigridlayout(app.MiscGrid);
            app.annularStepGrid.ColumnWidth = {'1x', '4x', 60, '1x'};
            app.annularStepGrid.RowHeight = {'1x'};
            app.annularStepGrid.ColumnSpacing = 0;
            app.annularStepGrid.RowSpacing = 0;
            app.annularStepGrid.Padding = [0 0 0 0];
            app.annularStepGrid.Layout.Row = 2;
            app.annularStepGrid.Layout.Column = 1;

            % Create AnnularIntegrationStepEditFieldLabel
            app.AnnularIntegrationStepEditFieldLabel = uilabel(app.annularStepGrid);
            app.AnnularIntegrationStepEditFieldLabel.WordWrap = 'on';
            app.AnnularIntegrationStepEditFieldLabel.Layout.Row = 1;
            app.AnnularIntegrationStepEditFieldLabel.Layout.Column = 2;
            app.AnnularIntegrationStepEditFieldLabel.Text = 'Annular Integration Step';

            % Create annularStep
            app.annularStep = uieditfield(app.annularStepGrid, 'numeric');
            app.annularStep.Limits = [1e-05 Inf];
            app.annularStep.ValueDisplayFormat = '%11.2f mrad';
            app.annularStep.Layout.Row = 1;
            app.annularStep.Layout.Column = 3;
            app.annularStep.Value = 0.5;

            % Create InfoTab
            app.InfoTab = uitab(app.SettingsTabGroup);
            app.InfoTab.AutoResizeChildren = 'off';
            app.InfoTab.Title = 'Info';

            % Create InfoGrid
            app.InfoGrid = uigridlayout(app.InfoTab);
            app.InfoGrid.ColumnWidth = {'1x'};
            app.InfoGrid.RowHeight = {'fit', '1x', 'fit'};
            app.InfoGrid.ColumnSpacing = 4;
            app.InfoGrid.RowSpacing = 4;
            app.InfoGrid.Padding = [4 4 4 4];

            % Create DataInfo
            app.DataInfo = uitextarea(app.InfoGrid);
            app.DataInfo.Editable = 'off';
            app.DataInfo.Layout.Row = 2;
            app.DataInfo.Layout.Column = 1;

            % Create DatasetInfoTextAreaLabel
            app.DatasetInfoTextAreaLabel = uilabel(app.InfoGrid);
            app.DatasetInfoTextAreaLabel.HorizontalAlignment = 'center';
            app.DatasetInfoTextAreaLabel.VerticalAlignment = 'bottom';
            app.DatasetInfoTextAreaLabel.FontWeight = 'bold';
            app.DatasetInfoTextAreaLabel.Layout.Row = 1;
            app.DatasetInfoTextAreaLabel.Layout.Column = 1;
            app.DatasetInfoTextAreaLabel.Text = 'Dataset Info';

            % Create DatasetOptionPanel
            app.DatasetOptionPanel = uipanel(app.InfoGrid);
            app.DatasetOptionPanel.BorderType = 'none';
            app.DatasetOptionPanel.TitlePosition = 'centertop';
            app.DatasetOptionPanel.Title = 'Swap Dataset Byte Order and Dimensions';
            app.DatasetOptionPanel.Layout.Row = 3;
            app.DatasetOptionPanel.Layout.Column = 1;
            app.DatasetOptionPanel.FontWeight = 'bold';

            % Create DatasetOptionGrid
            app.DatasetOptionGrid = uigridlayout(app.DatasetOptionPanel);
            app.DatasetOptionGrid.ColumnWidth = {'1x', 'fit', '1x'};
            app.DatasetOptionGrid.RowHeight = {10, 10, 10, 10};
            app.DatasetOptionGrid.ColumnSpacing = 2;
            app.DatasetOptionGrid.RowSpacing = 4;
            app.DatasetOptionGrid.Padding = [0 0 0 4];

            % Create SwapDfrnXY
            app.SwapDfrnXY = uibutton(app.DatasetOptionGrid, 'push');
            app.SwapDfrnXY.ButtonPushedFcn = createCallbackFcn(app, @datasetOptCallbacks, true);
            app.SwapDfrnXY.Tag = 'Dfrn';
            app.SwapDfrnXY.Tooltip = {'Swap the X/Y dimension sizes of the diffraction images, without re-importing'};
            app.SwapDfrnXY.Layout.Row = [1 2];
            app.SwapDfrnXY.Layout.Column = [2 3];
            app.SwapDfrnXY.Text = 'Swap Diffraction X/Y';

            % Create SwapRealXY
            app.SwapRealXY = uibutton(app.DatasetOptionGrid, 'push');
            app.SwapRealXY.ButtonPushedFcn = createCallbackFcn(app, @datasetOptCallbacks, true);
            app.SwapRealXY.Tag = 'Real';
            app.SwapRealXY.Tooltip = {'Swap the X/Y dimension sizes of the real-space images, without re-importing'};
            app.SwapRealXY.Layout.Row = [3 4];
            app.SwapRealXY.Layout.Column = [2 3];
            app.SwapRealXY.Text = 'Swap Real-space X/Y';

            % Create SwapByteOrder
            app.SwapByteOrder = uibutton(app.DatasetOptionGrid, 'push');
            app.SwapByteOrder.ButtonPushedFcn = createCallbackFcn(app, @datasetOptCallbacks, true);
            app.SwapByteOrder.Tooltip = {'Swap the X/Y dimension sizes of the diffraction images, without re-importing'};
            app.SwapByteOrder.Layout.Row = [2 3];
            app.SwapByteOrder.Layout.Column = 1;
            app.SwapByteOrder.Text = 'Swap Byte Order';

            % Create MathTab
            app.MathTab = uitab(app.SettingsTabGroup);
            app.MathTab.Title = 'Math';

            % Create MathGrid
            app.MathGrid = uigridlayout(app.MathTab);
            app.MathGrid.ColumnWidth = {'1x'};
            app.MathGrid.RowHeight = {'fit', 'fit', '1x', 24};
            app.MathGrid.ColumnSpacing = 4;
            app.MathGrid.RowSpacing = 4;
            app.MathGrid.Padding = [4 4 4 4];

            % Create MathFormula
            app.MathFormula = uitextarea(app.MathGrid);
            app.MathFormula.FontName = 'Consolas';
            app.MathFormula.Layout.Row = 3;
            app.MathFormula.Layout.Column = 1;

            % Create FormulaLabel
            app.FormulaLabel = uilabel(app.MathGrid);
            app.FormulaLabel.HorizontalAlignment = 'center';
            app.FormulaLabel.FontWeight = 'bold';
            app.FormulaLabel.Layout.Row = 2;
            app.FormulaLabel.Layout.Column = 1;
            app.FormulaLabel.Text = 'Formula';

            % Create MathButtonGrid
            app.MathButtonGrid = uigridlayout(app.MathGrid);
            app.MathButtonGrid.ColumnWidth = {18, '1x', 'fit', '1x', 18};
            app.MathButtonGrid.RowHeight = {'1x'};
            app.MathButtonGrid.ColumnSpacing = 4;
            app.MathButtonGrid.RowSpacing = 4;
            app.MathButtonGrid.Padding = [0 0 0 0];
            app.MathButtonGrid.Layout.Row = 4;
            app.MathButtonGrid.Layout.Column = 1;

            % Create MathEval
            app.MathEval = uibutton(app.MathButtonGrid, 'push');
            app.MathEval.ButtonPushedFcn = createCallbackFcn(app, @mathCallbacks, true);
            app.MathEval.Layout.Row = 1;
            app.MathEval.Layout.Column = 3;
            app.MathEval.Text = 'Evaluate';

            % Create MathExampleGrid
            app.MathExampleGrid = uigridlayout(app.MathGrid);
            app.MathExampleGrid.ColumnWidth = {'1x', 18};
            app.MathExampleGrid.RowHeight = {18, '1x'};
            app.MathExampleGrid.ColumnSpacing = 4;
            app.MathExampleGrid.RowSpacing = 2;
            app.MathExampleGrid.Padding = [0 0 0 0];
            app.MathExampleGrid.Layout.Row = 1;
            app.MathExampleGrid.Layout.Column = 1;

            % Create MathExampleLabel
            app.MathExampleLabel = uilabel(app.MathExampleGrid);
            app.MathExampleLabel.Layout.Row = [1 2];
            app.MathExampleLabel.Layout.Column = [1 2];
            app.MathExampleLabel.Text = {'<center><b>Syntax Examples</b></center>• Union of B and C, then intersects with A:'; '<b style="font-family:''Consolas''">  A & (B | C)</b>'; '• A squared plus B times C (element-wisely), then transposed:'; '<b style="font-family:''Consolas''">  (A.^2 + B .* C)''</b>'; '• Concatenates (on X-dimension) A''s Rows 1-3  to B''s Rows 4-to-last:'; '<b style="font-family:''Consolas''">  [A(1:3,:) ; B(4:end,:)]</b>'};

            % Create MathHelpIcon
            app.MathHelpIcon = uiimage(app.MathExampleGrid);
            app.MathHelpIcon.Tooltip = {'• MATLAB syntax/functions are used.'; '• The X/Y dimensions (in images) are corresponding to the 1st/2nd dimensions (Rows/Columns) of arrays, respectively.'};
            app.MathHelpIcon.Layout.Row = 1;
            app.MathHelpIcon.Layout.Column = 2;
            app.MathHelpIcon.ImageSource = 'help.png';

            % Create DfrnDetrTabGroup
            app.DfrnDetrTabGroup = uitabgroup(app.Quant4D_Fig);
            app.DfrnDetrTabGroup.TabLocation = 'bottom';
            app.DfrnDetrTabGroup.Position = [-266 85 260 328];

            % Create PreviewTab
            app.PreviewTab = uitab(app.DfrnDetrTabGroup);
            app.PreviewTab.Title = 'Pv';

            % Create PreviewGrid
            app.PreviewGrid = uigridlayout(app.PreviewTab);
            app.PreviewGrid.ColumnWidth = {'1x'};
            app.PreviewGrid.RowHeight = {'1x'};
            app.PreviewGrid.ColumnSpacing = 4;
            app.PreviewGrid.RowSpacing = 4;
            app.PreviewGrid.Padding = [4 4 4 4];

            % Create PreviewFramePanel
            app.PreviewFramePanel = uipanel(app.PreviewGrid);
            app.PreviewFramePanel.BorderType = 'none';
            app.PreviewFramePanel.TitlePosition = 'centertop';
            app.PreviewFramePanel.Title = 'Preview Frame';
            app.PreviewFramePanel.Layout.Row = 1;
            app.PreviewFramePanel.Layout.Column = 1;
            app.PreviewFramePanel.FontWeight = 'bold';

            % Create PreviewButtonGrid
            app.PreviewButtonGrid = uigridlayout(app.PreviewFramePanel);
            app.PreviewButtonGrid.ColumnWidth = {'1x', '1x', '1x'};
            app.PreviewButtonGrid.RowHeight = {24, 24, 24, '1x'};
            app.PreviewButtonGrid.ColumnSpacing = 2;
            app.PreviewButtonGrid.RowSpacing = 2;
            app.PreviewButtonGrid.Padding = [0 0 0 4];

            % Create PvTL
            app.PvTL = uibutton(app.PreviewButtonGrid, 'push');
            app.PvTL.ButtonPushedFcn = createCallbackFcn(app, @previewCallbacks, true);
            app.PvTL.FontName = 'Consolas';
            app.PvTL.Layout.Row = 1;
            app.PvTL.Layout.Column = 1;
            app.PvTL.Text = '[1,1]';

            % Create PvTC
            app.PvTC = uibutton(app.PreviewButtonGrid, 'push');
            app.PvTC.ButtonPushedFcn = createCallbackFcn(app, @previewCallbacks, true);
            app.PvTC.FontName = 'Consolas';
            app.PvTC.Layout.Row = 1;
            app.PvTC.Layout.Column = 2;
            app.PvTC.Text = '[X/2,1]';

            % Create PvTR
            app.PvTR = uibutton(app.PreviewButtonGrid, 'push');
            app.PvTR.ButtonPushedFcn = createCallbackFcn(app, @previewCallbacks, true);
            app.PvTR.FontName = 'Consolas';
            app.PvTR.Layout.Row = 1;
            app.PvTR.Layout.Column = 3;
            app.PvTR.Text = '[X,1]';

            % Create PvCL
            app.PvCL = uibutton(app.PreviewButtonGrid, 'push');
            app.PvCL.ButtonPushedFcn = createCallbackFcn(app, @previewCallbacks, true);
            app.PvCL.FontName = 'Consolas';
            app.PvCL.Layout.Row = 2;
            app.PvCL.Layout.Column = 1;
            app.PvCL.Text = '[1,Y/2]';

            % Create PvCC
            app.PvCC = uibutton(app.PreviewButtonGrid, 'push');
            app.PvCC.ButtonPushedFcn = createCallbackFcn(app, @previewCallbacks, true);
            app.PvCC.FontName = 'Consolas';
            app.PvCC.Layout.Row = 2;
            app.PvCC.Layout.Column = 2;
            app.PvCC.Text = '[X/2,Y/2]';

            % Create PvCR
            app.PvCR = uibutton(app.PreviewButtonGrid, 'push');
            app.PvCR.ButtonPushedFcn = createCallbackFcn(app, @previewCallbacks, true);
            app.PvCR.FontName = 'Consolas';
            app.PvCR.Layout.Row = 2;
            app.PvCR.Layout.Column = 3;
            app.PvCR.Text = '[X,Y/2]';

            % Create PvBL
            app.PvBL = uibutton(app.PreviewButtonGrid, 'push');
            app.PvBL.ButtonPushedFcn = createCallbackFcn(app, @previewCallbacks, true);
            app.PvBL.FontName = 'Consolas';
            app.PvBL.Layout.Row = 3;
            app.PvBL.Layout.Column = 1;
            app.PvBL.Text = '[1,Y]';

            % Create PvBC
            app.PvBC = uibutton(app.PreviewButtonGrid, 'push');
            app.PvBC.ButtonPushedFcn = createCallbackFcn(app, @previewCallbacks, true);
            app.PvBC.FontName = 'Consolas';
            app.PvBC.Layout.Row = 3;
            app.PvBC.Layout.Column = 2;
            app.PvBC.Text = '[X/2,Y]';

            % Create PvBR
            app.PvBR = uibutton(app.PreviewButtonGrid, 'push');
            app.PvBR.ButtonPushedFcn = createCallbackFcn(app, @previewCallbacks, true);
            app.PvBR.FontName = 'Consolas';
            app.PvBR.Layout.Row = 3;
            app.PvBR.Layout.Column = 3;
            app.PvBR.Text = '[X,Y]';

            % Create PreviewFrGrid
            app.PreviewFrGrid = uigridlayout(app.PreviewButtonGrid);
            app.PreviewFrGrid.ColumnWidth = {'1x', 'fit', '1x', 'fit', '1x'};
            app.PreviewFrGrid.RowHeight = {24};
            app.PreviewFrGrid.ColumnSpacing = 4;
            app.PreviewFrGrid.RowSpacing = 4;
            app.PreviewFrGrid.Padding = [0 0 0 4];
            app.PreviewFrGrid.Layout.Row = 4;
            app.PreviewFrGrid.Layout.Column = [1 3];

            % Create PreviewButton
            app.PreviewButton = uibutton(app.PreviewFrGrid, 'push');
            app.PreviewButton.ButtonPushedFcn = createCallbackFcn(app, @previewCallbacks, true);
            app.PreviewButton.FontWeight = 'bold';
            app.PreviewButton.Layout.Row = 1;
            app.PreviewButton.Layout.Column = 1;
            app.PreviewButton.Text = 'Preview';

            % Create PvFrX
            app.PvFrX = uispinner(app.PreviewFrGrid);
            app.PvFrX.RoundFractionalValues = 'on';
            app.PvFrX.ValueDisplayFormat = '%.0f';
            app.PvFrX.ValueChangedFcn = createCallbackFcn(app, @previewCallbacks, true);
            app.PvFrX.Layout.Row = 1;
            app.PvFrX.Layout.Column = 3;
            app.PvFrX.Value = 1;

            % Create PvFrXLabel
            app.PvFrXLabel = uilabel(app.PreviewFrGrid);
            app.PvFrXLabel.HorizontalAlignment = 'right';
            app.PvFrXLabel.Layout.Row = 1;
            app.PvFrXLabel.Layout.Column = 2;
            app.PvFrXLabel.Text = 'X';

            % Create PvFrY
            app.PvFrY = uispinner(app.PreviewFrGrid);
            app.PvFrY.RoundFractionalValues = 'on';
            app.PvFrY.ValueDisplayFormat = '%.0f';
            app.PvFrY.ValueChangedFcn = createCallbackFcn(app, @previewCallbacks, true);
            app.PvFrY.Layout.Row = 1;
            app.PvFrY.Layout.Column = 5;
            app.PvFrY.Value = 1;

            % Create PvFrYLabel
            app.PvFrYLabel = uilabel(app.PreviewFrGrid);
            app.PvFrYLabel.HorizontalAlignment = 'right';
            app.PvFrYLabel.Layout.Row = 1;
            app.PvFrYLabel.Layout.Column = 4;
            app.PvFrYLabel.Text = 'Y';

            % Create AlignmentTab
            app.AlignmentTab = uitab(app.DfrnDetrTabGroup);
            app.AlignmentTab.Title = 'Align';
            app.AlignmentTab.BackgroundColor = [0.9412 0.9412 0.9412];

            % Create AlignmentGrid
            app.AlignmentGrid = uigridlayout(app.AlignmentTab);
            app.AlignmentGrid.ColumnWidth = {'1x'};
            app.AlignmentGrid.RowHeight = {'fit', 'fit', 18};
            app.AlignmentGrid.ColumnSpacing = 4;
            app.AlignmentGrid.RowSpacing = 4;
            app.AlignmentGrid.Padding = [4 4 4 4];

            % Create DfrnCalibPanel
            app.DfrnCalibPanel = uipanel(app.AlignmentGrid);
            app.DfrnCalibPanel.BorderType = 'none';
            app.DfrnCalibPanel.TitlePosition = 'centertop';
            app.DfrnCalibPanel.Title = 'Diffraction Calibration';
            app.DfrnCalibPanel.Layout.Row = 1;
            app.DfrnCalibPanel.Layout.Column = 1;
            app.DfrnCalibPanel.FontName = 'MS Sans Serif';
            app.DfrnCalibPanel.FontWeight = 'bold';

            % Create DfrnCalibGrid
            app.DfrnCalibGrid = uigridlayout(app.DfrnCalibPanel);
            app.DfrnCalibGrid.ColumnWidth = {'1x', 58, 58, '1x'};
            app.DfrnCalibGrid.RowHeight = {24, 24};
            app.DfrnCalibGrid.ColumnSpacing = 4;
            app.DfrnCalibGrid.RowSpacing = 4;
            app.DfrnCalibGrid.Padding = [0 0 0 4];

            % Create ConvergenceAngleLabel
            app.ConvergenceAngleLabel = uilabel(app.DfrnCalibGrid);
            app.ConvergenceAngleLabel.HorizontalAlignment = 'right';
            app.ConvergenceAngleLabel.Layout.Row = 1;
            app.ConvergenceAngleLabel.Layout.Column = [1 2];
            app.ConvergenceAngleLabel.Text = 'Convergence Angle';

            % Create Alpha
            app.Alpha = uieditfield(app.DfrnCalibGrid, 'numeric');
            app.Alpha.Limits = [0 Inf];
            app.Alpha.ValueDisplayFormat = '%.2f';
            app.Alpha.ValueChangedFcn = createCallbackFcn(app, @transBeamCallbacks, true);
            app.Alpha.Layout.Row = 1;
            app.Alpha.Layout.Column = 3;
            app.Alpha.Value = 1;

            % Create mradLabel
            app.mradLabel = uilabel(app.DfrnCalibGrid);
            app.mradLabel.Layout.Row = 1;
            app.mradLabel.Layout.Column = 4;
            app.mradLabel.Text = 'mrad';

            % Create mradpxLabel
            app.mradpxLabel = uilabel(app.DfrnCalibGrid);
            app.mradpxLabel.Layout.Row = 2;
            app.mradpxLabel.Layout.Column = 4;
            app.mradpxLabel.Text = 'mrad/px';

            % Create DiffractionScaleLabel
            app.DiffractionScaleLabel = uilabel(app.DfrnCalibGrid);
            app.DiffractionScaleLabel.HorizontalAlignment = 'right';
            app.DiffractionScaleLabel.Layout.Row = 2;
            app.DiffractionScaleLabel.Layout.Column = [1 2];
            app.DiffractionScaleLabel.Text = 'Diffraction Scale';

            % Create mradPx
            app.mradPx = uieditfield(app.DfrnCalibGrid, 'numeric');
            app.mradPx.Limits = [0 Inf];
            app.mradPx.ValueDisplayFormat = '%.7g';
            app.mradPx.ValueChangedFcn = createCallbackFcn(app, @transBeamCallbacks, true);
            app.mradPx.Layout.Row = 2;
            app.mradPx.Layout.Column = 3;
            app.mradPx.Value = 1;

            % Create AlignmentHelpIcon
            app.AlignmentHelpIcon = uiimage(app.AlignmentGrid);
            app.AlignmentHelpIcon.Tooltip = {'1. Set "Convergence Angle"'; '2. Align the transmitted beam''s X/Y location'; '3. Switch to other "Diffraction (Mode)" when finished'};
            app.AlignmentHelpIcon.Layout.Row = 3;
            app.AlignmentHelpIcon.Layout.Column = 1;
            app.AlignmentHelpIcon.ImageSource = 'help.png';

            % Create TransBeamAlignPanel
            app.TransBeamAlignPanel = uipanel(app.AlignmentGrid);
            app.TransBeamAlignPanel.BorderType = 'none';
            app.TransBeamAlignPanel.TitlePosition = 'centertop';
            app.TransBeamAlignPanel.Title = 'Transmitted Beam Position Alignment';
            app.TransBeamAlignPanel.Layout.Row = 2;
            app.TransBeamAlignPanel.Layout.Column = 1;
            app.TransBeamAlignPanel.FontName = 'MS Sans Serif';
            app.TransBeamAlignPanel.FontWeight = 'bold';

            % Create TransBeamAlignGrid
            app.TransBeamAlignGrid = uigridlayout(app.TransBeamAlignPanel);
            app.TransBeamAlignGrid.ColumnWidth = {'1x', 80, 80, '1x'};
            app.TransBeamAlignGrid.RowHeight = {24, 2, 24, 'fit', 2, 24, 'fit', 2, 24, 'fit'};
            app.TransBeamAlignGrid.ColumnSpacing = 4;
            app.TransBeamAlignGrid.RowSpacing = 2;
            app.TransBeamAlignGrid.Padding = [0 0 0 4];

            % Create TBAutoAlign
            app.TBAutoAlign = uibutton(app.TransBeamAlignGrid, 'push');
            app.TBAutoAlign.ButtonPushedFcn = createCallbackFcn(app, @transBeamCallbacks, true);
            app.TBAutoAlign.Layout.Row = 1;
            app.TBAutoAlign.Layout.Column = [2 3];
            app.TBAutoAlign.Text = 'Auto Align';

            % Create TBX
            app.TBX = uislider(app.TransBeamAlignGrid);
            app.TBX.MajorTicks = [];
            app.TBX.ValueChangedFcn = createCallbackFcn(app, @transBeamCallbacks, true);
            app.TBX.ValueChangingFcn = createCallbackFcn(app, @transBeamCallbacks, true);
            app.TBX.MinorTicks = [];
            app.TBX.Layout.Row = 7;
            app.TBX.Layout.Column = [1 4];

            % Create TBXLabel
            app.TBXLabel = uilabel(app.TransBeamAlignGrid);
            app.TBXLabel.HorizontalAlignment = 'right';
            app.TBXLabel.Layout.Row = 6;
            app.TBXLabel.Layout.Column = 2;
            app.TBXLabel.Text = 'X';

            % Create TBYLabel
            app.TBYLabel = uilabel(app.TransBeamAlignGrid);
            app.TBYLabel.HorizontalAlignment = 'right';
            app.TBYLabel.Layout.Row = 9;
            app.TBYLabel.Layout.Column = 2;
            app.TBYLabel.Text = 'Y';

            % Create TBY
            app.TBY = uislider(app.TransBeamAlignGrid);
            app.TBY.MajorTicks = [];
            app.TBY.ValueChangedFcn = createCallbackFcn(app, @transBeamCallbacks, true);
            app.TBY.ValueChangingFcn = createCallbackFcn(app, @transBeamCallbacks, true);
            app.TBY.MinorTicks = [];
            app.TBY.Layout.Row = 10;
            app.TBY.Layout.Column = [1 4];

            % Create TBRLabel
            app.TBRLabel = uilabel(app.TransBeamAlignGrid);
            app.TBRLabel.HorizontalAlignment = 'right';
            app.TBRLabel.Layout.Row = 3;
            app.TBRLabel.Layout.Column = 2;
            app.TBRLabel.Text = 'Radius';

            % Create TBR
            app.TBR = uislider(app.TransBeamAlignGrid);
            app.TBR.MajorTicks = [];
            app.TBR.ValueChangedFcn = createCallbackFcn(app, @transBeamCallbacks, true);
            app.TBR.ValueChangingFcn = createCallbackFcn(app, @transBeamCallbacks, true);
            app.TBR.MinorTicks = [];
            app.TBR.Layout.Row = 4;
            app.TBR.Layout.Column = [1 4];

            % Create TBR_NF
            app.TBR_NF = uispinner(app.TransBeamAlignGrid);
            app.TBR_NF.Step = 0.25;
            app.TBR_NF.ValueChangingFcn = createCallbackFcn(app, @transBeamCallbacks, true);
            app.TBR_NF.ValueDisplayFormat = '%.2f';
            app.TBR_NF.ValueChangedFcn = createCallbackFcn(app, @transBeamCallbacks, true);
            app.TBR_NF.Layout.Row = 3;
            app.TBR_NF.Layout.Column = 3;

            % Create TBR_NFLabel
            app.TBR_NFLabel = uilabel(app.TransBeamAlignGrid);
            app.TBR_NFLabel.Layout.Row = 3;
            app.TBR_NFLabel.Layout.Column = 4;
            app.TBR_NFLabel.Text = 'px';

            % Create TBX_NF
            app.TBX_NF = uispinner(app.TransBeamAlignGrid);
            app.TBX_NF.Step = 0.25;
            app.TBX_NF.ValueChangingFcn = createCallbackFcn(app, @transBeamCallbacks, true);
            app.TBX_NF.ValueDisplayFormat = '%.2f';
            app.TBX_NF.ValueChangedFcn = createCallbackFcn(app, @transBeamCallbacks, true);
            app.TBX_NF.Layout.Row = 6;
            app.TBX_NF.Layout.Column = 3;

            % Create TBX_NFLabel
            app.TBX_NFLabel = uilabel(app.TransBeamAlignGrid);
            app.TBX_NFLabel.Layout.Row = 6;
            app.TBX_NFLabel.Layout.Column = 4;
            app.TBX_NFLabel.Text = 'px';

            % Create TBY_NF
            app.TBY_NF = uispinner(app.TransBeamAlignGrid);
            app.TBY_NF.Step = 0.25;
            app.TBY_NF.ValueChangingFcn = createCallbackFcn(app, @transBeamCallbacks, true);
            app.TBY_NF.ValueDisplayFormat = '%.2f';
            app.TBY_NF.ValueChangedFcn = createCallbackFcn(app, @transBeamCallbacks, true);
            app.TBY_NF.Layout.Row = 9;
            app.TBY_NF.Layout.Column = 3;

            % Create TBY_NFLabel
            app.TBY_NFLabel = uilabel(app.TransBeamAlignGrid);
            app.TBY_NFLabel.Layout.Row = 9;
            app.TBY_NFLabel.Layout.Column = 4;
            app.TBY_NFLabel.Text = 'px';

            % Create TBCrossAlign
            app.TBCrossAlign = uibutton(app.TransBeamAlignGrid, 'push');
            app.TBCrossAlign.ButtonPushedFcn = createCallbackFcn(app, @transBeamCallbacks, true);
            app.TBCrossAlign.Tooltip = {'Align transmitted beam location as the crossing point of two lines'};
            app.TBCrossAlign.Layout.Row = 1;
            app.TBCrossAlign.Layout.Column = 4;
            app.TBCrossAlign.Text = 'X';

            % Create AnnularDetectorTab
            app.AnnularDetectorTab = uitab(app.DfrnDetrTabGroup);
            app.AnnularDetectorTab.Title = 'Ann';
            app.AnnularDetectorTab.BackgroundColor = [0.9412 0.9412 0.9412];

            % Create AnnDetrGrid
            app.AnnDetrGrid = uigridlayout(app.AnnularDetectorTab);
            app.AnnDetrGrid.ColumnWidth = {'1x'};
            app.AnnDetrGrid.RowHeight = {'fit', 'fit', 'fit', '1x'};
            app.AnnDetrGrid.ColumnSpacing = 4;
            app.AnnDetrGrid.RowSpacing = 4;
            app.AnnDetrGrid.Padding = [4 4 4 4];

            % Create AnnRPanel
            app.AnnRPanel = uipanel(app.AnnDetrGrid);
            app.AnnRPanel.BorderType = 'none';
            app.AnnRPanel.TitlePosition = 'centertop';
            app.AnnRPanel.Title = 'Annular Detector Radii';
            app.AnnRPanel.Layout.Row = 1;
            app.AnnRPanel.Layout.Column = 1;
            app.AnnRPanel.FontWeight = 'bold';

            % Create AnnRGrid
            app.AnnRGrid = uigridlayout(app.AnnRPanel);
            app.AnnRGrid.ColumnWidth = {24, '1x', 52, 80, '1x'};
            app.AnnRGrid.RowHeight = {24, 'fit', 2, 24, 'fit', 2};
            app.AnnRGrid.ColumnSpacing = 4;
            app.AnnRGrid.RowSpacing = 2;
            app.AnnRGrid.Padding = [0 0 0 4];

            % Create AnnRo_NF
            app.AnnRo_NF = uispinner(app.AnnRGrid);
            app.AnnRo_NF.Step = 0.25;
            app.AnnRo_NF.ValueChangingFcn = createCallbackFcn(app, @annularDetectorCallbacks, true);
            app.AnnRo_NF.ValueDisplayFormat = '%.2f';
            app.AnnRo_NF.ValueChangedFcn = createCallbackFcn(app, @annularDetectorCallbacks, true);
            app.AnnRo_NF.Tag = 'AnnDetr RO';
            app.AnnRo_NF.Layout.Row = 4;
            app.AnnRo_NF.Layout.Column = 4;

            % Create AnnRo_NFLabel
            app.AnnRo_NFLabel = uilabel(app.AnnRGrid);
            app.AnnRo_NFLabel.Layout.Row = 4;
            app.AnnRo_NFLabel.Layout.Column = 5;
            app.AnnRo_NFLabel.Text = 'mard';

            % Create AnnRi_NFLabel
            app.AnnRi_NFLabel = uilabel(app.AnnRGrid);
            app.AnnRi_NFLabel.Layout.Row = 1;
            app.AnnRi_NFLabel.Layout.Column = 5;
            app.AnnRi_NFLabel.Text = 'mrad';

            % Create AnnRi_NF
            app.AnnRi_NF = uispinner(app.AnnRGrid);
            app.AnnRi_NF.Step = 0.25;
            app.AnnRi_NF.ValueChangingFcn = createCallbackFcn(app, @annularDetectorCallbacks, true);
            app.AnnRi_NF.ValueDisplayFormat = '%.2f';
            app.AnnRi_NF.ValueChangedFcn = createCallbackFcn(app, @annularDetectorCallbacks, true);
            app.AnnRi_NF.Tag = 'AnnDetr RI';
            app.AnnRi_NF.Layout.Row = 1;
            app.AnnRi_NF.Layout.Column = 4;

            % Create AnnRi
            app.AnnRi = uislider(app.AnnRGrid);
            app.AnnRi.MajorTicks = [];
            app.AnnRi.ValueChangedFcn = createCallbackFcn(app, @annularDetectorCallbacks, true);
            app.AnnRi.ValueChangingFcn = createCallbackFcn(app, @annularDetectorCallbacks, true);
            app.AnnRi.MinorTicks = [];
            app.AnnRi.Tag = 'AnnDetr RI';
            app.AnnRi.Layout.Row = 2;
            app.AnnRi.Layout.Column = [1 5];

            % Create AnnRiLabel
            app.AnnRiLabel = uilabel(app.AnnRGrid);
            app.AnnRiLabel.HorizontalAlignment = 'right';
            app.AnnRiLabel.Layout.Row = 1;
            app.AnnRiLabel.Layout.Column = [2 3];
            app.AnnRiLabel.Text = 'Inner Radius';

            % Create AnnRo
            app.AnnRo = uislider(app.AnnRGrid);
            app.AnnRo.MajorTicks = [];
            app.AnnRo.ValueChangedFcn = createCallbackFcn(app, @annularDetectorCallbacks, true);
            app.AnnRo.ValueChangingFcn = createCallbackFcn(app, @annularDetectorCallbacks, true);
            app.AnnRo.MinorTicks = [];
            app.AnnRo.Tag = 'AnnDetr RO';
            app.AnnRo.Layout.Row = 5;
            app.AnnRo.Layout.Column = [1 5];

            % Create AnnRoLabel
            app.AnnRoLabel = uilabel(app.AnnRGrid);
            app.AnnRoLabel.HorizontalAlignment = 'right';
            app.AnnRoLabel.Layout.Row = 4;
            app.AnnRoLabel.Layout.Column = [2 3];
            app.AnnRoLabel.Text = 'Outer Radius';

            % Create AnnRLink
            app.AnnRLink = uibutton(app.AnnRGrid, 'state');
            app.AnnRLink.ValueChangedFcn = createCallbackFcn(app, @annularDetectorCallbacks, true);
            app.AnnRLink.Tag = 'AnnDetr';
            app.AnnRLink.Tooltip = {'Move inner/outer annular sliders together'};
            app.AnnRLink.Icon = 'link.png';
            app.AnnRLink.Text = '';
            app.AnnRLink.Layout.Row = 4;
            app.AnnRLink.Layout.Column = 1;

            % Create SegDetrPanel
            app.SegDetrPanel = uipanel(app.AnnDetrGrid);
            app.SegDetrPanel.BorderType = 'none';
            app.SegDetrPanel.TitlePosition = 'centertop';
            app.SegDetrPanel.Title = 'Segmented Detector Controls';
            app.SegDetrPanel.Layout.Row = 2;
            app.SegDetrPanel.Layout.Column = 1;
            app.SegDetrPanel.FontWeight = 'bold';

            % Create SegDetrGrid
            app.SegDetrGrid = uigridlayout(app.SegDetrPanel);
            app.SegDetrGrid.ColumnWidth = {44, 24, '1x', 32, 44, 32, '1x', 24};
            app.SegDetrGrid.RowHeight = {24, 1, 24, 'fit', 1};
            app.SegDetrGrid.ColumnSpacing = 4;
            app.SegDetrGrid.RowSpacing = 2;
            app.SegDetrGrid.Padding = [0 4 0 4];

            % Create SegmentsLabel
            app.SegmentsLabel = uilabel(app.SegDetrGrid);
            app.SegmentsLabel.HorizontalAlignment = 'right';
            app.SegmentsLabel.Layout.Row = [1 2];
            app.SegmentsLabel.Layout.Column = [1 2];
            app.SegmentsLabel.Text = 'Segments';

            % Create NSeg
            app.NSeg = uispinner(app.SegDetrGrid);
            app.NSeg.Limits = [2 32];
            app.NSeg.RoundFractionalValues = 'on';
            app.NSeg.ValueDisplayFormat = '%d';
            app.NSeg.ValueChangedFcn = createCallbackFcn(app, @annularDetectorCallbacks, true);
            app.NSeg.Tag = 'SegDetr';
            app.NSeg.Layout.Row = [1 2];
            app.NSeg.Layout.Column = [3 4];
            app.NSeg.Value = 4;

            % Create RungsLabel
            app.RungsLabel = uilabel(app.SegDetrGrid);
            app.RungsLabel.HorizontalAlignment = 'right';
            app.RungsLabel.Layout.Row = 1;
            app.RungsLabel.Layout.Column = 5;
            app.RungsLabel.Text = 'Rungs';

            % Create NRung
            app.NRung = uispinner(app.SegDetrGrid);
            app.NRung.Limits = [1 16];
            app.NRung.RoundFractionalValues = 'on';
            app.NRung.ValueDisplayFormat = '%d';
            app.NRung.ValueChangedFcn = createCallbackFcn(app, @annularDetectorCallbacks, true);
            app.NRung.Tag = 'SegDetr';
            app.NRung.Layout.Row = 1;
            app.NRung.Layout.Column = [6 7];
            app.NRung.Value = 1;

            % Create DetRot_NFLabel
            app.DetRot_NFLabel = uilabel(app.SegDetrGrid);
            app.DetRot_NFLabel.Layout.Row = [2 3];
            app.DetRot_NFLabel.Layout.Column = 7;
            app.DetRot_NFLabel.Text = '°';

            % Create DetRot_NF
            app.DetRot_NF = uispinner(app.SegDetrGrid);
            app.DetRot_NF.Step = 4;
            app.DetRot_NF.ValueChangingFcn = createCallbackFcn(app, @annularDetectorCallbacks, true);
            app.DetRot_NF.Limits = [-180 180];
            app.DetRot_NF.ValueDisplayFormat = '%.2f';
            app.DetRot_NF.ValueChangedFcn = createCallbackFcn(app, @annularDetectorCallbacks, true);
            app.DetRot_NF.Tag = 'SegDetr';
            app.DetRot_NF.Layout.Row = [2 3];
            app.DetRot_NF.Layout.Column = [5 6];

            % Create DetRotLabel
            app.DetRotLabel = uilabel(app.SegDetrGrid);
            app.DetRotLabel.HorizontalAlignment = 'right';
            app.DetRotLabel.Layout.Row = 3;
            app.DetRotLabel.Layout.Column = [1 4];
            app.DetRotLabel.Text = 'Rotation';

            % Create DetRot
            app.DetRot = uislider(app.SegDetrGrid);
            app.DetRot.Limits = [-180 180];
            app.DetRot.MajorTicks = [];
            app.DetRot.ValueChangedFcn = createCallbackFcn(app, @annularDetectorCallbacks, true);
            app.DetRot.ValueChangingFcn = createCallbackFcn(app, @annularDetectorCallbacks, true);
            app.DetRot.MinorTicks = [];
            app.DetRot.Tag = 'SegDetr';
            app.DetRot.Layout.Row = [4 5];
            app.DetRot.Layout.Column = [1 8];

            % Create ScanDirPanel
            app.ScanDirPanel = uipanel(app.AnnDetrGrid);
            app.ScanDirPanel.BorderType = 'none';
            app.ScanDirPanel.TitlePosition = 'centertop';
            app.ScanDirPanel.Title = 'Scanning Direction';
            app.ScanDirPanel.Layout.Row = 3;
            app.ScanDirPanel.Layout.Column = 1;
            app.ScanDirPanel.FontWeight = 'bold';

            % Create ScanDirGrid
            app.ScanDirGrid = uigridlayout(app.ScanDirPanel);
            app.ScanDirGrid.ColumnWidth = {24, 24, 24, 24, '1x', 80, '1x', 24};
            app.ScanDirGrid.RowHeight = {24, 14};
            app.ScanDirGrid.ColumnSpacing = 4;
            app.ScanDirGrid.RowSpacing = 2;
            app.ScanDirGrid.Padding = [0 0 0 4];

            % Create ScanDir_NFLabel
            app.ScanDir_NFLabel = uilabel(app.ScanDirGrid);
            app.ScanDir_NFLabel.Layout.Row = 1;
            app.ScanDir_NFLabel.Layout.Column = 7;
            app.ScanDir_NFLabel.Text = '°';

            % Create ScanDir_NF
            app.ScanDir_NF = uispinner(app.ScanDirGrid);
            app.ScanDir_NF.Step = 4;
            app.ScanDir_NF.ValueChangingFcn = createCallbackFcn(app, @annularDetectorCallbacks, true);
            app.ScanDir_NF.Limits = [-180 180];
            app.ScanDir_NF.ValueDisplayFormat = '%.2f';
            app.ScanDir_NF.ValueChangedFcn = createCallbackFcn(app, @annularDetectorCallbacks, true);
            app.ScanDir_NF.Tag = 'ScanDir';
            app.ScanDir_NF.Layout.Row = 1;
            app.ScanDir_NF.Layout.Column = 6;

            % Create ScanDir
            app.ScanDir = uislider(app.ScanDirGrid);
            app.ScanDir.Limits = [-180 180];
            app.ScanDir.MajorTicks = [];
            app.ScanDir.ValueChangedFcn = createCallbackFcn(app, @annularDetectorCallbacks, true);
            app.ScanDir.ValueChangingFcn = createCallbackFcn(app, @annularDetectorCallbacks, true);
            app.ScanDir.MinorTicks = [];
            app.ScanDir.Tag = 'ScanDir';
            app.ScanDir.Layout.Row = 2;
            app.ScanDir.Layout.Column = [1 8];

            % Create ScanDirLabel
            app.ScanDirLabel = uilabel(app.ScanDirGrid);
            app.ScanDirLabel.HorizontalAlignment = 'right';
            app.ScanDirLabel.Layout.Row = 1;
            app.ScanDirLabel.Layout.Column = [3 5];
            app.ScanDirLabel.Text = 'Angle';

            % Create ScanDirYFlip
            app.ScanDirYFlip = uibutton(app.ScanDirGrid, 'state');
            app.ScanDirYFlip.ValueChangedFcn = createCallbackFcn(app, @annularDetectorCallbacks, true);
            app.ScanDirYFlip.Tag = 'ScanDir';
            app.ScanDirYFlip.Tooltip = {'Flip Scan Y Direction'};
            app.ScanDirYFlip.Icon = 'axis-y.png';
            app.ScanDirYFlip.Text = '';
            app.ScanDirYFlip.FontWeight = 'bold';
            app.ScanDirYFlip.Layout.Row = 1;
            app.ScanDirYFlip.Layout.Column = 8;

            % Create ScanDirUnlock
            app.ScanDirUnlock = uibutton(app.ScanDirGrid, 'state');
            app.ScanDirUnlock.ValueChangedFcn = createCallbackFcn(app, @annularDetectorCallbacks, true);
            app.ScanDirUnlock.Tag = 'ScanDir';
            app.ScanDirUnlock.Icon = 'unlock.png';
            app.ScanDirUnlock.Text = '';
            app.ScanDirUnlock.Layout.Row = 1;
            app.ScanDirUnlock.Layout.Column = 1;

            % Create autoCurl
            app.autoCurl = uibutton(app.ScanDirGrid, 'push');
            app.autoCurl.ButtonPushedFcn = createCallbackFcn(app, @annularDetectorCallbacks, true);
            app.autoCurl.Layout.Row = 1;
            app.autoCurl.Layout.Column = [2 3];
            app.autoCurl.Text = 'Auto';

            % Create VirtualApertureTab
            app.VirtualApertureTab = uitab(app.DfrnDetrTabGroup);
            app.VirtualApertureTab.Title = 'Vr';

            % Create VirtualApertureGrid
            app.VirtualApertureGrid = uigridlayout(app.VirtualApertureTab);
            app.VirtualApertureGrid.ColumnWidth = {'1x'};
            app.VirtualApertureGrid.RowHeight = {'fit', 'fit', '1x'};
            app.VirtualApertureGrid.ColumnSpacing = 4;
            app.VirtualApertureGrid.RowSpacing = 4;
            app.VirtualApertureGrid.Padding = [4 4 4 4];

            % Create VrAperCoordPanel
            app.VrAperCoordPanel = uipanel(app.VirtualApertureGrid);
            app.VrAperCoordPanel.BorderType = 'none';
            app.VrAperCoordPanel.TitlePosition = 'centertop';
            app.VrAperCoordPanel.Title = 'Aperture Coordinates';
            app.VrAperCoordPanel.Layout.Row = 1;
            app.VrAperCoordPanel.Layout.Column = 1;
            app.VrAperCoordPanel.FontWeight = 'bold';

            % Create VrAperCoordGrid
            app.VrAperCoordGrid = uigridlayout(app.VrAperCoordPanel);
            app.VrAperCoordGrid.ColumnWidth = {'1x', 52, 24, 80, '1x'};
            app.VrAperCoordGrid.RowHeight = {24, 'fit', 2, 24, 'fit', 2, 24, 'fit', 2, 24};
            app.VrAperCoordGrid.ColumnSpacing = 4;
            app.VrAperCoordGrid.RowSpacing = 2;
            app.VrAperCoordGrid.Padding = [0 0 0 4];

            % Create VrApR_NFLabel
            app.VrApR_NFLabel = uilabel(app.VrAperCoordGrid);
            app.VrApR_NFLabel.Layout.Row = 1;
            app.VrApR_NFLabel.Layout.Column = 5;
            app.VrApR_NFLabel.Text = 'mrad';

            % Create VrApR_NF
            app.VrApR_NF = uispinner(app.VrAperCoordGrid);
            app.VrApR_NF.Step = 0.25;
            app.VrApR_NF.ValueChangingFcn = createCallbackFcn(app, @virtualApertureCallbacks, true);
            app.VrApR_NF.ValueDisplayFormat = '%.2f';
            app.VrApR_NF.ValueChangedFcn = createCallbackFcn(app, @virtualApertureCallbacks, true);
            app.VrApR_NF.Layout.Row = 1;
            app.VrApR_NF.Layout.Column = 4;

            % Create VrApRLabel
            app.VrApRLabel = uilabel(app.VrAperCoordGrid);
            app.VrApRLabel.HorizontalAlignment = 'right';
            app.VrApRLabel.Layout.Row = 1;
            app.VrApRLabel.Layout.Column = [2 3];
            app.VrApRLabel.Text = 'Radius';

            % Create VrApR
            app.VrApR = uislider(app.VrAperCoordGrid);
            app.VrApR.MajorTicks = [];
            app.VrApR.ValueChangedFcn = createCallbackFcn(app, @virtualApertureCallbacks, true);
            app.VrApR.ValueChangingFcn = createCallbackFcn(app, @virtualApertureCallbacks, true);
            app.VrApR.MinorTicks = [];
            app.VrApR.Layout.Row = 2;
            app.VrApR.Layout.Column = [1 5];

            % Create VrApX_NFLabel
            app.VrApX_NFLabel = uilabel(app.VrAperCoordGrid);
            app.VrApX_NFLabel.Layout.Row = 4;
            app.VrApX_NFLabel.Layout.Column = 5;
            app.VrApX_NFLabel.Text = 'mrad';

            % Create VrApX_NF
            app.VrApX_NF = uispinner(app.VrAperCoordGrid);
            app.VrApX_NF.Step = 0.25;
            app.VrApX_NF.ValueChangingFcn = createCallbackFcn(app, @virtualApertureCallbacks, true);
            app.VrApX_NF.ValueDisplayFormat = '%.2f';
            app.VrApX_NF.ValueChangedFcn = createCallbackFcn(app, @virtualApertureCallbacks, true);
            app.VrApX_NF.Layout.Row = 4;
            app.VrApX_NF.Layout.Column = 4;

            % Create VrApXLabel
            app.VrApXLabel = uilabel(app.VrAperCoordGrid);
            app.VrApXLabel.HorizontalAlignment = 'right';
            app.VrApXLabel.Layout.Row = 4;
            app.VrApXLabel.Layout.Column = [2 3];
            app.VrApXLabel.Text = 'X';

            % Create VrApX
            app.VrApX = uislider(app.VrAperCoordGrid);
            app.VrApX.MajorTicks = [];
            app.VrApX.ValueChangedFcn = createCallbackFcn(app, @virtualApertureCallbacks, true);
            app.VrApX.ValueChangingFcn = createCallbackFcn(app, @virtualApertureCallbacks, true);
            app.VrApX.MinorTicks = [];
            app.VrApX.Layout.Row = 5;
            app.VrApX.Layout.Column = [1 5];

            % Create VrApY_NFLabel
            app.VrApY_NFLabel = uilabel(app.VrAperCoordGrid);
            app.VrApY_NFLabel.Layout.Row = 7;
            app.VrApY_NFLabel.Layout.Column = 5;
            app.VrApY_NFLabel.Text = 'mrad';

            % Create VrApY_NF
            app.VrApY_NF = uispinner(app.VrAperCoordGrid);
            app.VrApY_NF.Step = 0.25;
            app.VrApY_NF.ValueChangingFcn = createCallbackFcn(app, @virtualApertureCallbacks, true);
            app.VrApY_NF.ValueDisplayFormat = '%.2f';
            app.VrApY_NF.ValueChangedFcn = createCallbackFcn(app, @virtualApertureCallbacks, true);
            app.VrApY_NF.Layout.Row = 7;
            app.VrApY_NF.Layout.Column = 4;

            % Create VrApYLabel
            app.VrApYLabel = uilabel(app.VrAperCoordGrid);
            app.VrApYLabel.HorizontalAlignment = 'right';
            app.VrApYLabel.Layout.Row = 7;
            app.VrApYLabel.Layout.Column = [2 3];
            app.VrApYLabel.Text = 'Y';

            % Create VrApY
            app.VrApY = uislider(app.VrAperCoordGrid);
            app.VrApY.MajorTicks = [];
            app.VrApY.ValueChangedFcn = createCallbackFcn(app, @virtualApertureCallbacks, true);
            app.VrApY.ValueChangingFcn = createCallbackFcn(app, @virtualApertureCallbacks, true);
            app.VrApY.MinorTicks = [];
            app.VrApY.Layout.Row = 8;
            app.VrApY.Layout.Column = [1 5];

            % Create VrAperRotGrid
            app.VrAperRotGrid = uigridlayout(app.VrAperCoordGrid);
            app.VrAperRotGrid.ColumnWidth = {24, '1x', 24, 'fit', 24, '1x', 24};
            app.VrAperRotGrid.RowHeight = {24};
            app.VrAperRotGrid.ColumnSpacing = 4;
            app.VrAperRotGrid.RowSpacing = 4;
            app.VrAperRotGrid.Padding = [0 0 0 0];
            app.VrAperRotGrid.Layout.Row = 10;
            app.VrAperRotGrid.Layout.Column = [1 5];

            % Create VrApReset
            app.VrApReset = uibutton(app.VrAperRotGrid, 'push');
            app.VrApReset.ButtonPushedFcn = createCallbackFcn(app, @virtualApertureCallbacks, true);
            app.VrApReset.Icon = 'home.png';
            app.VrApReset.FontWeight = 'bold';
            app.VrApReset.Tooltip = {'Home'};
            app.VrApReset.Layout.Row = 1;
            app.VrApReset.Layout.Column = 1;
            app.VrApReset.Text = '';

            % Create VrApRotCCW
            app.VrApRotCCW = uibutton(app.VrAperRotGrid, 'push');
            app.VrApRotCCW.ButtonPushedFcn = createCallbackFcn(app, @virtualApertureCallbacks, true);
            app.VrApRotCCW.Icon = 'left_rotate.png';
            app.VrApRotCCW.Layout.Row = 1;
            app.VrApRotCCW.Layout.Column = 3;
            app.VrApRotCCW.Text = '';

            % Create VrApRotStep
            app.VrApRotStep = uidropdown(app.VrAperRotGrid);
            app.VrApRotStep.Items = {'90°', '60°', '45°', '30°', '22.5°', '10°', '5°', '2°', '1°', '0.5°', '0.25°'};
            app.VrApRotStep.ItemsData = [90 60 45 30 22.5 10 5 2 1 0.5 0.25];
            app.VrApRotStep.ValueChangedFcn = createCallbackFcn(app, @virtualApertureCallbacks, true);
            app.VrApRotStep.Layout.Row = 1;
            app.VrApRotStep.Layout.Column = 4;
            app.VrApRotStep.Value = 90;

            % Create VrApRotCW
            app.VrApRotCW = uibutton(app.VrAperRotGrid, 'push');
            app.VrApRotCW.ButtonPushedFcn = createCallbackFcn(app, @virtualApertureCallbacks, true);
            app.VrApRotCW.Icon = 'right_rotate.png';
            app.VrApRotCW.Layout.Row = 1;
            app.VrApRotCW.Layout.Column = 5;
            app.VrApRotCW.Text = '';

            % Create VrApInvert
            app.VrApInvert = uibutton(app.VrAperRotGrid, 'state');
            app.VrApInvert.ValueChangedFcn = createCallbackFcn(app, @virtualApertureCallbacks, true);
            app.VrApInvert.Tooltip = {'Invert virtual aperture mask'};
            app.VrApInvert.Icon = 'invertColors.png';
            app.VrApInvert.Text = '';
            app.VrApInvert.Layout.Row = 1;
            app.VrApInvert.Layout.Column = 7;

            % Create VrAperSymmOptPanel
            app.VrAperSymmOptPanel = uipanel(app.VirtualApertureGrid);
            app.VrAperSymmOptPanel.BorderType = 'none';
            app.VrAperSymmOptPanel.TitlePosition = 'centertop';
            app.VrAperSymmOptPanel.Title = 'Symmetry Operations';
            app.VrAperSymmOptPanel.Layout.Row = 2;
            app.VrAperSymmOptPanel.Layout.Column = 1;
            app.VrAperSymmOptPanel.FontWeight = 'bold';

            % Create VrAperSymmOptGrid
            app.VrAperSymmOptGrid = uigridlayout(app.VrAperSymmOptPanel);
            app.VrAperSymmOptGrid.ColumnWidth = {'1x', 'fit', 'fit', '1x'};
            app.VrAperSymmOptGrid.RowHeight = {24, 'fit'};
            app.VrAperSymmOptGrid.ColumnSpacing = 4;
            app.VrAperSymmOptGrid.RowSpacing = 4;
            app.VrAperSymmOptGrid.Padding = [0 0 0 6];

            % Create VrApSymm
            app.VrApSymm = uidropdown(app.VrAperSymmOptGrid);
            app.VrApSymm.Items = {'1', '2', '3', '4', '6'};
            app.VrApSymm.ItemsData = [1 2 3 4 6];
            app.VrApSymm.ValueChangedFcn = createCallbackFcn(app, @virtualApertureCallbacks, true);
            app.VrApSymm.Layout.Row = 1;
            app.VrApSymm.Layout.Column = 3;
            app.VrApSymm.Value = 1;

            % Create VrApSymmLabel
            app.VrApSymmLabel = uilabel(app.VrAperSymmOptGrid);
            app.VrApSymmLabel.HorizontalAlignment = 'right';
            app.VrApSymmLabel.Layout.Row = 1;
            app.VrApSymmLabel.Layout.Column = 2;
            app.VrApSymmLabel.Text = 'Rotational Symmetry';

            % Create VrApMirrGrid
            app.VrApMirrGrid = uigridlayout(app.VrAperSymmOptGrid);
            app.VrApMirrGrid.ColumnWidth = {24, 24, 52, '1x', 80, '1x', 24};
            app.VrApMirrGrid.RowHeight = {24, 14};
            app.VrApMirrGrid.ColumnSpacing = 4;
            app.VrApMirrGrid.RowSpacing = 2;
            app.VrApMirrGrid.Padding = [0 0 0 0];
            app.VrApMirrGrid.Layout.Row = 2;
            app.VrApMirrGrid.Layout.Column = [1 4];

            % Create VrApMirrRot_NF
            app.VrApMirrRot_NF = uispinner(app.VrApMirrGrid);
            app.VrApMirrRot_NF.Step = 4;
            app.VrApMirrRot_NF.ValueChangingFcn = createCallbackFcn(app, @virtualApertureCallbacks, true);
            app.VrApMirrRot_NF.Limits = [-180 180];
            app.VrApMirrRot_NF.ValueDisplayFormat = '%.2f';
            app.VrApMirrRot_NF.ValueChangedFcn = createCallbackFcn(app, @virtualApertureCallbacks, true);
            app.VrApMirrRot_NF.Layout.Row = 1;
            app.VrApMirrRot_NF.Layout.Column = 5;

            % Create VrApMirrRot_NFLabel
            app.VrApMirrRot_NFLabel = uilabel(app.VrApMirrGrid);
            app.VrApMirrRot_NFLabel.Layout.Row = 1;
            app.VrApMirrRot_NFLabel.Layout.Column = 6;
            app.VrApMirrRot_NFLabel.Text = '°';

            % Create VrApMirrRotLabel
            app.VrApMirrRotLabel = uilabel(app.VrApMirrGrid);
            app.VrApMirrRotLabel.HorizontalAlignment = 'right';
            app.VrApMirrRotLabel.Layout.Row = 1;
            app.VrApMirrRotLabel.Layout.Column = [2 4];
            app.VrApMirrRotLabel.Text = 'Mirror Rotation';

            % Create VrApMirrRot
            app.VrApMirrRot = uislider(app.VrApMirrGrid);
            app.VrApMirrRot.Limits = [-180 180];
            app.VrApMirrRot.MajorTicks = [];
            app.VrApMirrRot.ValueChangedFcn = createCallbackFcn(app, @virtualApertureCallbacks, true);
            app.VrApMirrRot.ValueChangingFcn = createCallbackFcn(app, @virtualApertureCallbacks, true);
            app.VrApMirrRot.MinorTicks = [];
            app.VrApMirrRot.Layout.Row = 2;
            app.VrApMirrRot.Layout.Column = [1 7];

            % Create VrApMirror
            app.VrApMirror = uibutton(app.VrApMirrGrid, 'state');
            app.VrApMirror.ValueChangedFcn = createCallbackFcn(app, @virtualApertureCallbacks, true);
            app.VrApMirror.Tooltip = {'Mirrored'};
            app.VrApMirror.Icon = 'mirrored.png';
            app.VrApMirror.Text = '';
            app.VrApMirror.Layout.Row = 1;
            app.VrApMirror.Layout.Column = 1;

            % Create CustomDetectorTab
            app.CustomDetectorTab = uitab(app.DfrnDetrTabGroup);
            app.CustomDetectorTab.Title = 'C';

            % Create CustomDetectorGrid
            app.CustomDetectorGrid = uigridlayout(app.CustomDetectorTab);
            app.CustomDetectorGrid.ColumnWidth = {'1x'};
            app.CustomDetectorGrid.RowHeight = {'fit', 'fit', '1x', '0.8x'};
            app.CustomDetectorGrid.ColumnSpacing = 4;
            app.CustomDetectorGrid.RowSpacing = 0;
            app.CustomDetectorGrid.Padding = [0 0 0 0];

            % Create CDDetailsPanel
            app.CDDetailsPanel = uipanel(app.CustomDetectorGrid);
            app.CDDetailsPanel.BorderType = 'none';
            app.CDDetailsPanel.TitlePosition = 'centertop';
            app.CDDetailsPanel.BackgroundColor = [1 1 1];
            app.CDDetailsPanel.Layout.Row = 4;
            app.CDDetailsPanel.Layout.Column = 1;
            app.CDDetailsPanel.FontWeight = 'bold';

            % Create CDDetailsGrid
            app.CDDetailsGrid = uigridlayout(app.CDDetailsPanel);
            app.CDDetailsGrid.ColumnWidth = {24, '1x', 24};
            app.CDDetailsGrid.RowHeight = {24, 24, 24, 24, '1x'};
            app.CDDetailsGrid.ColumnSpacing = 1;
            app.CDDetailsGrid.RowSpacing = 1;
            app.CDDetailsGrid.Padding = [1 1 1 1];

            % Create CDFlipHorz
            app.CDFlipHorz = uibutton(app.CDDetailsGrid, 'push');
            app.CDFlipHorz.ButtonPushedFcn = createCallbackFcn(app, @customDetectorCallbacks, true);
            app.CDFlipHorz.Icon = 'mirrorHorz.png';
            app.CDFlipHorz.Tooltip = {'Flip mask vertically'};
            app.CDFlipHorz.Layout.Row = 2;
            app.CDFlipHorz.Layout.Column = 3;
            app.CDFlipHorz.Text = '';

            % Create CDFlipVert
            app.CDFlipVert = uibutton(app.CDDetailsGrid, 'push');
            app.CDFlipVert.ButtonPushedFcn = createCallbackFcn(app, @customDetectorCallbacks, true);
            app.CDFlipVert.Icon = 'mirrorVert.png';
            app.CDFlipVert.Tooltip = {'Flip mask horizontally'};
            app.CDFlipVert.Layout.Row = 3;
            app.CDFlipVert.Layout.Column = 3;
            app.CDFlipVert.Text = '';

            % Create CDTranspose
            app.CDTranspose = uibutton(app.CDDetailsGrid, 'push');
            app.CDTranspose.ButtonPushedFcn = createCallbackFcn(app, @customDetectorCallbacks, true);
            app.CDTranspose.Icon = 'transpose.png';
            app.CDTranspose.Tooltip = {'Transpose mask'};
            app.CDTranspose.Layout.Row = 4;
            app.CDTranspose.Layout.Column = 3;
            app.CDTranspose.Text = '';

            % Create CDMirror
            app.CDMirror = uibutton(app.CDDetailsGrid, 'state');
            app.CDMirror.ValueChangedFcn = createCallbackFcn(app, @customDetectorCallbacks, true);
            app.CDMirror.Tooltip = {'Mirrored'};
            app.CDMirror.Icon = 'mirrored.png';
            app.CDMirror.Text = '';
            app.CDMirror.Layout.Row = 2;
            app.CDMirror.Layout.Column = 1;

            % Create CDInvert
            app.CDInvert = uibutton(app.CDDetailsGrid, 'state');
            app.CDInvert.ValueChangedFcn = createCallbackFcn(app, @customDetectorCallbacks, true);
            app.CDInvert.Tooltip = {'Invert mask'};
            app.CDInvert.Icon = 'invertColors.png';
            app.CDInvert.Text = '';
            app.CDInvert.Layout.Row = 3;
            app.CDInvert.Layout.Column = 1;

            % Create CDRotGrid
            app.CDRotGrid = uigridlayout(app.CDDetailsGrid);
            app.CDRotGrid.ColumnWidth = {'fit', '1x', 1, 'fit', 24, 24};
            app.CDRotGrid.RowHeight = {24};
            app.CDRotGrid.ColumnSpacing = 1;
            app.CDRotGrid.RowSpacing = 4;
            app.CDRotGrid.Padding = [0 0 0 0];
            app.CDRotGrid.Layout.Row = 1;
            app.CDRotGrid.Layout.Column = [1 3];

            % Create CDRotStep
            app.CDRotStep = uidropdown(app.CDRotGrid);
            app.CDRotStep.Items = {'180°', '90°', '60°', '45°', '30°', '22.5°', '10°', '5°', '2°', '1°', '0.5°', '0.25°'};
            app.CDRotStep.ItemsData = [180 90 60 45 30 22.5 10 5 2 1 0.5 0.25];
            app.CDRotStep.Tooltip = {'Mask rotation step size'};
            app.CDRotStep.Layout.Row = 1;
            app.CDRotStep.Layout.Column = 4;
            app.CDRotStep.Value = 90;

            % Create CDRotCW
            app.CDRotCW = uibutton(app.CDRotGrid, 'push');
            app.CDRotCW.ButtonPushedFcn = createCallbackFcn(app, @customDetectorCallbacks, true);
            app.CDRotCW.Icon = 'right_rotate.png';
            app.CDRotCW.Tooltip = {'Rotate mask'};
            app.CDRotCW.Layout.Row = 1;
            app.CDRotCW.Layout.Column = 6;
            app.CDRotCW.Text = '';

            % Create CDRotCCW
            app.CDRotCCW = uibutton(app.CDRotGrid, 'push');
            app.CDRotCCW.ButtonPushedFcn = createCallbackFcn(app, @customDetectorCallbacks, true);
            app.CDRotCCW.Icon = 'left_rotate.png';
            app.CDRotCCW.Tooltip = {'Rotate mask'};
            app.CDRotCCW.Layout.Row = 1;
            app.CDRotCCW.Layout.Column = 5;
            app.CDRotCCW.Text = '';

            % Create CDIntraCombLabel
            app.CDIntraCombLabel = uilabel(app.CDRotGrid);
            app.CDIntraCombLabel.HorizontalAlignment = 'center';
            app.CDIntraCombLabel.Layout.Row = 1;
            app.CDIntraCombLabel.Layout.Column = 1;
            app.CDIntraCombLabel.Text = 'Intra-mask';

            % Create CDIntraMask
            app.CDIntraMask = uidropdown(app.CDRotGrid);
            app.CDIntraMask.Items = {'Union', 'Intersection', 'Additive'};
            app.CDIntraMask.ValueChangedFcn = createCallbackFcn(app, @customDetectorCallbacks, true);
            app.CDIntraMask.Tooltip = {'Combine different regions in mask as:'; 'Union, e.g. A = A1 ∪ A2 ∪ A3;'; 'Intersection, e.g. A = A1 ∩ A2 ∩ A3;'; 'Additive, e.g. A = A1 + A2 + A3.'};
            app.CDIntraMask.Layout.Row = 1;
            app.CDIntraMask.Layout.Column = 2;
            app.CDIntraMask.Value = 'Union';

            % Create CDDTable
            app.CDDTable = uitable(app.CDDetailsGrid);
            app.CDDTable.ColumnName = {'X'; 'Y'; 'R'};
            app.CDDTable.RowName = {};
            app.CDDTable.ColumnSortable = true;
            app.CDDTable.ColumnEditable = true;
            app.CDDTable.CellEditCallback = createCallbackFcn(app, @customDetectorCallbacks, true);
            app.CDDTable.Layout.Row = [2 5];
            app.CDDTable.Layout.Column = 2;

            % Create CDColor
            app.CDColor = uibutton(app.CDDetailsGrid, 'push');
            app.CDColor.ButtonPushedFcn = createCallbackFcn(app, @customDetectorCallbacks, true);
            app.CDColor.Icon = 'colorPicker.png';
            app.CDColor.Tooltip = {'Change color of current mask display'};
            app.CDColor.Layout.Row = 4;
            app.CDColor.Layout.Column = 1;
            app.CDColor.Text = '';

            % Create CDNewMaskGrid
            app.CDNewMaskGrid = uigridlayout(app.CustomDetectorGrid);
            app.CDNewMaskGrid.ColumnWidth = {'1x', 28, 28, 28, 28, 28, 28, 28, '1x'};
            app.CDNewMaskGrid.RowHeight = {28};
            app.CDNewMaskGrid.ColumnSpacing = 2;
            app.CDNewMaskGrid.RowSpacing = 4;
            app.CDNewMaskGrid.Padding = [4 0 4 4];
            app.CDNewMaskGrid.Layout.Row = 1;
            app.CDNewMaskGrid.Layout.Column = 1;

            % Create CDNewGrid
            app.CDNewGrid = uibutton(app.CDNewMaskGrid, 'push');
            app.CDNewGrid.ButtonPushedFcn = createCallbackFcn(app, @customDetectorCallbacks, true);
            app.CDNewGrid.Icon = 'grid.png';
            app.CDNewGrid.Tooltip = {'Add grid mask'};
            app.CDNewGrid.Layout.Row = 1;
            app.CDNewGrid.Layout.Column = 3;
            app.CDNewGrid.Text = '';

            % Create CDNewWedge
            app.CDNewWedge = uibutton(app.CDNewMaskGrid, 'push');
            app.CDNewWedge.ButtonPushedFcn = createCallbackFcn(app, @customDetectorCallbacks, true);
            app.CDNewWedge.Icon = 'wedge.png';
            app.CDNewWedge.FontSize = 10;
            app.CDNewWedge.Tooltip = {'Add wedge mask'};
            app.CDNewWedge.Layout.Row = 1;
            app.CDNewWedge.Layout.Column = 5;
            app.CDNewWedge.Text = '';

            % Create CDNewPolygon
            app.CDNewPolygon = uibutton(app.CDNewMaskGrid, 'push');
            app.CDNewPolygon.ButtonPushedFcn = createCallbackFcn(app, @customDetectorCallbacks, true);
            app.CDNewPolygon.Icon = 'poly.png';
            app.CDNewPolygon.Tooltip = {'Add polygon mask'};
            app.CDNewPolygon.Layout.Row = 1;
            app.CDNewPolygon.Layout.Column = 6;
            app.CDNewPolygon.Text = '';

            % Create CDNewFromFile
            app.CDNewFromFile = uibutton(app.CDNewMaskGrid, 'push');
            app.CDNewFromFile.ButtonPushedFcn = createCallbackFcn(app, @customDetectorCallbacks, true);
            app.CDNewFromFile.Icon = 'openMask.png';
            app.CDNewFromFile.Tooltip = {'Add mask from file'};
            app.CDNewFromFile.Layout.Row = 1;
            app.CDNewFromFile.Layout.Column = 7;
            app.CDNewFromFile.Text = '';

            % Create CDNewBandpass
            app.CDNewBandpass = uibutton(app.CDNewMaskGrid, 'push');
            app.CDNewBandpass.ButtonPushedFcn = createCallbackFcn(app, @customDetectorCallbacks, true);
            app.CDNewBandpass.Icon = 'bandpass.png';
            app.CDNewBandpass.Tooltip = {'Add bandpass mask'};
            app.CDNewBandpass.Layout.Row = 1;
            app.CDNewBandpass.Layout.Column = 4;
            app.CDNewBandpass.Text = '';

            % Create CDNewCircle
            app.CDNewCircle = uibutton(app.CDNewMaskGrid, 'push');
            app.CDNewCircle.ButtonPushedFcn = createCallbackFcn(app, @customDetectorCallbacks, true);
            app.CDNewCircle.Icon = 'circle.png';
            app.CDNewCircle.Tooltip = {'Add circular mask'};
            app.CDNewCircle.Layout.Row = 1;
            app.CDNewCircle.Layout.Column = 2;
            app.CDNewCircle.Text = '';

            % Create CDNewMath
            app.CDNewMath = uibutton(app.CDNewMaskGrid, 'push');
            app.CDNewMath.ButtonPushedFcn = createCallbackFcn(app, @customDetectorCallbacks, true);
            app.CDNewMath.Icon = 'math.png';
            app.CDNewMath.Tooltip = {'Add mask from formula'};
            app.CDNewMath.Layout.Row = 1;
            app.CDNewMath.Layout.Column = 8;
            app.CDNewMath.Text = '';

            % Create CDInterMaskGrid
            app.CDInterMaskGrid = uigridlayout(app.CustomDetectorGrid);
            app.CDInterMaskGrid.ColumnWidth = {24, '1x', 'fit', 'fit', '1x', 24};
            app.CDInterMaskGrid.RowHeight = {24};
            app.CDInterMaskGrid.ColumnSpacing = 4;
            app.CDInterMaskGrid.RowSpacing = 6;
            app.CDInterMaskGrid.Padding = [4 4 4 4];
            app.CDInterMaskGrid.Layout.Row = 2;
            app.CDInterMaskGrid.Layout.Column = 1;

            % Create IntermaskLabel
            app.IntermaskLabel = uilabel(app.CDInterMaskGrid);
            app.IntermaskLabel.HorizontalAlignment = 'right';
            app.IntermaskLabel.FontWeight = 'bold';
            app.IntermaskLabel.Layout.Row = 1;
            app.IntermaskLabel.Layout.Column = 3;
            app.IntermaskLabel.Text = 'Inter-mask';

            % Create CDInterMask
            app.CDInterMask = uidropdown(app.CDInterMaskGrid);
            app.CDInterMask.Items = {'Union', 'Intersection', 'Additive', 'Current-only'};
            app.CDInterMask.ValueChangedFcn = createCallbackFcn(app, @customDetectorCallbacks, true);
            app.CDInterMask.Tooltip = {'Combine different custom masks as:'; 'Union, e.g. Final = A ∪ B ∪ C;'; 'Intersection, e.g. Final = A ∩ B ∩ C;'; 'Additive, e.g. Final = A*WtA + B*WtB + C*WtC;'; 'Current-only, i.e. only the selected mask.'; 'Zero-weighted masks are always ignored. Weightings have no effect in Union and Intersection. Weightings are applied unnormalised in Additive and Current-only.'};
            app.CDInterMask.FontWeight = 'bold';
            app.CDInterMask.Layout.Row = 1;
            app.CDInterMask.Layout.Column = 4;
            app.CDInterMask.Value = 'Union';

            % Create ShowDfrnMaskWdw
            app.ShowDfrnMaskWdw = uibutton(app.CDInterMaskGrid, 'push');
            app.ShowDfrnMaskWdw.ButtonPushedFcn = createCallbackFcn(app, @showWindowCallbacks, true);
            app.ShowDfrnMaskWdw.Tag = 'DfrnMask';
            app.ShowDfrnMaskWdw.Icon = 'Aperture.png';
            app.ShowDfrnMaskWdw.Tooltip = {'Show Diffraction Mask Image'};
            app.ShowDfrnMaskWdw.Layout.Row = 1;
            app.ShowDfrnMaskWdw.Layout.Column = 1;
            app.ShowDfrnMaskWdw.Text = '';

            % Create CDDelMask
            app.CDDelMask = uibutton(app.CDInterMaskGrid, 'push');
            app.CDDelMask.ButtonPushedFcn = createCallbackFcn(app, @customDetectorCallbacks, true);
            app.CDDelMask.Icon = 'delete.png';
            app.CDDelMask.FontWeight = 'bold';
            app.CDDelMask.Tooltip = {'Delete seleced mask'};
            app.CDDelMask.Layout.Row = 1;
            app.CDDelMask.Layout.Column = 6;
            app.CDDelMask.Text = '';

            % Create CDT
            app.CDT = uitable(app.CustomDetectorGrid);
            app.CDT.ColumnName = {'ID'; 'Type'; 'Label'; '✅'; '👁'; 'μ'};
            app.CDT.RowName = {};
            app.CDT.ColumnSortable = [false true true false false false];
            app.CDT.ColumnEditable = [false false true true true true];
            app.CDT.RowStriping = 'off';
            app.CDT.CellEditCallback = createCallbackFcn(app, @customDetectorCallbacks, true);
            app.CDT.CellSelectionCallback = createCallbackFcn(app, @customDetectorCallbacks, true);
            app.CDT.Tooltip = {'✅: Enable mask.'; '👁: Show annotation on pattern.'; 'μ: Weighting.'};
            app.CDT.FontName = 'MS Sans Serif';
            app.CDT.Layout.Row = 3;
            app.CDT.Layout.Column = 1;

            % Create DebugContextMenu
            app.DebugContextMenu = uicontextmenu(app.Quant4D_Fig);

            % Create Test1Menu
            app.Test1Menu = uimenu(app.DebugContextMenu);
            app.Test1Menu.MenuSelectedFcn = createCallbackFcn(app, @test1, true);
            app.Test1Menu.Text = 'Test1';

            % Create Test2Menu
            app.Test2Menu = uimenu(app.DebugContextMenu);
            app.Test2Menu.MenuSelectedFcn = createCallbackFcn(app, @test2, true);
            app.Test2Menu.Text = 'Test2';

            % Create SaveVecMenu
            app.SaveVecMenu = uimenu(app.DebugContextMenu);
            app.SaveVecMenu.MenuSelectedFcn = createCallbackFcn(app, @firstMoment, true);
            app.SaveVecMenu.Text = 'SaveVec';

            % Create ReimportMenu
            app.ReimportMenu = uimenu(app.DebugContextMenu);
            app.ReimportMenu.MenuSelectedFcn = createCallbackFcn(app, @importCallbacks, true);
            app.ReimportMenu.Text = 'Re-import';

            % Create ResetQuant4DMenu
            app.ResetQuant4DMenu = uimenu(app.DebugContextMenu);
            app.ResetQuant4DMenu.MenuSelectedFcn = createCallbackFcn(app, @resetQuant4DCallbacks, true);
            app.ResetQuant4DMenu.Text = 'ResetQuant4D';

            % Create EnableallUIsMenu
            app.EnableallUIsMenu = uimenu(app.DebugContextMenu);
            app.EnableallUIsMenu.MenuSelectedFcn = createCallbackFcn(app, @enableAllUICallbacks, true);
            app.EnableallUIsMenu.Text = 'Enable all UIs';
            
            % Assign app.DebugContextMenu
            app.ShowImportWdw.ContextMenu = app.DebugContextMenu;

            % Create CDDelContext
            app.CDDelContext = uicontextmenu(app.Quant4D_Fig);

            % Create CDDelResetMenu
            app.CDDelResetMenu = uimenu(app.CDDelContext);
            app.CDDelResetMenu.MenuSelectedFcn = createCallbackFcn(app, @customDetectorCallbacks, true);
            app.CDDelResetMenu.Text = 'Reset';
            
            % Assign app.CDDelContext
            app.CDNewMaskGrid.ContextMenu = app.CDDelContext;
            app.CDDelMask.ContextMenu = app.CDDelContext;

            % Show the figure after all components are created
            app.Quant4D_Fig.Visible = 'on';
        end
    end

    % App creation and deletion
    methods (Access = public)

        % Construct app
        function app = Quant4D_exported(varargin)

            % Create UIFigure and components
            createComponents(app)

            % Register the app with App Designer
            registerApp(app, app.Quant4D_Fig)

            % Execute the startup function
            runStartupFcn(app, @(app)startupFcn(app, varargin{:}))

            if nargout == 0
                clear app
            end
        end

        % Code that executes before app deletion
        function delete(app)

            % Delete UIFigure when app is deleted
            delete(app.Quant4D_Fig)
        end
    end
end