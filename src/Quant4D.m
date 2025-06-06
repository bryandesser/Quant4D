classdef Quant4D < matlab.apps.AppBase

    % Properties that correspond to self components
    properties (Access = public)
        Quant4D_Fig                     matlab.ui.Figure
        diffraction_dropdown            matlab.ui.control.DropDown
        Quant4D_FigGrid                 matlab.ui.container.GridLayout
        RealPanelGrid                   matlab.ui.container.GridLayout
        RealPanel                       matlab.ui.container.Panel
        RealGrid                        matlab.ui.container.GridLayout
        RealROIShape                    matlab.ui.control.DropDown
        RealROIGrid                     matlab.ui.container.GridLayout
        RealROIFrameLabel               matlab.ui.control.Label
        RealROIFrameX                   matlab.ui.control.Spinner
        RealXLabel                      matlab.ui.control.Label
        RealROIFrameY                   matlab.ui.control.Spinner
        RealYLabel                      matlab.ui.control.Label
        ShowRealMaskWindow              matlab.ui.control.Button
        RealROIInvert                   matlab.ui.control.StateButton
        ModePanel                       matlab.ui.container.Panel
        ModeGrid                        matlab.ui.container.GridLayout
        Mode                            matlab.ui.control.DropDown
        ShortcutButtonGrid              matlab.ui.container.GridLayout
        ShowSettingsWindow              matlab.ui.control.Button
        UpdateImages                    matlab.ui.control.Button
        AutoSaveImage                   matlab.ui.control.Button
        ShowSaveWindow                  matlab.ui.control.Button
        ShowImportWindow                matlab.ui.control.Button
        ModeTabGroup                    matlab.ui.container.TabGroup
        PreviewTab                      matlab.ui.container.Tab
        PreviewGrid                     matlab.ui.container.GridLayout
        PreviewFramePanel               matlab.ui.container.Panel
        PreviewButtonGrid               matlab.ui.container.GridLayout
        PreviewFrameGrid                matlab.ui.container.GridLayout
        PreviewFrameY                   matlab.ui.control.Spinner
        PvFrYLabel                      matlab.ui.control.Label
        PreviewFrameX                   matlab.ui.control.Spinner
        PvFrXLabel                      matlab.ui.control.Label
        PreviewButton                   matlab.ui.control.Button
        PreviewFrame_X_Y                matlab.ui.control.Button
        PreviewFrame_X2_Y               matlab.ui.control.Button
        PreviewFrame_1_Y                matlab.ui.control.Button
        PreviewFrame_X_Y2               matlab.ui.control.Button
        PreviewFrame_X2_Y2              matlab.ui.control.Button
        PreviewFrame_1_Y2               matlab.ui.control.Button
        PreviewFrame_X_1                matlab.ui.control.Button
        PreviewFrame_X2_1               matlab.ui.control.Button
        PreviewFrame_1_1                matlab.ui.control.Button
        AlignmentTab                    matlab.ui.container.Tab
        AlignmentGrid                   matlab.ui.container.GridLayout
        AlignmentHelpIcon               matlab.ui.control.Image
        TransBeamAlignPanel             matlab.ui.container.Panel
        TransBeamAlignGrid              matlab.ui.container.GridLayout
        TransBeamY                      matlab.ui.control.Slider
        TBY_NFLabel                     matlab.ui.control.Label
        TransBeamYSpinner               matlab.ui.control.Spinner
        TBYLabel                        matlab.ui.control.Label
        TransBeamX                      matlab.ui.control.Slider
        TBX_NFLabel                     matlab.ui.control.Label
        TransBeamXSpinner               matlab.ui.control.Spinner
        TBXLabel                        matlab.ui.control.Label
        TransBeamR                      matlab.ui.control.Slider
        TBR_NFLabel                     matlab.ui.control.Label
        TransBeamRSpinner               matlab.ui.control.Spinner
        TBRLabel                        matlab.ui.control.Label
        TBCrossAlign                    matlab.ui.control.Button
        TBAutoAlign                     matlab.ui.control.Button
        DiffractionCalibrationPanel     matlab.ui.container.Panel
        DiffractionCalibrationGrid      matlab.ui.container.GridLayout
        mradPxLabel                     matlab.ui.control.Label
        mradPx                          matlab.ui.control.NumericEditField
        DiffractionScaleLabel           matlab.ui.control.Label
        AlphaLabel                      matlab.ui.control.Label
        Alpha                           matlab.ui.control.NumericEditField
        ConvergenceAngleLabel           matlab.ui.control.Label
        AnnularDetectorTab              matlab.ui.container.Tab
        AnnularDetectorGrid             matlab.ui.container.GridLayout
        AnnularStepGrid                 matlab.ui.container.GridLayout
        AnnularStep                     matlab.ui.control.NumericEditField
        AnnularIntegrationStepEditFieldLabel  matlab.ui.control.Label
        SegmentedDetectorPanel          matlab.ui.container.Panel
        SegmentedDetectorGrid           matlab.ui.container.GridLayout
        DetectorRotationSlider          matlab.ui.control.Slider
        DetRot_NFLabel                  matlab.ui.control.Label
        DetectorRotationSpinner         matlab.ui.control.Spinner
        DetRotLabel                     matlab.ui.control.Label
        NRung                           matlab.ui.control.Spinner
        RungsLabel                      matlab.ui.control.Label
        NSeg                            matlab.ui.control.Spinner
        SegmentsLabel                   matlab.ui.control.Label
        ScanDirectionPanel              matlab.ui.container.Panel
        ScanDirectionGrid               matlab.ui.container.GridLayout
        ScanDirectionSlider             matlab.ui.control.Slider
        FlipScanDirectionY              matlab.ui.control.StateButton
        ScanDir_NFLabel                 matlab.ui.control.Label
        ScanDirectionSpinner            matlab.ui.control.Spinner
        ScanDirLabel                    matlab.ui.control.Label
        AutoCurl                        matlab.ui.control.Button
        ScanDirectionLock               matlab.ui.control.StateButton
        AnnularRadiiPanel               matlab.ui.container.Panel
        AnnularRadiiGrid                matlab.ui.container.GridLayout
        OuterAnnularRadius              matlab.ui.control.Slider
        AnnRo_NFLabel                   matlab.ui.control.Label
        OuterAnnularRadiusSpinner       matlab.ui.control.Spinner
        AnnRoLabel                      matlab.ui.control.Label
        AnnularRadiusLink               matlab.ui.control.StateButton
        InnerAnnularRadius              matlab.ui.control.Slider
        AnnRi_NFLabel                   matlab.ui.control.Label
        InnerAnnularRadiusSpinner       matlab.ui.control.Spinner
        AnnRiLabel                      matlab.ui.control.Label
        VirtualApertureTab              matlab.ui.container.Tab
        VirtualApertureGrid             matlab.ui.container.GridLayout
        VirtualApertureSymmetryPanel    matlab.ui.container.Panel
        VirtualApertureSymmetryGrid     matlab.ui.container.GridLayout
        VirtualApertureMirrorGrid       matlab.ui.container.GridLayout
        VirtualApertureMirrorRotation   matlab.ui.control.Slider
        VrApMirrRot_NFLabel             matlab.ui.control.Label
        VirtualApertureMirrorRotationSpinner  matlab.ui.control.Spinner
        VrApMirrRotLabel                matlab.ui.control.Label
        VirtualApertureMirror           matlab.ui.control.StateButton
        VirtualApertureSymmetry         matlab.ui.control.DropDown
        VrApSymmLabel                   matlab.ui.control.Label
        VirtualApertureCoordinatesPanel  matlab.ui.container.Panel
        VirtualApertureCoordinatesGrid  matlab.ui.container.GridLayout
        VirtualApertureRotationGrid     matlab.ui.container.GridLayout
        AnnularStepGrid_2               matlab.ui.container.GridLayout
        AnnularStep_2                   matlab.ui.control.NumericEditField
        AnnularIntegrationStepEditFieldLabel_2  matlab.ui.control.Label
        VirtualApertureInvert           matlab.ui.control.StateButton
        VirtualApertureRotateCW         matlab.ui.control.Button
        VirtualApertureRotationStep     matlab.ui.control.DropDown
        VirtualApertureRotateCCW        matlab.ui.control.Button
        VirtualApertureReset            matlab.ui.control.Button
        VirtualApertureY                matlab.ui.control.Slider
        VrApY_NFLabel                   matlab.ui.control.Label
        VirtualApertureYSpinner         matlab.ui.control.Spinner
        VrApYLabel                      matlab.ui.control.Label
        VirtualApertureX                matlab.ui.control.Slider
        VrApX_NFLabel                   matlab.ui.control.Label
        VirtualApertureXSpinner         matlab.ui.control.Spinner
        VrApXLabel                      matlab.ui.control.Label
        VirtualApertureR                matlab.ui.control.Slider
        VrApR_NFLabel                   matlab.ui.control.Label
        VirtualApertureRSpinner         matlab.ui.control.Spinner
        VrApRLabel                      matlab.ui.control.Label
        CustomDetectorTab               matlab.ui.container.Tab
        CustomDetectorGrid              matlab.ui.container.GridLayout
        CustomDetectorDetailsPanel      matlab.ui.container.Panel
        CustomDetectorDetailsGrid       matlab.ui.container.GridLayout
        CustomDetectorTranspose         matlab.ui.control.StateButton
        CustomDetectorFlipVertical      matlab.ui.control.StateButton
        CustomDetectorFlipHorizontal    matlab.ui.control.StateButton
        CustomDetectorColor             matlab.ui.control.Button
        CustomDetectorInvert            matlab.ui.control.StateButton
        CustomDetectorDetailsTable      matlab.ui.control.Table
        CustomDetectorMirror            matlab.ui.control.StateButton
        CustomDetectorRotationGrid      matlab.ui.container.GridLayout
        CustomDetectorRotateCW          matlab.ui.control.Button
        CustomDetectorRotateCCW         matlab.ui.control.Button
        CustomDetectorRotationStep      matlab.ui.control.DropDown
        CustomDetectorIntraMask         matlab.ui.control.DropDown
        CDIntraCombLabel                matlab.ui.control.Label
        CustomDetectorTable             matlab.ui.control.Table
        CustomDetectorInterMaskGrid     matlab.ui.container.GridLayout
        CustomDetectorDeleteMask        matlab.ui.control.Button
        CustomDetectorInterMask         matlab.ui.control.DropDown
        IntermaskLabel                  matlab.ui.control.Label
        ShowDiffractionMaskWindow       matlab.ui.control.Button
        CustomDetectorNewMaskGrid       matlab.ui.container.GridLayout
        CustomDetectorNewGridNoCenter   matlab.ui.control.Button
        CustomDetectorNewMath           matlab.ui.control.Button
        CustomDetectorNewFromFile       matlab.ui.control.Button
        CustomDetectorNewPolygon        matlab.ui.control.Button
        CustomDetectorNewWedge          matlab.ui.control.Button
        CustomDetectorNewBandpass       matlab.ui.control.Button
        CustomDetectorNewGrid           matlab.ui.control.Button
        CustomDetectorNewCircle         matlab.ui.control.Button
        SettingsPanel                   matlab.ui.container.Panel
        SettingsGrid                    matlab.ui.container.GridLayout
        SettingsTabGroup                matlab.ui.container.TabGroup
        DisplayTab                      matlab.ui.container.Tab
        DisplayGrid                     matlab.ui.container.GridLayout
        DispContrastsGrid               matlab.ui.container.GridLayout
        DisplayMaskOpacitySpinner       matlab.ui.control.Spinner
        DisplayMaskOpacitySlider        matlab.ui.control.Slider
        ShowMaskWindow                  matlab.ui.control.Button
        DisplayGammaSpinner             matlab.ui.control.Spinner
        DisplayGamma                    matlab.ui.control.Slider
        DisplayGammaReset               matlab.ui.control.Button
        DisplayContrastSpinner          matlab.ui.control.Spinner
        DisplayContrast                 matlab.ui.control.Slider
        DisplayContrastReset            matlab.ui.control.Button
        DisplayBrightnessSpinner        matlab.ui.control.Spinner
        DisplayBrightness               matlab.ui.control.Slider
        DisplayBrightnessReset          matlab.ui.control.Button
        HistogramGrid                   matlab.ui.container.GridLayout
        HistogramLog                    matlab.ui.control.StateButton
        HistogramAxes                   matlab.ui.control.UIAxes
        ImageStatistics                 matlab.ui.control.TextArea
        DisplayDropDownGrid             matlab.ui.container.GridLayout
        DispColorMapInvert              matlab.ui.control.StateButton
        DispColorMap                    matlab.ui.control.DropDown
        ColormapLabel                   matlab.ui.control.Label
        DisplayLock                     matlab.ui.control.StateButton
        DisplayImage                    matlab.ui.control.DropDown
        ImageLabel                      matlab.ui.control.Label
        ShowImageWindow                 matlab.ui.control.Button
        WindowsTab                      matlab.ui.container.Tab
        WindowsTabGrid                  matlab.ui.container.GridLayout
        WindowResizePanel               matlab.ui.container.Panel
        WindowResizeGrid                matlab.ui.container.GridLayout
        WindowResizeTabGroup            matlab.ui.container.TabGroup
        DiffractionTab                  matlab.ui.container.Tab
        DiffractionTabGrid              matlab.ui.container.GridLayout
        DiffractionWindowPanel          matlab.ui.container.Panel
        DiffractionWindowGrid           matlab.ui.container.GridLayout
        SetAllDiffractionWindows        matlab.ui.control.Button
        SetDiffractionWindow            matlab.ui.control.Button
        SetDiffractionWindowHeight      matlab.ui.control.NumericEditField
        HEditFieldLabel                 matlab.ui.control.Label
        SetDiffractionWindowWidth       matlab.ui.control.NumericEditField
        WEditFieldLabel                 matlab.ui.control.Label
        DiffractionAxesGrid             matlab.ui.container.GridLayout
        RotateDiffraction               matlab.ui.control.DropDown
        RotateDiffractionIcon           matlab.ui.control.Image
        ReverseDiffractionY             matlab.ui.control.StateButton
        ReverseDiffractionX             matlab.ui.control.StateButton
        ShowDiffractionAxes             matlab.ui.control.StateButton
        RealspaceTab                    matlab.ui.container.Tab
        RealspaceTabGrid                matlab.ui.container.GridLayout
        RealWindowPanel                 matlab.ui.container.Panel
        RealWindowGrid                  matlab.ui.container.GridLayout
        SetRealWindowWidth              matlab.ui.control.NumericEditField
        WEditField_2Label               matlab.ui.control.Label
        SetAllRealWindows               matlab.ui.control.Button
        SetRealWindow                   matlab.ui.control.Button
        SetRealWindowHeight             matlab.ui.control.NumericEditField
        HEditField_2Label               matlab.ui.control.Label
        RealAxesGrid                    matlab.ui.container.GridLayout
        RotateReal                      matlab.ui.control.DropDown
        RotateRealIcon                  matlab.ui.control.Image
        ReverseRealY                    matlab.ui.control.StateButton
        ReverseRealX                    matlab.ui.control.StateButton
        ShowRealAxes                    matlab.ui.control.StateButton
        ShowImageWindowsPanel           matlab.ui.container.Panel
        ShowImageWindowsGrid            matlab.ui.container.GridLayout
        VectorSamplingGrid              matlab.ui.container.GridLayout
        ShowColorWheelWindow            matlab.ui.control.Button
        DisplayVectorColor              matlab.ui.control.Button
        DisplayVectorField              matlab.ui.control.DropDown
        DispVecFieldLabel               matlab.ui.control.Label
        ShowiCoMWindow                  matlab.ui.control.Button
        ShowdCoMWindow                  matlab.ui.control.Button
        ShowCoMYWindow                  matlab.ui.control.Button
        ShowCoMXWindow                  matlab.ui.control.Button
        ShowCoMMagnitudeWindow          matlab.ui.control.Button
        ShowCoMPhaseWindow              matlab.ui.control.Button
        ShowCoMPhaseMagnitudeWindow     matlab.ui.control.Button
        ShowColorWheelWindow2           matlab.ui.control.Button
        ShowRealMaskWindow2             matlab.ui.control.Button
        ShowRealWindow                  matlab.ui.control.Button
        ShowDiffractionMaskWindow2      matlab.ui.control.Button
        ShowDiffractionWindow           matlab.ui.control.Button
        BandpassFilterPanel             matlab.ui.container.Panel
        BandpassFilterGrid              matlab.ui.container.GridLayout
        BandpassFilterLow               matlab.ui.control.Spinner
        BandpassFilterHigh              matlab.ui.control.Spinner
        BandpassFilter                  matlab.ui.control.RangeSlider
        MiscTab                         matlab.ui.container.Tab
        MiscGrid                        matlab.ui.container.GridLayout
        DatasetOptionPanel              matlab.ui.container.Panel
        DatasetOptionGrid               matlab.ui.container.GridLayout
        SwapRealXY                      matlab.ui.control.Button
        SwapDiffractionXY               matlab.ui.control.Button
        SwapByteOrder                   matlab.ui.control.Button
        DetectorCoordinatePanel         matlab.ui.container.Panel
        DetectorCoordinateGrid          matlab.ui.container.GridLayout
        DetectorCoordinateUnit          matlab.ui.control.DropDown
        DetectorCoordinatePosition      matlab.ui.control.DropDown
        DetectorCoordinateSystem        matlab.ui.control.DropDown
        LiveUpdateImagesGrid            matlab.ui.container.GridLayout
        CalculationPolicy               matlab.ui.control.DropDown
        CalculationPolicyDropDownLabel  matlab.ui.control.Label
        CalculationPolicyIcon           matlab.ui.control.Image
        InfoTab                         matlab.ui.container.Tab
        InfoGrid                        matlab.ui.container.GridLayout
        ShowVariables                   matlab.ui.control.StateButton
        DatasetInfo                     matlab.ui.control.TextArea
        DatasetInfoTextAreaLabel        matlab.ui.control.Label
        MathTab                         matlab.ui.container.Tab
        MathGrid                        matlab.ui.container.GridLayout
        EvaluateGrid                    matlab.ui.container.GridLayout
        Evaluate                        matlab.ui.control.Button
        MathFormula                     matlab.ui.control.TextArea
        FormulaLabel                    matlab.ui.control.Label
        MathExampleGrid                 matlab.ui.container.GridLayout
        MathHelpIcon                    matlab.ui.control.Image
        MathExample                     matlab.ui.control.Label
        VariablesTab                    matlab.ui.container.Tab
        VariablesGrid                   matlab.ui.container.GridLayout
        VariablesTree                   matlab.ui.container.Tree
        VariablesTable                  matlab.ui.control.Table
        ImportPanel                     matlab.ui.container.Panel
        ImportGrid                      matlab.ui.container.GridLayout
        ImportButtonGrid                matlab.ui.container.GridLayout
        CancelImport                    matlab.ui.control.Button
        SwapDataset                     matlab.ui.control.CheckBox
        ImportData                      matlab.ui.control.Button
        ImportOptionsPanel              matlab.ui.container.Panel
        ImportOptionsGrid               matlab.ui.container.GridLayout
        ImportSummary                   matlab.ui.control.TextArea
        ImportSummaryLabel              matlab.ui.control.Label
        RealPartialImportGrid           matlab.ui.container.GridLayout
        RealPartialImportY              matlab.ui.control.Spinner
        INFrYl                          matlab.ui.control.Label
        RealPartialImportX              matlab.ui.control.Spinner
        INFrXl                          matlab.ui.control.Label
        RealPartialImportYStart         matlab.ui.control.Spinner
        ysub1Label_6                    matlab.ui.control.Label
        RealPartialImportXStart         matlab.ui.control.Spinner
        xsub1Label_6                    matlab.ui.control.Label
        RealPartialImportFramesDist     matlab.ui.control.Spinner
        SamplingIntervalLabel_2         matlab.ui.control.Label
        DiffractionPartialImportGrid    matlab.ui.container.GridLayout
        DiffractionPartialImportY       matlab.ui.control.Spinner
        YLabel_3                        matlab.ui.control.Label
        DiffractionPartialImportX       matlab.ui.control.Spinner
        XLabel_3                        matlab.ui.control.Label
        DiffractionPartialImportYStart  matlab.ui.control.Spinner
        ysub1Label_5                    matlab.ui.control.Label
        DiffractionPartialImportXStart  matlab.ui.control.Spinner
        xsub1Label_5                    matlab.ui.control.Label
        DiffractionPartialImportPixelsDist  matlab.ui.control.Spinner
        BinningDistanceLabel            matlab.ui.control.Label
        ImportPartialFrames             matlab.ui.control.CheckBox
        ImportPartialPixels             matlab.ui.control.CheckBox
        MemoryGrid                      matlab.ui.container.GridLayout
        GPU                             matlab.ui.control.DropDown
        MemoryType                      matlab.ui.control.DropDown
        ImportDatasetInfoPanel          matlab.ui.container.Panel
        ImportDatasetInfoGrid           matlab.ui.container.GridLayout
        ImportFileMetadata              matlab.ui.control.TextArea
        DatasetInfofromMetadataLabel    matlab.ui.control.Label
        ImportFileSizeGrid              matlab.ui.container.GridLayout
        ImportEstimatedFilesize         matlab.ui.control.Label
        ImportEstimatedFilesizeLabel    matlab.ui.control.Label
        ImportActualFilesize            matlab.ui.control.Label
        ImportActualFilesizeLabel       matlab.ui.control.Label
        ImportDimensionGrid             matlab.ui.container.GridLayout
        ImportFramesY                   matlab.ui.control.NumericEditField
        YLabel                          matlab.ui.control.Label
        ImportFramesX                   matlab.ui.control.NumericEditField
        XLabel                          matlab.ui.control.Label
        ImportFramesLabel               matlab.ui.control.Label
        ImportPixelsY                   matlab.ui.control.NumericEditField
        YLabel_2                        matlab.ui.control.Label
        ImportPixelsX                   matlab.ui.control.NumericEditField
        XLabel_2                        matlab.ui.control.Label
        ImportPixelsLabel               matlab.ui.control.Label
        ImportDatasetStructureGrid      matlab.ui.container.GridLayout
        ImportByteOrder                 matlab.ui.control.DropDown
        ByteOrderDropDownLabel          matlab.ui.control.Label
        ImportDataType                  matlab.ui.control.DropDown
        DataTypeLabel                   matlab.ui.control.Label
        FrameFooter                     matlab.ui.control.NumericEditField
        FrameFooterLabel                matlab.ui.control.Label
        FrameHeader                     matlab.ui.control.NumericEditField
        FrameHeaderLabel                matlab.ui.control.Label
        DataOffset                      matlab.ui.control.NumericEditField
        DataOffsetLabel                 matlab.ui.control.Label
        SubDataset                      matlab.ui.control.DropDown
        SubdatasetDropDownLabel         matlab.ui.control.Label
        FileTypeButtonGroup             matlab.ui.container.ButtonGroup
        Custom                          matlab.ui.control.ToggleButton
        HDF5                            matlab.ui.control.ToggleButton
        DM34                            matlab.ui.control.ToggleButton
        MRC                             matlab.ui.control.ToggleButton
        Medipix                         matlab.ui.control.ToggleButton
        EMPAD                           matlab.ui.control.ToggleButton
        ImportFileGrid                  matlab.ui.container.GridLayout
        ImportFilePath                  matlab.ui.control.EditField
        ImportFileSelect                matlab.ui.control.Button
        SavePanel                       matlab.ui.container.Panel
        SaveGrid                        matlab.ui.container.GridLayout
        SaveExportButtonGrid            matlab.ui.container.GridLayout
        SaveCloseButton                 matlab.ui.control.Button
        SaveExport                      matlab.ui.control.Button
        SaveTabGroup                    matlab.ui.container.TabGroup
        SaveImagesTab                   matlab.ui.container.Tab
        SaveImagesGrid                  matlab.ui.container.GridLayout
        SaveImageFormatGrid             matlab.ui.container.GridLayout
        SaveImagePNGGrid                matlab.ui.container.GridLayout
        SaveImageDPI                    matlab.ui.control.NumericEditField
        SaveImgAnnotDPILabel            matlab.ui.control.Label
        SaveImageAnnotations            matlab.ui.control.CheckBox
        SaveImagePNG                    matlab.ui.control.CheckBox
        SaveImageTIFF                   matlab.ui.control.CheckBox
        SaveImageListGrid               matlab.ui.container.GridLayout
        SaveImageList                   matlab.ui.control.ListBox
        SaveImageSelectAll              matlab.ui.control.CheckBox
        ImagestoSaveMultiselectwithCtrlShiftLabel  matlab.ui.control.Label
        SavePrefixAngleGrid             matlab.ui.container.GridLayout
        SavePrefixAngleOuter            matlab.ui.control.CheckBox
        SavePrefixAngleInner            matlab.ui.control.CheckBox
        SavePrefixAngleLabel            matlab.ui.control.Label
        SaveImagePrefixGrid             matlab.ui.container.GridLayout
        SaveImagePrefix                 matlab.ui.control.EditField
        FilenamePrefixLabel             matlab.ui.control.Label
        ExportDatasetTab                matlab.ui.container.Tab
        ExportGrid                      matlab.ui.container.GridLayout
        ExportPartialFrames             matlab.ui.control.CheckBox
        ExportNotes                     matlab.ui.control.TextArea
        SummaryLabel                    matlab.ui.control.Label
        RealPartialExportGrid           matlab.ui.container.GridLayout
        RealPartialExportFramesDist     matlab.ui.control.Spinner
        SamplingIntervalLabel           matlab.ui.control.Label
        RealPartialExportY              matlab.ui.control.Spinner
        ENFrYl                          matlab.ui.control.Label
        RealPartialExportX              matlab.ui.control.Spinner
        ENFrXl                          matlab.ui.control.Label
        RealPartialExportYStart         matlab.ui.control.Spinner
        ysub1Label_4                    matlab.ui.control.Label
        RealPartialExportXStart         matlab.ui.control.Spinner
        xsub1Label_4                    matlab.ui.control.Label
        DiffractionPartialExportGrid    matlab.ui.container.GridLayout
        DiffractionPartialExportY       matlab.ui.control.Spinner
        ENPxYl                          matlab.ui.control.Label
        DiffractionPartialExportX       matlab.ui.control.Spinner
        ENPxXl                          matlab.ui.control.Label
        DiffractionPartialExportYStart  matlab.ui.control.Spinner
        ysub1Label_3                    matlab.ui.control.Label
        DiffractionPartialExportXStart  matlab.ui.control.Spinner
        xsub1Label_3                    matlab.ui.control.Label
        DiffractionPartialExportPixelsDist  matlab.ui.control.Spinner
        BinningDistanceLabel_2          matlab.ui.control.Label
        ExportPartialPixels             matlab.ui.control.CheckBox
        ExportByteOrder                 matlab.ui.control.DropDown
        ExportDataType                  matlab.ui.control.DropDown
        ExportFileGrid                  matlab.ui.container.GridLayout
        ExportDimensionSuffix           matlab.ui.control.CheckBox
        ExportFilename                  matlab.ui.control.EditField
        FilenameLabel                   matlab.ui.control.Label
        SaveDirectoryGrid               matlab.ui.container.GridLayout
        SaveDirectoryPath               matlab.ui.control.EditField
        SaveDirectoryButton             matlab.ui.control.Button
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

    properties (Access = public)
        debug                                                           % Debug mode. false to disable; else enables timers/tracers
        data                                                            % Imported dataset, may be moved to GPU
        memfile                                                         % Memory map file of the imported dataset
        sys_constants                                                   % Constants for system info that set at self startup
        tmp_variables                                                   % Temporary global variables, e.g. for progress bar and import etc., should never be cleared
        dataset_parameters                                              % Parameters of the current imported dataset; should be constants (except for data type conversion)
        common_parameters                                               % Common parameters, should be cleared when a dataset is unloaded
        previous_values                                                 % Previous values, should be cleared when a dataset is unloaded
        figures                                                         % All figure windows excluding the Main UI
        image_axes                                                      % All image axes
        images                                                          % Arrays of raw data for the images/masks to be plotted/saved
        image_displays                                                  % Image objects with modified contrast for display, e.g. by ``self.image_displays.(id) = imagesc(...)``
        annotations                                                     % Image annotations on `axes` or `uiaxes`, excluding annotations on `figure` and `uifigure`
        masks                                                           % Real and Diffraction space masks applied to data
        ui_groups                                                       % Different groups of figures/axes/images; assigned just once at startup in create_other_windows()
        center = [0 0];                                                 % Central beam absolute pixel coordinates
        center_rel = [0 0];                                             % Relative position of center. [0 0] (when "Absolute" position) or center (when "Relative")
        diff_scale = 1;                                                 % Diffraction pixel scale. 1 (when in pixel) or mrad/px (when in mrad)
        real_scale = 1;                                                 % Real-space pixel scale. 1 (when in pixel) or nm/px (when in nm). Not implemented yet
        variable_nodes                                                  % uitree nodes to display variables for users
        byte_size = struct("uint8", 1, ...                              % size of each supported data type in bytes
                           "int8", 1, ...
                           "uint16", 2, ...
                           "int16", 2, ...
                           "single", 4, ...
                           "int32", 4, ...
                           "uint32", 4, ...
                           "double", 8, ...
                           "int64", 8, ...
                           "uint64", 8);
    end

    methods (Access = public)

        function enable_virtual_aperture_UI(self)
            % Function to update UI enable/disable states
            %
            % Parameters:
            %    self (Quant4D)
            %
            % Returns:
            %    None
        
            % Enable/Disable mirror UIs, except `self.VirtualApertureMirror`
            set(setdiff(self.VirtualApertureMirrorGrid.Children,self.VirtualApertureMirror), ...
                "Enable", switch_on_off(self, self.VirtualApertureMirror.Value))
        end

        function limit_virtual_aperture_UI(self)
            % Function to update UIs Limits/Labels for coordinate options
            %
            % Parameters:
            %    self (Quant4D)
            %
            % Returns:
            %    None
        
            % set virtual aperture step size to 1/4 diffraction scale (mrad/pixel)
            step_size = 0.25*self.diff_scale; 
            unit = self.DetectorCoordinateUnit.Value;
        
            % reflect the coordinate system choice in the UI elements
            if self.DetectorCoordinateSystem.Value == "Polar"
                x_limits = [0, min([self.center, self.dataset_parameters.n_pixels-self.center]*2^.5)*self.diff_scale];
                y_limits = [-1 1]*180;
                x_text = 'Distance';
                y_text = 'Rotation';
                y_unit = '°'; 
                y_step = 4;
            else
                x_limits = (self.TransBeamX.Limits-self.center_rel(1))*self.diff_scale;
                y_limits = (self.TransBeamY.Limits-self.center_rel(2))*self.diff_scale;
                x_text = 'X'; 
                y_text = 'Y';
                y_unit = unit;
                y_step = step_size;
            end
            
            % update limits for sliders and numeric spinners
            set([self.VirtualApertureX; ...
                 self.VirtualApertureXSpinner; ...
                 self.VirtualApertureY; ...
                 self.VirtualApertureYSpinner; ...
                 self.VirtualApertureRSpinner], ...
                {"Limits"}, ...
                {x_limits; ...
                 x_limits; ...
                 y_limits; ...
                 y_limits; ...
                 self.TransBeamR.Limits*self.diff_scale})
        
            % update labels
            set([self.VrApXLabel; ...
                 self.VrApYLabel; ...
                 self.VrApX_NFLabel; ...
                 self.VrApY_NFLabel; ...
                 self.VrApR_NFLabel], ...
                {'Text'}, ...
                {x_text; ...
                 y_text; ...
                 unit; ...
                 y_unit; ...
                 unit})
        
            % update step size for numeric spinner
            set([self.VirtualApertureXSpinner; ...
                 self.VirtualApertureYSpinner; ...
                 self.VirtualApertureRSpinner], ...
                {'Step'}, ...
                {step_size; ...
                 y_step; ...
                 step_size})
        end

        function draw_virtual_aperture_annotation(self)
            % Function to draw virtual aperture annotations
            %
            % Parameters:
            %    self (Quant4D)
            %
            % Returns:
            %    None
            
                % clear any previous virtual aperture annotations
                delete(findobj(self.image_axes.Diffraction, "Tag","VrApertAnnot"))
            
                % plot the apertures, and only allow the first one to be interactive
                self.annotations.VrAp = gobjects(self.VirtualApertureSymmetry.Value*(1+self.VirtualApertureMirror.Value), 1);
                for i = 1:numel(self.annotations.VrAp)
                    self.annotations.VrAp(i) = drawcircle(self.image_axes.Diffraction, ...
                                                         "Center", self.common_parameters.virtual_aperture_center, ...
                                                         "Radius", self.VirtualApertureR.Value, ...
                                                         "Color","r", ...
                                                         "FaceAlpha", 0, ...
                                                         "Deletable", 0, ...
                                                         "InteractionsAllowed", "none", ...
                                                         "Tag","VrApertAnnot");
                end
                
                % Make sure the draggable annotations are at the front
                bringToFront(self.annotations.VrAp(1));
            
                % set aperture annotation parameters
                set(self.annotations.VrAp(1), ...
                    "InteractionsAllowed", "all", ...
                    "DrawingArea", "unlimited")
                
                % add listeners to main virtual aperture annotation
                self.annotations.VrAp(1).UserData.Move = addlistener(self.annotations.VrAp(1), "ROIMoved", @self.move_virtual_aperture);
                addlistener(self.annotations.VrAp(1), "MovingROI", @self.move_virtual_aperture);
            
                % Mirror line/point annotations
                self.annotations.VrApMirL = drawline(self.image_axes.Diffraction, ...
                                                    "Position", [0 0; self.dataset_parameters.n_pixels], ...
                                                    "Color", [0 0.7 0], ...
                                                    "StripeColor", "k", ...
                                                    "LineWidth", 1.5, ...
                                                    "EdgeAlpha", 0.7, ...
                                                    "InteractionsAllowed", "none", ...
                                                    "Visible", self.VirtualApertureMirror.Value, ...
                                                    "Deletable", false, ...
                                                    "Tag","VrApertAnnot");
            
                self.annotations.VrApMirP = drawpoint(self.image_axes.Diffraction, ...
                                                     "Position", [min(self.dataset_parameters.n_pixels)/4 0] + self.center, ...
                                                     "Color", "g", ...
                                                     "MarkerSize", 8, ...
                                                     "Visible", self.VirtualApertureMirror.Value, ...
                                                     "Deletable", 0, ...
                                                     "Tag", "VrApertAnnot");
            
                % add listeners to the mirror line point
                self.annotations.VrApMirP.UserData.Move = addlistener(self.annotations.VrApMirP, "ROIMoved", @self.move_virtual_aperture);
                addlistener(self.annotations.VrApMirP, "MovingROI", @self.move_virtual_aperture);
            end

        function move_virtual_aperture(self, source, event)
            % Live update function for virtual aperture annotations
            %
            % Parameters:
            %    self (Quant4D)
            %    source (images.roi.Circle | images.roi.Point) : virtual aperture annotations
            %    event (event.EventData) : ROIMoved, MovingROI
            %
            % Returns:
            %    None
        
            % To determine real-time values
            transmitted_beam_center = self.center_rel;
            scale = self.diff_scale;
            num_pix = self.dataset_parameters.n_pixels;
            mirror_angle = self.VirtualApertureMirrorRotation.Value;
            radius = self.VirtualApertureR.Value;
            virtual_aperture_center = self.common_parameters.virtual_aperture_center;
            
            switch source
                case self.annotations.VrAp(1)
                    radius = source.Radius;
                    virtual_aperture_center = source.Center;
            
                case {self.VirtualApertureX self.VirtualApertureXSpinner self.VirtualApertureY self.VirtualApertureYSpinner}
                    % Potentially converting from polar/relative/mrad to Cartesian absolute pixel coordinates
                    x = self.VirtualApertureX.Value;
                    y = self.VirtualApertureY.Value;
            
                    if ismember(source, [self.VirtualApertureX self.VirtualApertureXSpinner])
                        x = event.Value;
                    else
                        y = event.Value;
                    end
            
                    if self.DetectorCoordinateSystem.Value == "Cartesian"
                        virtual_aperture_center = [x y]/scale + transmitted_beam_center;
                    else
                        [x,y] = pol2cart(deg2rad(y), x/scale);
                        virtual_aperture_center = self.center+[x y];
                    end
            
                case self.VirtualApertureR
                    radius = event.Value;
            
                case self.VirtualApertureRSpinner
                    radius = event.Value/scale;
            
                case self.VirtualApertureReset
                    radius = self.TransBeamR.Value;
                    virtual_aperture_center = transmitted_beam_center;
            
                case {self.VirtualApertureRotateCCW self.VirtualApertureRotateCW} % Rotation buttons
                    % Clockwise if odd numbers of "Reverse X"
                    % "Reverse Y" "Rotate Clockwise" are true
                    rot = self.VirtualApertureRotationStep.Value * (1-2*rem(self.ReverseDiffractionX.Value+self.ReverseDiffractionY.Value+(source == self.VirtualApertureRotateCW), 2));
                    virtual_aperture_center = (virtual_aperture_center-transmitted_beam_center)*rotation_matrix(self, rot)+transmitted_beam_center;
            
                case {self.VirtualApertureMirrorRotation self.VirtualApertureMirrorRotationSpinner}
                    % update the mirror line position
                    mirror_angle = event.Value;
            
                case self.annotations.VrApMirP
                    mirror_position = source.Position - transmitted_beam_center;
                    mirror_angle = atan2d(mirror_position(2), mirror_position(1));
            end
            
            % Restrict aperture location/size
            radius = min(radius, self.common_parameters.max_radius);
            virtual_aperture_center(virtual_aperture_center > num_pix) = num_pix(virtual_aperture_center > num_pix);
            virtual_aperture_center(virtual_aperture_center < 1) = 1;
            self.common_parameters.virtual_aperture_center = virtual_aperture_center;
            
            % Update GUI with Limits check
            xy_limits = [self.VirtualApertureX.Limits; self.VirtualApertureY.Limits]';
            
            if self.DetectorCoordinateSystem.Value == "Cartesian"
                xyui = (virtual_aperture_center - transmitted_beam_center)*scale;
            else % "Polar"
                xyui = virtual_aperture_center - transmitted_beam_center;
                [theta, rho] = cart2pol(xyui(1), xyui(2));
                xyui = [rho*scale, rad2deg(theta)];
            end
            
            % Limit check
            xyui = clip(xyui, xy_limits(1,:), xy_limits(2,:));
            
            set_external_source(self, event, ...
                [self.VirtualApertureR; ...
                self.VirtualApertureRSpinner; ...
                self.VirtualApertureX; ...
                self.VirtualApertureXSpinner; ...
                self.VirtualApertureY; ...
                self.VirtualApertureYSpinner], ...
                {"Value"}, ...
                {radius; ...
                min(radius*scale, self.common_parameters.max_radius*scale); ...
                xyui(1); ...
                xyui(1); ...
                xyui(2); ...
                xyui(2)})
            
            set_external_source(self, event, ...
                [self.VirtualApertureMirrorRotation; ...
                self.VirtualApertureMirrorRotationSpinner], ...
                "Value", mirror_angle)
            
            % Early return if only updating for coordinate options
            if source == self.DetectorCoordinateSystem
                return;
            end
            
            % Update ROIs
            [theta, rho] = cart2pol(virtual_aperture_center(1) - transmitted_beam_center(1), ...
                virtual_aperture_center(2) - transmitted_beam_center(2));
            
            angles = rad2deg(theta) + (0 : 360/self.VirtualApertureSymmetry.Value : 360*(1-1/self.VirtualApertureSymmetry.Value))';
            virtual_aperture_center_new = rho*[cosd(angles) sind(angles)];
            
            % If mirrored, double the amount of center positions
            if self.VirtualApertureMirror.Value
                R_mirror = rotation_matrix(self, 90 - mirror_angle);
                virtual_aperture_center_new = [virtual_aperture_center_new; virtual_aperture_center_new*R_mirror.*[-1 1]*(R_mirror')];
            end
            
            % Relative -> Absolute
            virtual_aperture_center_new = virtual_aperture_center_new + transmitted_beam_center;
            set(self.annotations.VrAp, ...
                {"Center"}, num2cell(virtual_aperture_center_new,2), ...
                'Radius', radius)
            
            % Update mirror line ROIs, whether visible or not, deal
            % with any Infs by clipping to [-1e9, 1e9]
            pos = [[1;self.dataset_parameters.n_pixels(1)], tand(mirror_angle)*([1;self.dataset_parameters.n_pixels(1)] - transmitted_beam_center(1)) + transmitted_beam_center(2)];
            pos = clip(pos,-1e9,1e9);
            self.annotations.VrApMirL.Position = pos;
            
            [x,y] = pol2cart(deg2rad(mirror_angle), sqrt(sum((self.annotations.VrApMirP.Position - transmitted_beam_center).^2)));
            
            % Restrict point within plot
            xy_point = [x y] + transmitted_beam_center;
            xy_point(xy_point > num_pix) = num_pix(xy_point > num_pix);
            xy_point(xy_point < 1) = 1;
            set_external_source(self, event, self.annotations.VrApMirP, "Position", xy_point)
            
            % Whether to update images
            if to_update_image(self, event)
                % Generate mask
                mask_vr = false(self.dataset_parameters.n_pixels);
                for i = 1:numel(self.annotations.VrAp)
                    mask_vr = mask_vr | createMask(self.annotations.VrAp(i), self.image_displays.Diffraction)';
                end
            
                % Invert mask?
                if self.VirtualApertureInvert.Value
                    mask_vr = 1 - mask_vr;
                end
            
                self.images.DiffractionMask = mask_vr;
                self.images.Real = gather(reshape(reshape(mask_vr,1,[])*self.data, self.dataset_parameters.n_frames));
                plot_all_patterns(self, event)
            end
        end

        function auto_align(self)
            % Auto-align transmitted beam
            %
            % Parameters:
            %    self (Quant4D)
            %
            % Returns:
            %    None

            % display a progress dialog
            self.tmp_variables.progress_dialog = progress_dialog(self, 'Finding transmitted beam ...', "Auto Alignment");

            % Align transmitted beam by trying to find the transmitted
            % disk in the diffraction pattern (self.images.Diffraction),
            % apply slight Gaussian blur of 5 pixels to help the fit if
            % necessary
            try
                warning("off");
                [trans_beam_center, trans_beam_radius, ~] = imfindcircles(self.images.Diffraction*(-1)^self.DispColorMapInvert.Value, [1 round(max(self.dataset_parameters.n_pixels)/2)]);
                if isempty(trans_beam_center)
                    [trans_beam_center, trans_beam_radius, ~] = imfindcircles(imgaussfilt(self.images.Diffraction*(-1)^self.DispColorMapInvert.Value,5), [1 round(max(self.dataset_parameters.n_pixels)/2)]);
                end
                warning("on");
            catch
                trans_beam_center = [];
                trans_beam_radius = [];
            end
            trans_beam_center = fliplr(trans_beam_center);

            % Close the progress bar
            delete(self.tmp_variables.progress_dialog);

            % Store old transmitted beam values
            transBeam_old = [self.center self.TransBeamR.Value];

            % Find circle closest to the center of the diffraction
            % pattern, plot for user confirmation
            if isempty(trans_beam_center)
                notification_dialog(self, ...
                    "warn", ...
                    "No transmitted beam detected. Please align the transmitted beam manually.", ...
                    "Auto-align Failed");
                selection = "No. Revert";
            else
                % Assign radius and center value(s) found above using
                % imfindcircles based on whichever is found to be
                % closest to the diffraction pattern center
                % `self.common_parameters.diffraction_center`
                [~,im] = min(sqrt(sum((trans_beam_center-self.common_parameters.diffraction_center).^2,2)));
                self.TransBeamX.Value = trans_beam_center(im,1);
                self.TransBeamY.Value = trans_beam_center(im,2);
                self.TransBeamR.Value = trans_beam_radius(im);

                % To update annotation/panel values
                transmitted_beam_callbacks(self,struct("Source", "", "EventName", ""));

                % don't ask the user for feedback on the initial run of
                % autoAlign(self)
                if self.common_parameters.transmitted_beam_init
                    selection = notification_dialog(self,'quest', "Is the auto-alignment correct?",'Auto-align',["Yes", "No. Revert"]);
                else
                    selection = "Yes";
                end
            end

            % Revert alignment if not correctly detected
            if selection == "No. Revert"
                self.TransBeamX.Value = transBeam_old(1);
                self.TransBeamY.Value = transBeam_old(2);
                self.TransBeamR.Value = transBeam_old(3);
            end
        end

        function cross_align(self)
            % Function to align the transmitted beam to the intersection of two lines
            %
            % Parameters:
            %    self (Quant4D)
            %
            % Returns:
            %    None

            % draw two line annotations
            self.annotations.line1 = drawline("Parent", self.image_axes.Diffraction, ...
                                             "Position", self.dataset_parameters.n_pixels.*[1 1;3 3]/4, ...
                                             "Color", "r", ...
                                             "Deletable",false);

            self.annotations.line2 = drawline("Parent", self.image_axes.Diffraction, ...
                                             "Position", self.dataset_parameters.n_pixels.*[1 3;3 1]/4, ...
                                             "Color", "r", ...
                                             "Deletable",false);

            % add listeners to the annotations
            addlistener(self.annotations.line1, "ROIMoved", @find_intersection);
            addlistener(self.annotations.line1, "MovingROI", @find_intersection);
            addlistener(self.annotations.line2, "ROIMoved", @find_intersection);
            addlistener(self.annotations.line2, "MovingROI", @find_intersection);

            % initialize transmitted beam to the intersection point of the two
            % line annotations
            find_intersection()

            % Wait for the user to confirm before finishing
            h = helpdlg('Push OK when finished');
            uiwait(h);

            % clear line annotations
            delete(self.annotations.line1)
            delete(self.annotations.line2)

            function find_intersection(~,~)
                % Internal function to find the intersection point of two lines
                % and set the transmitted beam location accordingly.
                %
                % Parameters:
                %    source (images.roi.Line): line annotation (unused)
                %    event: even Class (unused)
                %
                % Returns:
                %    None

                % get point-pairs
                x1 = self.annotations.line1.Position(1,1);
                x2 = self.annotations.line1.Position(2,1);
                x3 = self.annotations.line2.Position(1,1);
                x4 = self.annotations.line2.Position(2,1);

                y1 = self.annotations.line1.Position(1,2);
                y2 = self.annotations.line1.Position(2,2);
                y3 = self.annotations.line2.Position(1,2);
                y4 = self.annotations.line2.Position(2,2);

                % get intersection from 4 point-pairs
                self.center = [x1*y2-x2*y1, x3*y4-x4*y3] / ...
                                [   y2-y1,  y4-y3;
                                -(x2-x1),-(x4-x3)];

                % send values to transmitted beam UI elements
                self.TransBeamX.Value = self.center(1);
                self.TransBeamXSpinner.Value = self.center(1);
                self.TransBeamY.Value = self.center(2);
                self.TransBeamYSpinner.Value = self.center(2);

                % update global center
                self.annotations.TransBeam.Center = self.center;

            end
        end

        function move_transmitted_beam(self, source, event)
            % Function to sync UIs/ROIs depending on the central beam location
            %
            % Parameters:
            %    self (Quant4D)
            %    source (images.roi.Circle) : transmitted beam annotation
            %    event (event.EventData) : ROIMoved, MovingROI
            %
            % Returns:
            %    None

            trans_beam_center = [self.TransBeamX.Value, self.TransBeamY.Value];
            radius = self.TransBeamR.Value;
            alpha = self.Alpha.Value;
            mrad_per_px = alpha/radius;
            n_pixels = self.dataset_parameters.n_pixels;

            if isempty(findobj(self.image_axes.Diffraction, "Tag","TransBeamAnnot"))
                self.annotations.TransBeam = []; % If ROI is not plotted
            else
                switch event.Source
                    case {self.TransBeamX, self.TransBeamXSpinner}
                        % Force X >= 1
                        trans_beam_center(1) = max(1, event.Value);

                    case {self.TransBeamY, self.TransBeamYSpinner}
                        % Force Y >= 1
                        trans_beam_center(2) = max(1, event.Value);

                    case {self.TransBeamR, self.TransBeamRSpinner}
                        % Radius
                        radius = event.Value;

                    case self.Alpha
                        % Calculate the diffraction scale
                        alpha = event.Value;
                        mrad_per_px = alpha/radius;

                    case self.mradPx
                        % Manually set the diffraction scale
                        mrad_per_px = event.Value;
                        alpha = mrad_per_px*radius;

                    case self.annotations.TransBeam
                        % ROI
                        trans_beam_center = source.Center;
                        radius = source.Radius;
                end
            end

            % Restrict transmitted beam location/size
            %center(center > n_pixels) = n_pixels(center > n_pixels);
            %center(center < 1) = 1;
            trans_beam_center = clip(trans_beam_center, 1, n_pixels);
            self.center = trans_beam_center;

            % Find the max allowed radius to the furthest corner from `center`
            self.common_parameters.max_radius = ceil(sqrt(sum((abs(self.common_parameters.diffraction_center-trans_beam_center) + self.common_parameters.diffraction_center -1).^2)));

            % set the annular integration step size based on max radius
            % (convert to mrad for the UI); default to stepping each
            % pixel, with a max of 250 steps, otherwise pre-calculation
            % of the annular images can get quite slow
            if event.Source ~= self.AnnularStep
                self.AnnularStep.Value = self.mradPx.Value * max(1, self.common_parameters.max_radius/250);
            end

            % make sure r is not larger than the max radius; cannot be
            % 0 so clip to eps
            radius = clip(radius, eps, self.common_parameters.max_radius);

            % Update UI limits
            set([self.TransBeamR, ...
                self.TransBeamRSpinner], ...
                "Limits", ...
                [eps(), self.common_parameters.max_radius])

            set([self.InnerAnnularRadius, ...
                self.OuterAnnularRadius, ...
                self.VirtualApertureR, ...
                self.BandpassFilterLow, ...
                self.BandpassFilterHigh, ...
                self.BandpassFilter], ...
                "Limits", ...
                [0, self.common_parameters.max_radius])

            % Update UI values
            set_external_source(self, ...
                event, ...
                [self.TransBeamR; ...
                self.TransBeamX; ...
                self.TransBeamY; ...
                self.TransBeamRSpinner; ...
                self.TransBeamXSpinner; ...
                self.TransBeamYSpinner; ...
                self.BandpassFilterLow; ...
                self.BandpassFilterHigh; ...
                self.BandpassFilter; ...
                self.Alpha; ...
                self.mradPx], ...
                {"Value"}, ...
                {radius; ...
                trans_beam_center(1); ...
                trans_beam_center(2); ...
                radius; ...
                trans_beam_center(1); ...
                trans_beam_center(2); ...
                0;...
                self.common_parameters.max_radius; ...
                [0, self.common_parameters.max_radius];...
                alpha; ...
                mrad_per_px})

            % Update ROI
            set(self.annotations.TransBeam,"Center",trans_beam_center,'Radius',radius)

            % Update global coordinate properties
            detector_coordinates_callbacks(self, event)

        end

        function notes = get_import_info(self)
            % Function to update current dataset import parameters
            %
            % Parameters:
            %   self (Quant4D)
            %
            % Returns:
            %    notes (str) : collection of import parameters for display to the user

            params = self.dataset_parameters;
            previous_params = self.tmp_variables.prev_D;

            % create a notes string with important info
            notes = "File: " + replace(params.file_path, "\", "\\");

            % include sub-image if applicable
            if ~isempty(params.subimage)
                notes = notes + "\nSub-dataset: " + params.subimage;
            end

            notes = notes ...
                    + "\n\n" ...
                    + "# Current Data Info #\n" ...
                    + "Byte Order: " + self.sys_constants.endian_text.(params.byte_orer) + "\n"...
                    + "Data Type: " + params.data_type + "\n"...
                    + "Byte Size: " + self.byte_size.(params.data_type) + " bytes\n" ...
                    + sprintf("Diffraction size (X×Y): %d×%d\n",params.n_pixels) ...
                    + sprintf("Real-spaces size (X×Y): %d×%d\n\n",params.n_frames) ...
                    + "# Data Structure in File #\n" ...
                    + "Data Offset: " + previous_params.offset + " bytes\n" ...
                    + "Frame Header: " + previous_params.frame_header + "bytes\n" ...
                    + "Frame Footer: " + previous_params.frame_footer + " bytes\n" ...
                    + "Byte Order: " + self.sys_constants.endian_text.(previous_params.byte_orer) + "\n"...
                    + "Data Type: "+ previous_params.data_type + "\n"...
                    + "Byte Size: " + self.byte_size.(previous_params.data_type) + " bytes" ...
                    + "\n\n" ...
                    + "# File Meta Info Notes #\n" ...
                    + strjoin(previous_params.file_metadata,'\n') ...
                    + "\n\n" ...
                    + "# Import Option Notes #\n" ...
                    + strjoin(previous_params.import_options,'\n');

            notes = sprintf(notes);
        end

        function err = export_data(self, event)
            % Function to export data as `.h5` or `.raw`
            %
            % Parameters:
            %    self (Quant4D)
            %    event (event.EventData)
            %
            % Returns:
            %    err (int | bool) : error code, default: false, -1 if an error has occurred

            err = false;

            % export full file name with directory path
            self.tmp_variables.efile = fullfile(self.SaveDirectoryPath.Value, self.ExportFilename.Value+"."+self.ExportDataType.Value);

            % notify user and exit if the file already exists
            if isfile(self.tmp_variables.efile)
                notification_dialog(self, "warn", "File: '"+self.tmp_variables.efile+"' already exists!",'File Exists!');
                return
            end

            % Update export range
            [pixels_dist, pixels_start, n_pixels, pixels_end, frames_dist, frames_start, n_frames] = update_export_range(self, event);

            % Local variables
            data_type = self.dataset_parameters.data_type;
            frame_size = n_pixels(1) * n_pixels(2) * self.dataset_parameters.byte_size;
            byte_order = self.ExportByteOrder.Value;

            % Progress window with per-second-updating `timer`
            [self.tmp_variables.progress_dialog, self.tmp_variables.tmr] = import_export_progress(self, "Export", n_frames(1)*n_frames(2), frame_size);

            % Make dataset 4D
            self.data = reshape(self.data, [self.dataset_parameters.n_pixels, self.dataset_parameters.n_frames]);

            if self.ExportDataType.Value == "h5"
                % Sort out the h5 data type string; e.g. H5T_IEEE_F32LE, H5T_IEEE_F32BE, H5T_IEEE_F64LE, H5T_IEEE_F64BE
                h5dt = "H5T_IEEE_F" + self.byte_size.(data_type)*8 + upper(byte_order) + "E";

                % C-like array indices for H5 low-level APIs
                file_id = H5F.create(self.tmp_variables.efile);
                type_id = H5T.copy(h5dt);
                file_space_id = H5S.create_simple(4, [n_frames(2), n_frames(1), n_pixels(2), n_pixels(1)], []);
                memory_space_id = H5S.create_simple(2, [n_pixels(2), n_pixels(1)], []);
                property_list = H5P.create('H5P_DATASET_CREATE');
                H5P.set_chunk(property_list, [1, 1, n_pixels(2), n_pixels(1)]);
                dataset_id = H5D.create(file_id, '/STEM4D', type_id, file_space_id, property_list);

                % Whole data in one go
                %         H5D.write(dset_id,'H5ML_DEFAULT','H5S_ALL','H5S_ALL','H5P_DEFAULT', ...
                %           data(pixels_start(1):pixels_end(1), pixels_start(2):pixels_end(2), frames_start(1):frames_end(1), frames_start(2):frames_end(2)));

                % One frame at a time
                for frame_y = 0 : n_frames(2) - 1
                    for frame_x = 0 : n_frames(1) - 1
                        % Break when progress windows closed
                        if ~isvalid(self.tmp_variables.progress_dialog)
                            err = -1;
                            break;
                        end

                        % Update processed Frame Number for progress update
                        self.tmp_variables.frame_number(1) = frame_y*n_frames(1) + frame_x + 1;
                        H5S.select_hyperslab(file_space_id, 'H5S_SELECT_SET', [frame_y, frame_x, 0, 0], [], [], [1, 1, n_pixels(2), n_pixels(1)]);

                        % Selected frame
                        frame = gather(self.data(pixels_start(1):pixels_end(1), ...
                            pixels_start(2):pixels_end(2), ...
                            frames_start(1)+frame_x*frames_dist, ...
                            frames_start(2)+frame_y*frames_dist));

                        % Pixel Binning
                        if pixels_dist > 1
                            frame = squeeze(sum(reshape(frame, [pixels_dist, n_pixels(1), pixels_dist, n_pixels(2)]), [1 3]),'omitnan');
                        end

                        H5D.write(dataset_id, 'H5ML_DEFAULT', memory_space_id, file_space_id, 'H5P_DEFAULT', frame);
                    end

                    if err == -1
                        break;
                    end
                end

                % Close created handles
                H5D.close(dataset_id);
                H5S.close(memory_space_id);
                H5S.close(file_space_id);
                H5T.close(type_id);
                H5P.close(property_list);
                H5F.close(file_id);

            elseif self.ExportDataType.Value == "raw"
                file_id = fopen(self.tmp_variables.efile,"w");
                % One frame at a time
                for frame_y = 0 : n_frames(2)-1
                    for frame_x = 0 : n_frames(1)-1
                        % Break when progress windows closed
                        if ~isvalid(self.tmp_variables.progress_dialog)
                            err = -1;
                            break;
                        end

                        % Update processed Frame # for progress update
                        self.tmp_variables.frame_number(1) = frame_y*n_frames(1) + frame_x + 1;

                        % Selected frame
                        frame = gather(self.data(pixels_start(1):pixels_end(1), pixels_start(2):pixels_end(2), frames_start(1)+frame_x*frames_dist, frames_start(2)+frame_y*frames_dist));

                        % Pixel binning
                        if pixels_dist > 1
                            frame = squeeze(sum(reshape(frame, [pixels_dist, n_pixels(1), pixels_dist, n_pixels(2)]), [1 3]),'omitnan');
                        end

                        fwrite(file_id, frame, data_type, byte_order);
                    end
                    if err == -1
                        break;
                    end
                end

                fclose(file_id);
            end

            % Close progress window
            delete(self.tmp_variables.progress_dialog);

            % Make dataset 2D again
            self.data = reshape(self.data, prod(self.dataset_parameters.n_pixels), []);

            if err
                self.tmp_variables.progress_dialog = progress_dialog(self, "Deleting the canceled export file ...", "Export Canceled");

                % Delete created file, if export canceled
                delete(self.tmp_variables.efile);
                delete(self.tmp_variables.progress_dialog)
            else
                notification_dialog(self, "help", "Export to '"+self.tmp_variables.efile+"' finished!",'Export Finished!');
            end

            enable_windows(self, true)
        end

        function [pixels_dist, pixels_start, n_pixels, pixels_end, frames_dist, frames_start, n_frames] = update_export_range(self, event)
            % Save images based on the user selections on the Save/Export UI
            %
            % Parameters:
            %    self (Quant4D)
            %    event (event.EventData)
            %
            % Returns:
            %    pixels_dist (int) : binning distance in diffraction space
            %    pixels_start ([int int]) : starting pixel index in diffraction space (default: 1, unless cropping)
            %    n_pixels ([int int]) : number of pixels to be exported in diffraction space
            %    pixels_end ([int int]) :final pixel index in diffraction space (default: n_pixels, unless cropping)
            %    frames_dist (int) : sub-sampling distance in real space
            %    frames_start ([int int]) : starting frame index in real space (default: 1, unless sub-sampling)
            %    n_frames ([int int]) : number of frames to be exported in real space

            % initialize parameters
            diffraction_event = event;
            real_event = event;

            % Update Diffraction and Real-space export ranges; use dummy event if source is not a range UI
            if ~contains(event.Source.Tag, "Diffraction")
                diffraction_event = struct("Source", self.DiffractionPartialExportPixelsDist, ...
                    "Value", self.DiffractionPartialExportPixelsDist.Value);
            end

            if ~contains(event.Source.Tag, "Real")
                real_event = struct("Source", self.RealPartialExportFramesDist, ...
                    "Value", self.RealPartialExportFramesDist.Value);
            end

            %notes, binning, xy_start, n_points, xy_end
            [diffraction_note, pixels_dist, pixels_start, n_pixels, pixels_end] = range_import_export(self, diffraction_event);
            [real_note, frames_dist, frames_start, n_frames,  ~] = range_import_export(self, real_event);

            % Add dimension suffix and Remove old suffix
            self.ExportFilename.Value = regexprep(self.ExportFilename.Value, '_\d*x\d*x\d*x\d*$', "");
            if self.ExportDimensionSuffix.Value
                self.ExportFilename.Value = sprintf('%s_%dx%dx%dx%d', self.ExportFilename.Value, n_pixels, n_frames);
            end

            % Export summary notes
            filenote = sprintf("Directory: '%s'\nFilename: '%s.%s'", self.SaveDirectoryPath.Value, self.ExportFilename.Value, self.ExportDataType.Value);

            if self.ExportDataType.Value == "h5"
                filenote = filenote + sprintf("\nDataset: '/STEM4D'");
            end

            notes = diffraction_note + real_note ...
                + "\nData Type: " + self.dataset_parameters.data_type + " (was " + self.tmp_variables.prev_D.data_type + " in original file)" ...
                + "\nByte Order: " + self.sys_constants.endian_text.(self.ExportByteOrder.Value) + " (was " + self.sys_constants.endian_text.(self.tmp_variables.prev_D.byte_orer) + " in original file)" ...
                + "\nSystem Byte Order: " + self.sys_constants.endian_text.(self.sys_constants.system_endianness) ...
                + sprintf('\nEstimated file size: %.3f GiB', prod([n_pixels n_frames])*self.dataset_parameters.byte_size/1024^3) ...
                + sprintf('\nAvailable space: %.3f GiB', java.io.File(self.SaveDirectoryPath.Value).getUsableSpace/1024^3);

            self.ExportNotes.Value = filenote+sprintf("\n\n"+notes);
        end

        function move_export_annotation(self, ~, event)
            % Update Export Data boundaries as user change the Export Data Annotations
            %
            % Parameters:
            %    self (Quant4D)
            %    source (images.roi.Rectangle) : real-space export annotations, ignored
            %    event (event.EventData)
            %
            % Returns:
            %    None

            debug_time = tic;
            export_callbacks(self, event)
            debug_toc(self, event, "", debug_time)
        end

        function update_prefix(self, event)
            % Update image name prefix on the Save/Export UI
            %
            % Parameters:
            %    self (Quant4D)
            %    event (event.EventData) 
            %
            % Returns:
            %    None

            if is_static_event(self, event)
                % If not in any annular mode, disable the inner/outer radii prefix
                set([self.SavePrefixAngleInner; ...
                    self.SavePrefixAngleOuter], ...
                    "Enable", ismember(self.Mode.Value,["Annular" "CoM" "DPC"]))

                if ~self.SavePrefixAngleInner.Enable
                    set([self.SavePrefixAngleInner self.SavePrefixAngleOuter], "Value",0);
                end

                % Include inner and outer annular radii
                ang = "";
                inner_radius = "";
                outer_radius = "";
                if self.SavePrefixAngleInner.Value
                    inner_radius = "" + round(self.InnerAnnularRadiusSpinner.Value,2);
                end

                if self.SavePrefixAngleOuter.Value
                    outer_radius = ""+round(self.OuterAnnularRadiusSpinner.Value,2);
                end

                if all([inner_radius outer_radius] ~= "")
                    ang = "-";
                end

                ang = inner_radius + ang + outer_radius;

                if ang ~= ""
                    ang = ang + self.DetectorCoordinateUnit.Value + "_";
                end

                self.SaveImageList.Items = self.SaveImagePrefix.Value + ang + self.SaveImageList.ItemsData;
                if self.Mode.Value == "DPC"
                    self.SaveImageList.Items = replace(self.SaveImageList.Items, "CoM", "DPC");
                end
            end
        end

        function save_images(self)
            % Save images based on the user selections on the Save/Export UI
            %
            % Parameters:
            %    self (Quant4D)
            %
            % Returns:
            %    None

            % Give the user a progress bar in case it takes some time to save
            self.tmp_variables.progress_dialog = progress_dialog(self, 'Saving image(s) ...', "Image Saving");

            % Save as 32-bit unscaled, uncompressed Tiff images
            tagstruct = struct('PlanarConfiguration',Tiff.PlanarConfiguration.Chunky,'Compression',Tiff.Compression.None, ...
                'SampleFormat',Tiff.SampleFormat.IEEEFP,'Photometric',Tiff.Photometric.MinIsBlack,'BitsPerSample',32);

            for id = reshape(string(self.SaveImageList.Value),1,[])
                imgfile = fullfile(self.SaveDirectoryPath.Value, self.SaveImageList.Items{self.SaveImageList.ItemsData == id});

                if self.SaveImagePNG.Value
                    if self.SaveImageAnnotations.Value
                        print(self.figures.(id), imgfile, '-dpng', "-r"+num2str(self.SaveImageDPI.Value))
                    else
                        imgd = self.image_displays.(id);
                        imwrite(ind2rgb(round(255*imgd.CData)+1,self.image_axes.(id).Colormap).*imgd.AlphaData, [imgfile '.png'])
                    end
                end

                if self.SaveImageTIFF.Value
                    if id == "DiffractionMask" && self.Mode.Value == "DPC"
                        % Save all mask segments into a TIFF stack
                        for j = 1:self.NRung.Value
                            for i = 1:self.NSeg.Value
                                im = uint8(reshape(self.masks.Seg(self.NSeg.Value*(j-1)+i, :), self.dataset_parameters.n_pixels))';
                                imwrite(im, [imgfile '.tif'], 'WriteMode','append');
                            end
                        end
                    elseif id == "DiffractionMask" && self.Mode.Value == "CoM"
                        im = uint8(self.masks.annular)';
                        imwrite(im, [imgfile '.tif']);
                    else
                        % Other images (and "DiffractionMask" from `self.images.DiffractionMask` for other Detector Modes)
                        t = Tiff([imgfile '.tif'], "w");
                        im = self.images.(id)';
                        [tagstruct.ImageLength, tagstruct.ImageWidth] = size(im);
                        tagstruct.SamplesPerPixel = size(im,3);
                        t.setTag(tagstruct);
                        t.write(single(im));
                        t.close();
                    end
                end
            end

            delete(self.tmp_variables.progress_dialog);
        end

        function gpu_note = check_GPU_memory(self, n_pixels, n_frames)
            % Check the amount of GPU memory on the available GPU(s),
            % compare with the estimated memory from `check_memory()` and
            % warn if incompatible.
            %
            % Parameters:
            %    self (Quant4D)
            %    n_pixels ([int int]) : number of pixels in Diffraction space
            %    n_frames ([int int]) : number of probe positions in Real space
            %
            % Returns:
            %    gpu_note (str) : report on memory usage for the user
        
            igpu = self.GPU.Value;
            if ~igpu
                gpu_note = "GPU disabled.";
            elseif prod([n_pixels n_frames]) > intmax("int32")
                gpu_note = "GPU disabled, because dataset has more elements than MATLAB CUDA's maximum (2^31-1).";
                self.GPU.Value = 0;
            else
                tgpu = sprintf('GPU %d. %s %.1f GiB', igpu, self.sys_constants.gpu(igpu).name, self.sys_constants.gpu(igpu).memory/1024^3);
                try
                    if ~parallel.gpu.GPUDevice.getDevice(igpu).DeviceSelected
                        gpuDevice(igpu);
                    end
            
                    available_memory = parallel.gpu.GPUDevice.getDevice(igpu).AvailableMemory;
            
                    % If GPU is already in use, taking the current data size into account
                    if isfield(self.dataset_parameters, "GPU") && self.dataset_parameters.gpu == self.GPU.Value
                        try
                            available_memory = available_memory + self.dataset_parameters.estimated_memory;
                        catch
                        end
                    end
            
                    amem_t = sprintf('%.3f GiB', available_memory/1024^3);
            
                    warning_text = [];
            
                    if self.tmp_variables.estimated_memory > available_memory - 128*1024^2 % Has 128 MiB extra?
                        gpu_note = tgpu+" does NOT have enough free memory ("+amem_t+"). 128 MiB extra free memory required.";
                        warning_text = 'GPU Not Enough Free Memory!';
                        self.GPU.Value = 0;
            
                    elseif self.tmp_variables.estimated_memory > available_memory - 512*1024^2 % Has 512 MiB extra?
                        gpu_note = tgpu+" has LIMITED free memory ("+amem_t+") and may cause errors.";
                        warning_text = 'GPU Limited Free Memory!';
            
                    else
                        gpu_note = tgpu+" has enough free memory ("+amem_t+") for the selected dataset.";
            
                    end
            
                    % Notify warnings if any
                    if ~isempty(warning_text)
                        notification_dialog(self, "warn", gpu_note, warning_text);
                    end
            
                catch ME
                    gpu_note = sprintf('Failed to select %s!\n%s\n%s\n%s',tgpu,ME.identifier,ME.message,ME.Correction);
                    notification_dialog(self, "error", gpu_note, 'Error Selecting GPU!');
                    self.GPU.Value = 0;
                end
            end
        end

        function memory_note = check_memory(self, event, n_pixels, n_frames, bytesize)
            % Check the amount of system memory available, estimate the
            % required memory, compare and warn if incompatible. 
            %
            % Parameters:
            %    self (Quant4D)
            %    n_pixels ([int int]): number of pixels in Diffraction space
            %    n_frames ([int int]): number of probe positions in Real space
            %    bytesize (int): size of the data type in bytes
            %
            % Returns:
            %    memory_note (str) : report on memory usage for the user

            % Display estimated size in green if matches actual size, brown if smaller, red if larger
            if self.tmp_variables.EstSize == self.tmp_variables.FileSize
                self.ImportEstimatedFilesize.FontColor = [0 0.5 0];
            elseif self.tmp_variables.EstSize < self.tmp_variables.FileSize
                self.ImportEstimatedFilesize.FontColor = [0.5 0.5 0];
            else
                self.ImportEstimatedFilesize.FontColor = "r";
            end
            
            % Estimate the amount of memory needed to hold the largest arrays in memory
            % Estimate of the distance to the far corner of the diffraction pattern
            est_mem = prod([n_pixels n_frames]) ...                                   % self.data
                + prod(n_frames)*size(0:0.5:floor(sqrt(sum((n_pixels/2).^2))),2) ...  % self.images.annular_images
                + prod(n_frames)*10 + prod(n_pixels)*2  ...                           % self.images
                + prod(n_pixels)*10;                                                  % self.masks
            
            self.tmp_variables.estimated_memory = est_mem*bytesize;
            
            % check if there is an appropriate GPU to use
            if event.Source ~= self.GPU
                if any([self.sys_constants.gpu.memory]>=self.tmp_variables.estimated_memory)
                    [~,gpu_index] = max([self.sys_constants.gpu.memory]);
                    self.GPU.Value = gpu_index;
                else
                    self.GPU.Value = 0;
                end
            end
            
            memory_note = sprintf("Estimated memory usage: %.3f GiB.",self.tmp_variables.estimated_memory/1024^3);
            if self.tmp_variables.estimated_memory > self.sys_constants.total_memory
                msg = sprintf("WARNING: Size of dataset is larger than the system memory!");
                notification_dialog(self, "error", msg, 'Size Exceeds System Memory!');
                memory_note = memory_note+"\n"+msg;
            end
            memory_note = memory_note+"\nSystem byte order: "+self.sys_constants.endian_text.(self.sys_constants.system_endianness)+".";
        end

        function guess_frames_from_dim3(self, dim3)
            % Guess number of real space frames in X and Y when a dataset is read
            % in as 3D, rather than 4D. 
            %
            % Parameters:
            %    self (Quant4D)
            %    dim3 (int): Total number of real-space frames in a 4D dataset that has been read in as 3D.
            %
            % Returns:
            %    None
        
            self.ImportFramesX.Value = round(sqrt(dim3));
            self.ImportFramesY.Value = round(dim3/self.ImportFramesX.Value);
        end

        function get_dims_from_name(self, filename)
            % Guess dataset size from `filename` if it contains certain
            % regular expressions. Where A, B, C, D are integers. (A,B) = #
            % pixels in Diffraction space. (C,D) = # probe positions in
            % Real space.
            % 
            % Parameters:
            %    self (Quant4D)
            %    filename (str) : 'prefixAxBxCxDbar' or 'scan_xC_yD.raw'
            %
            % Returns:
            %    None

                s = regexp(filename, ["scan_x(\d*)_y(\d*).raw", "(\d*)x(\d*)x(\d*)x(\d*)"], "tokens");
                
                if ~isempty(s{1})
                    % "scan_xC_yD.raw" file name, assume EMPAD file format
                    set([self.ImportPixelsX, ...
                         self.ImportPixelsY, ...
                         self.ImportFramesX, ...
                         self.ImportFramesY], ...
                        {"Value"}, ...
                        num2cell([128, 128, str2double(s{1}{1})])')
                
                elseif ~isempty(s{2})
                    % "AxBxCxD" found in file name, assume (kx, ky, rx, ry)
                    set([self.ImportPixelsX, ...
                         self.ImportPixelsY, ...
                         self.ImportFramesX, ...
                         self.ImportFramesY], ...
                        {"Value"}, ...
                        num2cell(str2double(s{2}{1}))')
                end
                    end

        function guess_frames_from_size(self)
            % Make an initial guess at the dataset dimensions assuming a roughly
            % square field of view (ImportFramesX≈ImportFramesY). Sets the
            % estimated values in their respective numeric fields in the Import UI
            %
            % Parameters:
            %    self (Quant4D)
            %
            % Returns:
            %    None

            if self.ImportPixelsX.Value > 1 && self.ImportPixelsY.Value > 1
                x = sqrt((self.tmp_variables.FileSize-self.DataOffset.Value-self.tmp_variables.fileTail) ...
                    /(self.ImportPixelsX.Value*self.ImportPixelsY.Value*self.byte_size.(self.ImportDataType.Value)+self.FrameHeader.Value+self.FrameFooter.Value));

                set([self.ImportFramesX, ...
                    self.ImportFramesY], ...
                    "Value",max(floor(x),1))
            end
        end

        function import_data(self, event)
            % Function to prepare for dataset import, read the file, and
            % switch the UI to `Alignment` mode
            %
            % Parameters:
            %    self (Quant4D)
            %    event (event.EventData)
            %
            % Returns:
            %    None


            debug_time = tic;

            if ~isfile(self.dataset_parameters.file_path)
                notification_dialog(self, "warn", "File: '"+self.dataset_parameters.file_path+"' is not found!",'File Unfound!');
                return
            end

            % Set save/export filenames etc.
            self.Quant4D_Fig.Name = "Quant4D: " + self.dataset_parameters.file_name + self.dataset_parameters.file_extension;
            self.SaveDirectoryPath.Value = self.dataset_parameters.file_directory;
            self.SaveImagePrefix.Value = self.dataset_parameters.file_name + "_";
            self.ExportFilename.Value = self.dataset_parameters.file_name + "_export";

            % Start file reading here
            try
                err = read_file(self, event);
            catch ME
                % Kill the reading progress update timer
                try stop(self.tmp_variables.tmr), delete(self.tmp_variables.tmr); catch; end
                try delete(self.tmp_variables.progress_dialog); catch; end
                try unload_data(self); catch; end
                stk = "";
                for i = 1:numel(ME.stack)
                    stk = sprintf("%s\n%s, Line: %d", stk, ME.stack(i).name, ME.stack(i).line);
                end
                notification_dialog(self, ...
                    "error", ...
                    sprintf('%s\n%s\n%s%s', ME.identifier, ME.message, ME.Correction, stk), ...
                    "Error during Import!");
                enable_windows(self,true)
                rethrow(ME)
            end
            % If aborted or errors occurred during file reading, reset self like just opened without import
            if err == -1
                reset_Quant4D(self, event);
                return;
            end

            debug_toc(self, event, "", debug_time)

            % Prepare imported data
            if self.dataset_parameters.keep_parameters
                % Enter alignment mode
                self.Mode.Value = "Alignment";

                % Not re-initializing and just to update all images if "swap data"
                mock_UI_callbacks(self, self.UpdateImages)
                mock_UI_callbacks(self, self.Mode)

                % Swap byte check
                dataset_options_callbacks(self, event)

            else
                prepare_data(self, event)

            end

        end

        function err = read_file(self, event)
            % Function to read the dataset from file
            %
            % Parameters:
            %    self (Quant4D)
            %    event (event.EventData)
            %
            % Returns:
            %    err (int | bool) : error code, default: false, -1 if an error has occurred

            debug_time = tic;
            err = false;

            % Use local variables, which is faster
            offs = self.dataset_parameters.offset;
            hdr = self.dataset_parameters.frame_header;
            ftr = self.dataset_parameters.frame_footer;
            order = self.dataset_parameters.byte_orer;
            dtype = self.dataset_parameters.data_type;
            bsize = self.dataset_parameters.byte_size;
            dnpx = self.dataset_parameters.n_pixels_file(1);
            dnpy = self.dataset_parameters.n_pixels_file(1);
            pd = self.dataset_parameters.pixels_binning;
            dnfx = self.dataset_parameters.n_frames_file(1);
            dnfy = self.dataset_parameters.n_frames_file(2);
            fd = self.dataset_parameters.frames_sampling;
            px1 = self.dataset_parameters.pixels_start(1);
            py1 = self.dataset_parameters.pixels_start(2);
            npx = self.dataset_parameters.n_pixels(1);
            npy = self.dataset_parameters.n_pixels(2);
            fx1 = self.dataset_parameters.frames_start(1);
            fy1 = self.dataset_parameters.frames_start(2);
            nfx = self.dataset_parameters.n_frames(1);
            nfy = self.dataset_parameters.n_frames(2);
            frame_size = npx*npy*pd^2*bsize;

            % convert to single/double if int/uint
            dtype1 = dtype;
            if contains(dtype,'int')
                if bsize > 4
                    dtype1 = "double";
                    bsize1 = 8;
                else
                    dtype1 = "single";
                    bsize1 = 4;
                end
                self.dataset_parameters.data_type = dtype1;
                self.dataset_parameters.byte_size = bsize1;
            end

            [self.tmp_variables.progress_dialog, self.tmp_variables.tmr] = import_export_progress(self, "Import", prod(self.dataset_parameters.n_frames), frame_size);

            if ~isempty(self.dataset_parameters.h5ds) % HDF5 import
                % Preallocate array
                data_tmp = zeros(npx, npy, nfx, nfy, dtype1);
                fid = H5F.open(self.dataset_parameters.file_path);
                dset_id = H5D.open(fid, self.dataset_parameters.h5ds);
                file_space_id = H5S.create_simple(4, [dnfy dnfx dnpy dnpx], []);
                mem_space_id = H5S.create_simple(2, [npy*pd npx*pd], []);

                % Read whole
                % data = H5D.read(dset_id,'H5ML_DEFAULT','H5S_ALL','H5S_ALL','H5P_DEFAULT');

                % Read frame by frame
                for ify = 1:nfy
                    for ifx = 1:nfx
                        % Cancel if progress window closed
                        if ~isvalid(self.tmp_variables.progress_dialog)
                            err = -1;
                            break;
                        end

                        % Update processed Frame Number for progress update
                        self.tmp_variables.frame_number(1) = (ify-1)*nfx + ifx;

                        % Read 1 frame at a time; C-like array indices for H5 low-level APIs
                        H5S.select_hyperslab(file_space_id, 'H5S_SELECT_SET', [fy1+(ify-1)*fd, fx1+(ifx-1)*fd, py1, px1]-1, [],[], [1 1 npy*pd npx*pd]);

                        frame = H5D.read(dset_id, 'H5ML_DEFAULT', mem_space_id, file_space_id, 'H5P_DEFAULT');

                        % Pixel binning
                        if pd > 1
                            frame = squeeze(sum(reshape(frame, [pd npx pd npy]), [1 3]),'omitnan');
                        end

                        % Store frame
                        data_tmp(:, :, ifx, ify) = frame;
                    end

                    % break on error
                    if err == -1
                        break;
                    end
                end

                % Close opened handles
                H5S.close(mem_space_id);
                H5S.close(file_space_id);
                H5D.close(dset_id);
                H5F.close(fid);

                % Make dataset a 2D array
                self.data = reshape(data_tmp, prod(self.dataset_parameters.n_pixels), prod(self.dataset_parameters.n_frames));

            elseif self.dataset_parameters.memory_type== "Physical Memory"
                % General reading method; read data into physical memory

                % Pre-allocate array
                data_tmp = zeros(npx, npy, nfx, nfy, dtype1);

                % frame size including header/footer
                dfrSize = hdr+dnpx*dnpy*bsize+ftr;

                % file id
                fid = fopen(self.dataset_parameters.file_path,"r");

                for ify = 1:nfy
                    for ifx = 1:nfx
                        % Cancel if progress window closed
                        if ~isvalid(self.tmp_variables.progress_dialog)
                            err = -1;
                            break;
                        end

                        % Update processed Frame Number for progress update
                        self.tmp_variables.frame_number(1) = (ify-1)*nfx + ifx;

                        % Read 1 frame at a time; move cursor to "frame offset" + "pixel Y offset" in file dataset
                        % Frame indices in dataset file
                        dfx = fx1+(ifx-1)*fd;
                        dfy = fy1+(ify-1)*fd;

                        fseek(fid, offs + (dfx-1 + (dfy-1)*dnfx) * dfrSize + hdr + ((px1-1) + (py1-1)*dnpx) * bsize, 'bof');
                        % Read including "pixel X offset"
                        frame = fread(fid, [dnpx, npy*pd], dtype, 0, order);

                        % Crop "pixel X offset" off from array memory
                        if npx*pd ~= dnpx
                            frame = frame(px1:px1+npx*pd-1, :);
                        end

                        % Pixel binning
                        if pd > 1
                            frame = squeeze(sum(reshape(frame, [pd npx pd npy]), [1 3],'omitnan'));
                        end

                        % Store frame
                        data_tmp(:, :, ifx, ify) = frame;
                    end

                    % break on error
                    if err == -1
                        break;
                    end
                end

                % close file id
                fclose(fid);

                % Make dataset a 2D array
                self.data = reshape(data_tmp,prod(self.dataset_parameters.n_pixels),prod(self.dataset_parameters.n_frames));

            elseif self.dataset_parameters.memory_type== "Virtual Mapping"
                % Virtual memory mapping

                % Create a memory mapped file, rather than reading the file directly into memory
                if ~strcmp(self.sys_constants.system_endianness, order)
                    error("Dataset's endianness is different to that of the system!")
                end

                if hdr == 0 && ftr == 0
                    self.memfile = memmapfile(self.dataset_parameters.file_path, ...
                        'Offset',offs, ...
                        'Format',{dtype1,[prod(self.dataset_parameters.n_pixels), prod(self.dataset_parameters.n_frames)],'data'}, ...
                        'Repeat',1);
                    self.data = self.memfile.Data.data;
                else
                    error("Virtual memory with header/footer > 0 not supported yet.")
                end
            end

            % remove temporary data reference
            clear data_tmp

            % Delete the interruptible progress window
            delete(self.tmp_variables.progress_dialog)

            % Move to GPU if enabled
            if self.dataset_parameters.gpu > 0 && err == 0
                self.tmp_variables.progress_dialog = progress_dialog(self, "Moving dataset to GPU memory ...", "GPU Transfer");
                self.data = gpuArray(self.data);
                delete(self.tmp_variables.progress_dialog)
            end

            % Check data NaN/Inf, without asking to sway byte-order
            selection = check_NaN(self, self.data(:), true);
            if strcmp(selection,'Set NaNs to 0')
                self.data(isnan(self.data(:)))=0;
            end

            debug_toc(self, event, "", debug_time)
        end

        function prepare_data(self, event)
            % Initialize GUI/Image/self.common_parameters defaults based
            % on the specifics of the imported dataset.
            %
            % Parameters:
            %    self (Quant4D)
            %    event (event.EventData)
            %
            % Returns:
            %    None

            self.tmp_variables.progress_dialog = progress_dialog(self, 'Preparing data ...', "Data Preparation");

            % Detector controls

            % Reset alignments
            self.common_parameters.scan_direction_initialized = false;

            % Prepare to enter alignment mode
            self.Mode.Value = "Alignment";
            self.AnnularRadiusLink.Value = false;

            set([self.NSeg, ...
                self.NRung, ...
                self.DetectorRotationSlider, ...
                self.DetectorRotationSpinner, ...
                self.ScanDirectionSlider, ...
                self.ScanDirectionSpinner], ...
                {"Value"}, ...
                {4; ...
                1; ...
                0; ...
                0; ...
                0; ...
                0})

            set([self.VirtualApertureSymmetry, ...
                self.VirtualApertureInvert, ...
                self.VirtualApertureMirror, ...
                self.VirtualApertureMirrorRotation], ...
                {"Value"}, ...
                {1; ...
                0; ...
                0; ...
                0})

            % Alignments

            % Exact center of the Diffraction image
            self.common_parameters.diffraction_center = self.dataset_parameters.n_pixels/2 + 0.5;

            % Exact center of the Real-space image
            self.common_parameters.real_space_center = self.dataset_parameters.n_frames/2 + 0.5;

            % Convergence angle default = 1
            self.Alpha.Value = 1;

            % Set virtual aperture (x,y) default location to diffraction center
            self.common_parameters.virtual_aperture_center = self.common_parameters.diffraction_center;

            % Axes limits, restrict to avoid rounding to pixels outside the image
            self.common_parameters.diffraction_axes_limit = [0.51, self.dataset_parameters.n_pixels(1) + .49, 0.51, self.dataset_parameters.n_pixels(2) + .49];
            self.common_parameters.real_axes_limit = [0.51, self.dataset_parameters.n_frames(1) + .49, 0.51, self.dataset_parameters.n_frames(2) + .49];
            set(self.ui_groups.diffraction_axes, ...
                "XLim" , self.common_parameters.diffraction_axes_limit(1:2), ...
                "YLim",self.common_parameters.diffraction_axes_limit(3:4));
            set(self.ui_groups.real_axes, ...
                "XLim", self.common_parameters.real_axes_limit(1:2), ...
                "YLim",self.common_parameters.real_axes_limit(3:4));

            % Transmitted Beam controls
            if event.Source ~= self.SwapRealXY
                % Keep transmitted beam alignment if swapping Real-space X/Y
                self.common_parameters.transmitted_beam_init = false;

                % set transmitted beam radius, x, y limits and values
                set([self.TransBeamR; ...
                    self.TransBeamX; ...
                    self.TransBeamXSpinner; ...
                    self.TransBeamY; ...
                    self.TransBeamYSpinner], ...
                    {"Limits"}, ...
                    {[eps(), max(self.dataset_parameters.n_pixels)]; ...
                    [0, self.dataset_parameters.n_pixels(1)]; ...
                    [0, self.dataset_parameters.n_pixels(1)]; ...
                    [0, self.dataset_parameters.n_pixels(2)]; ...
                    [0, self.dataset_parameters.n_pixels(2)]}, ...
                    {"Value"}, ...
                    {min(self.dataset_parameters.n_pixels)/10; ...
                    self.common_parameters.diffraction_center(1); ...
                    self.common_parameters.diffraction_center(1); ...
                    self.common_parameters.diffraction_center(2); ...
                    self.common_parameters.diffraction_center(2)});

                % Update Transmitted Beam dependent variables
                transmitted_beam_callbacks(self, event)
            end

            % Real-space ROI controls
            set([self.RealROIFrameX; ...
                self.RealROIFrameY], ...
                {"Limits"}, ...
                {[0 self.dataset_parameters.n_frames(1)]; ...
                [0 self.dataset_parameters.n_frames(2)]}, ...
                {"Value"}, ...
                {self.common_parameters.real_space_center(1); ...
                self.common_parameters.real_space_center(2)})
            self.RealROIInvert.Value = false;
            self.RealROIShape.Value = "full";

            % Export controls
            export_callbacks(self, struct("Source", self.ExportPartialPixels, "EventName", [], "Value", 0))
            export_callbacks(self, struct("Source", self.ExportPartialFrames, "EventName", [], "Value", 0))

            % Image display contrasts and vector field
            for ax = self.ui_groups.image_axes'
                ax.UserData.brightness = 50;
                ax.UserData.contrast = 50;
                ax.UserData.gamma = 1;
                ax.UserData.mask_opacity = 0;
                ax.UserData.vector_field = false;
            end

            % Update all images
            mock_UI_callbacks(self, self.UpdateImages)

            % Close progress bar and Enable panel objects
            delete(self.tmp_variables.progress_dialog);

            % Enter initializing alignment
            mock_UI_callbacks(self, self.Mode)
            self.SettingsTabGroup.SelectedTab = self.DisplayTab;

            % Show the brightness/contrast/gamma controls
            figure(self.Quant4D_Fig)
            figure(self.figures.Settings)

            % alert user to the need to calibrate the transmitted beam
            flash_background(self, [self.DiffractionCalibrationGrid self.TransBeamAlignGrid])
        end

        function d = gather_import_options(self, preview)
            % Collects all import parameters from the Import UI into a
            % structure, `d`.
            %
            % Parameters:
            %    self (Quant4D)
            %    preview (bool) : true = Preview mode, false = Import mode
            %
            % Returns:
            %    d (struct) : dataset parameters from Import UI

            % get file location
            d.file_path = self.ImportFilePath.Value;
            [d.file_directory, d.file_name, d.file_extension] = fileparts(d.file_path);
            d.file_directory = strcat(d.file_directory, filesep);
            d.subimage = self.SubDataset.Value;

            % BYTES offset of: 1) the dataset from the beginning of file, 2) before and 3) after each frame
            d.offset = self.DataOffset.Value;
            d.frame_header = self.FrameHeader.Value;
            d.frame_footer = self.FrameFooter.Value;

            % Endianness (big "b" or little "l"), Data type of the dataset and Size in bytes of the data type
            d.byte_orer = self.ImportByteOrder.Value;
            d.data_type = self.ImportDataType.Value;
            d.byte_size = self.byte_size.(d.data_type);

            % Physical or virtual memory loading
            d.memory_type= self.MemoryType.Value;

            % Select GPU if acceleration is enabled AND not in Import Preview Mode
            d.gpu = self.GPU.Value;
            if ~preview && d.gpu
                gpuDevice(d.gpu);
            end

            % Dimensions of pixels/frames in file and import binning/sampling distance
            d.n_pixels_file = [self.ImportPixelsX.Value, self.ImportPixelsY.Value];
            d.n_frames_file = [self.ImportFramesX.Value, self.ImportFramesY.Value];
            d.pixels_binning= self.DiffractionPartialImportPixelsDist.Value;
            d.frames_sampling = self.RealPartialImportFramesDist.Value;

            % Starting points and Number of pixels/frames after binning/sampling to import
            d.pixels_start = [self.DiffractionPartialImportXStart.Value, self.DiffractionPartialImportYStart.Value];
            d.frames_start = [self.RealPartialImportXStart.Value, self.RealPartialImportYStart.Value];
            d.n_pixels = [self.DiffractionPartialImportX.Value, self.DiffractionPartialImportY.Value];
            d.n_frames = [self.RealPartialImportX.Value, self.RealPartialImportY.Value];

            % Estimated memory usage for current dataset
            d.estimated_memory = self.tmp_variables.estimated_memory;

            % Swap dataset option+self.ImportSummary.Value;
            d.keep_parameters = self.SwapDataset.Value;

            % Notes at import
            d.file_metadata = self.ImportFileMetadata.Value;
            d.import_options = self.ImportSummary.Value;

            % H5 dataset path within the H5 file; if not set empty, the H5 library API will be called when importing
            d.h5ds = [];
            if self.HDF5.Value && d.memory_type== "Physical Memory"
                d.h5ds = d.subimage;
            end
        end

        function output = switch_on_off(~, status)
        % Wrapper function for MATLAB's `OnOffSwitchState()`
        %
        % Parameters:
        %    self (Quant4D) : ignored
        %    status (int | bool) : 0 or false = off; 1 or true = on
        %
        % Returns:
        %    output (str) : "on", "off"

            output = string(matlab.lang.OnOffSwitchState(status));
        end

        function set_external_source(self, event, object, varargin)
            % Set properties of objects that are not `source` if it is a changing event
            %
            % Parameters:
            %    self (Quant4D)
            %    event (event.EventData)
            %    object: UI component, annotation, list of objects with a common property
            %    varargin : property/value pair(s) (i.e. "Value", 1)
            %
            % Returns:
            %    None

            % Get source
            source = event.Source;

            % If not a changing event, set source as well
            if is_static_event(self, event) || isempty(source)
                source = {[]};
            end

            % Convert source to string if it is a character string
            if ischar(source)
                source = string(source);
            end

            % get index of objects that are NOT source
            object = object(:);
            source_index = object ~= source;

            % set properties and values for each object
            for i = 1:numel(varargin)/2
                prop = varargin{2*i-1};
                val = varargin{2*i};
                
                if iscell(prop) && all(numel(object) == numel(prop))
                    prop = prop(source_index);
                end
                
                if iscell(val) && all(numel(object) == numel(val))
                    val = val(source_index);
                end

                set(object(source_index),prop,val);
            end
        end

        function R = rotation_matrix(~, degrees)
            % Rotation matrix, for degree input
            %
            % Parameters:
            %    self (Quant4D) : ignored
            %    degrees (double) : angle in degrees
            %
            % Returns:
            %    R (array) : 2D rotation matrix

            R = [cosd(degrees), sind(degrees);
                -sind(degrees), cosd(degrees)];
        end

        function status = is_static_event(~, event)
            % Function to test whether an event is NOT "MovingROI" or
            % "ValueChanging"; return `true` for `[]` etc. This helps
            % to reduce computational load, especially on image refresh.
            %
            % Parameters:
            %    self (Quant4D) : ignored
            %    event (event.EventData)
            %
            % Returns:
            %    status (bool) : true if `event` is static; else false

            status = isempty(event) || ...
                     ~(isfield(event,"EventName") || ...
                     isprop(event,"EventName")) || ...
                     isempty(event.EventName) || ...
                     ~ismember(event.EventName, ["MovingROI" "ValueChanging"]);
        end

        function h = h5_datasets(~,file)
            % Return all h5 Datasets with some key info
            %
            % Parameters:
            %    self (Quant4D) : ignored
            %    file (str) : file path from self.ImportFilePath.Value
            %
            % Returns:
            %    h (struct) : h5 Dataset information, including Name, Dataspace, Datatype, offset, size, byte_ordering, and type.

            h5_info = h5info(file);
            h = struct("Name", {}, ...
                       "Dataspace", {}, ...
                       "Datatype", {}, ...
                       "offset", {}, ...
                       "size", {}, ...
                       "byte_order", {}, ...
                       "type", {});

            get_groups(h5_info);
            type_details();

            % End of main function
            function get_groups(g)
                for i = 1:length(g)
                    datasets(g(i).Name, g(i).Datasets);
                    get_groups(g(i).Groups);
                end
            end

            function datasets(p, d)
                if p(end) ~= '/'
                    p(end + 1) = '/';
                end

                for i = 1:length(d)
                    h(end + 1).Name = strcat(p, d(i).Name); %#ok<*AGROW>
                    h(end).Dataspace = d(i).Dataspace;
                    h(end).Datatype = d(i).Datatype;
                end
            end

            function type_details()
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

                    byte_order = H5T.get_order(type_id);
                    % Byte order
                    switch byte_order
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

                    data_type = h(j).Datatype;
                    switch data_type.Class
                        case 'H5T_FLOAT'
                            if data_type.Size == 4
                                h(j).type = "single";
                            elseif data_type.Size == 8
                                h(j).type = "double";
                            end

                        case 'H5T_INTEGER'
                            h(j).type = sprintf('int%d', data_type.Size * 8);
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

        function debug_toc(self, event, notes, tic_start)
            % Function to debug and time functions
            %
            % Parameters:
            %    self (Quant4D)
            %    event (event.EventData)
            %    notes (str) : debugging information
            %    tic_start (uint64) : stopwatch timer start
            %
            % Returns:
            %    None

            if self.debug
                source_name = "";
                event_name = "";

                if ~isempty(event)
                    % Find name of the source field_name` by comparing the source with fieldnames of `self`
                    if (isfield(event, "Source") || isprop(event, "Source")) && ~isempty(event.Source)
                        field_name = fieldnames(self);
                        for i = 1:length(field_name)
                            if ~isa(self.(field_name{i}), 'gpuArray') && isequal(self.(field_name{i}), event.Source)
                                source_name = field_name{i};
                                break;
                            end
                        end
                    end

                    % Get EventName
                    if (isfield(event, "EventName") || ...
                        isprop(event, "EventName")) && ...
                        ~isempty(event.EventName)
                        event_name = event.EventName;
                    end
                end

                % caller(2).name`: caller of the function on dbstack
                caller = dbstack;

                % print debug notes to Command Window
                fprintf('%s, %s, %s, %s: %.3f s\n', caller(2).name, source_name, event_name, notes, toc(tic_start));
            end
        end

        function flash_background(~, target)
            % Function to flash the background of UIs, which have
            % `BackgroundColor`. This process will pause the whole
            % program during flashing
            %
            % Parameters:
            %    self (Quant4D) : ignored
            %    target : UI component
            %
            % Returns:
            %    None

            % Input `target` can be arrays of multiple UIs;
            % which will flash simultaneously 
            
            % Get original color
            original_color = get(target, "BackgroundColor");

            % Make `original_color` a cell if not already
            if ~iscell(original_color)
                original_color = {original_color};
            end

            % commence flashing between green and `orignal_color` twice
            for i = 1:2
                pause(0.2);
                set(target, "BackgroundColor",'g');
                pause(0.2);
                set(target,{"BackgroundColor"},original_color)
            end
        end

        function change_icon_background(self, source)
            % state button background color change to highlight when it
            % is/isn't enabled
            %
            % Parameters:
            %    self (Quant4D)
            %    source (matlab.ui.control.Button) : UI State Button
            %
            % Returns:
            %    None

            if source.Value
                source.BackgroundColor = self.sys_constants.highlight_color;
            else
                source.BackgroundColor = self.sys_constants.background_color + 0.02;
            end
        end

        function get_GPU(self)
            % Function to get all available GPUs
            %
            % Parameters:
            %    self (Quant4D)
            %
            % Returns:
            %    None

            % initialize items
            self.GPU.Items = {''};
            self.GPU.ItemsData = 0;
            self.sys_constants.nGPU = -1;

            % Check if parallel computing toolbox is installed for GPU acceleration
            if any(strcmpi("Parallel Computing Toolbox", {ver().Name}))
                try self.sys_constants.nGPU = gpuDeviceCount(); catch; end
            end

            % Find GPU devices and turn on/off GPU support;
            % `self.GPU.Value` == `0` always means "GPU off"
            switch self.sys_constants.nGPU
                case -1
                    self.GPU.Items = {'Parallel Computing Toolbox missing. GPU acceleration disabled.'};
                    self.GPU.Value = 0;
                
                case 0 % no GPU devices
                    self.GPU.Items = {'No GPU found.'};
                    self.GPU.ItemsData = 0;
                    self.GPU.Value = 0;
                
                otherwise % 1 or more devices found
                    maxmem = 0;
                    for i = 1:self.sys_constants.nGPU
                        try
                            tmp = parallel.gpu.GPUDevice.getDevice(i);
                            self.sys_constants.gpu(i).memory = tmp.TotalMemory;
                            self.sys_constants.gpu(i).name = tmp.Name;
                            self.GPU.Items{i} = sprintf('%d. %s %.1f GiB', i, self.sys_constants.gpu(i).name, self.sys_constants.gpu(i).memory/1024^3);
                            self.GPU.ItemsData(i) = i;
                            
                            % Default to GPU with the most memory
                            if self.sys_constants.gpu(i).memory > maxmem
                                maxmem = self.sys_constants.gpu(i).memory;
                                self.GPU.Value = i;
                            end
                        catch
                        end
                    end
                    self.GPU.Items{end + 1} = 'GPU off';
                    self.GPU.ItemsData(end + 1) = 0;
            end
        end

        function get_memory(self)
            % Function to Check usable system memory and make sure the
            % file will fit
            %
            % Parameters:
            %    self (Quant4D)
            %
            % Returns:
            %    None

            if ispc
                [~,tmp] = memory;
                self.sys_constants.total_memory = tmp.PhysicalMemory.Total;
                self.sys_constants.free_memory = tmp.PhysicalMemory.Available;

            elseif ismac
                [~,self.sys_constants.total_memory] = system('sysctl -n hw.memsize');
                self.sys_constants.total_memory = str2double(self.sys_constants.total_memory);
                [~,page_memory_size] = system("vm_stat | grep 'page size' | awk '{print $8}'");
                page_memory_size = str2double(page_memory_size);
                [~,wired_memory] = system("vm_stat | grep 'wired' | awk '{print $4}'");
                wired_memory = str2double(wired_memory)*page_memory_size;
                self.sys_constants.free_memory = self.sys_constants.total_memory - wired_memory;
            
            elseif isunix % memory output is in kB => multiply by 1024 for consistency 
                [~,self.sys_constants.total_memory] = system("cat /proc/meminfo | grep MemTotal: | awk '{print $2}'");
                self.sys_constants.total_memory = str2double(self.sys_constants.total_memory)*1024; 
                [~,self.sys_constants.free_memory] = system("cat /proc/meminfo | grep MemAvailable: | awk '{print $2}'");
                self.sys_constants.free_memory = str2double(self.sys_constants.free_memory)*1024;
            end
        end

        % *********************** UI components ***********************
        % Import/export binning/sampling distances:
        %   self.DiffractionPartialImportPixelsDist
        %   self.RealPartialImportFramesDist
        %   self.DiffractionPartialExportPixelsDist
        %   self.RealPartialExportFramesDist
        %
        % DATASET DIMENSIONS IN FILE ON DISK:
        %   self.ImportPixelsX
        %   self.ImportPixelsY
        %   self.ImportFramesX
        %   self.ImportFramesY
        %
        % IMPORT/EXPORT DIMENSIONS (AFTER BINNING/SAMPLING/CROPPING):
        %   self.DiffractionPartialImportX
        %   self.DiffractionPartialImportY
        %   self.RealPartialImportX
        %   self.RealPartialImportY
        %   self.DiffractionPartialExportX
        %   self.DiffractionPartialExportY
        %   self.RealPartialExportX
        %   self.RealPartialExportY
        %
        % IMPORT/EXPORT START POSITIONS (CROPPING):
        %   self.DiffractionPartialImportXStart
        %   self.DiffractionPartialImportYStart
        %   self.RealPartialImportXStart
        %   self.RealPartialImportYStart
        %   self.DiffractionPartialExportXStart
        %   self.DiffractionPartialExportYStart
        %   self.RealPartialExportXStart
        %   self.RealPartialExportYStart
        %
        %
        % ******************** self.dataset parameters *********************
        %
        % DATASET DIMENSIONS IN FILE ON DISK:
        %   self.dataset_parameters.n_pixels_file
        %   self.dataset_parameters.n_frames_file
        %
        % IMPORT DIMENSIONS (AFTER BINNING/SAMPLING/CROPPING):
        %   self.dataset_parameters.n_pixels
        %   self.dataset_parameters.n_frames
        %
        % IMPORT START POSITIONS (CROPPING):
        %   self.dataset_parameters.pixels_start
        %   self.dataset_parameters.frames_start
        function [notes, binning, xy_start, n_points, xy_end] = range_import_export(self, event)
            % Function to calculate import/export range for pixels/frames
            %
            % Parameters:
            %    self (Quant4D)
            %    event (event.EventData)
            %
            % Returns:
            %    notes (str) : Diffraction or Real space-dependent notes on import range and binning
            %    binning (int) : binning distance in Diffraction, sub-sampling distance in Real
            %    xy_start ([int int]) : starting pixels or frames in x,y
            %    n_points ([int int]) : number of pixels or frames in x,y
            %    xy_end ([int int]) : ending pixels or frames in x,y

            source = event.Source;
            
            % `uispinner` upper/lower limits must be different, so now set lower limit `0` but force minimum to `1`
            if isfield(event, "Value") || isprop(event, "Value")
                value = max(event.Value, 1);
            end
           
            % Round positions from ROIs
            if isprop(event,'CurrentPosition')
                position = round(event.CurrentPosition);
            end

            % `space`/`unit`: "Diffraction"/"Pixels" OR "Real"/"Frames"
            if contains(source.Tag, "Diffraction")
                space = "Diffraction";
                unit = "Pixels";
            else
                space = "Real";
                unit = "Frames";
            end

            % `action`: "Import" or "Export"
            if contains(source.Tag, "Import")
                action = "Import";
                % Raw dataset dimensions, e.g. self.ImportPixelsX.Value
                data_size = [self.(action+unit+"X").Value, self.(action+unit+"Y").Value];
            else
                action = "Export";
                % Loaded dataset dimensions
                data_size = self.dataset_parameters.("n_"+lower(unit));
            end

            % Binning/Sampling (self.DiffractionPartialImportPixelsDist, self.DiffractionPartialExportPixelsDist, self.RealPartialImportFramesDist or self.RealPartialExportFramesDist)
            binning = self.(space+"Partial"+action+unit+"Dist").Value;
            
            % Get values from UI
            switch source.Tag
                case "Export Diffraction ROI" % From Export Diffraction ROIs
                    xy_start = position(1:2);
                    n_points = max(floor((position(3:4)+1)/binning), 1);
                
                case "Export Real ROI" % From Export Real-space ROIs
                    xy_start = position(1:2);
                    n_points = floor(position(3:4)/binning)+1;
                
                otherwise % From other sources
                    % self.DiffractionPartialImportXStart, self.RealPartialExportXStart etc, (X/Y)Start UIs
                    xy_start = [self.(space+"Partial"+action+"XStart").Value self.(space+"Partial"+action+"YStart").Value];
                    
                    % self.DiffractionPartialImportX, self.RealPartialExportX etc, n_points X & Y UIs
                    n_points = [self.(space+"Partial"+action+"X").Value self.(space+"Partial"+action+"Y").Value];
            end
            
            % Replace value with current event value
            switch source
                case self.(space+"Partial"+action+unit+"Dist")
                    % Binning/Sampling UI
                    binning = value;
                
                case self.(space+"Partial"+action+"XStart")
                    % XStart UI
                    xy_start(1) = value;
                
                case self.(space+"Partial"+action+"YStart")
                    % YStart UI
                    xy_start(2) = value;
                
                case self.(space+"Partial"+action+"X")
                    % n_points X UI
                    n_points(1) = value;
                
                case self.(space+"Partial"+action+"Y")
                    % n_points Y UI
                    n_points(2) = value;
                
                case {self.("Import"+unit+"X") self.("Import"+unit+"Y") self.(action+"Partial"+unit)}
                    % Reset range options if dataset raw dimension changes OR partial selection enables/disables
                    % Update binning/sampling UI limits
                    self.(space+"Partial"+action+unit+"Dist").Limits(2) = min(data_size);
                    
                    % Update preview frame limits
                    if action == "Import" && unit == "Frames"
                        set([self.PreviewFrameX, self.PreviewFrameY], ...
                            {"Limits"}, ...
                            {[0 data_size(1)];[0 data_size(2)]}, ...
                            {"Value"}, ...
                            {data_size(1);data_size(2)});
                    end
                    binning = 1;
                    xy_start = [1 1];
                    n_points = data_size;
            end

            % In general, n_points are determined by (X/Y)Start and Binning/Sampling, unless n_points are the source
            % Whether n_points X or Y are not the source
            source_index = [self.(space+"Partial"+action+"X") self.(space+"Partial"+action+"Y")] ~= source;
            if unit == "Pixels"
                % Determine n_points X/Y if not source
                n_points(source_index) = max(1, min(n_points(source_index), ...
                                             floor((data_size(source_index)-xy_start(source_index)+1)/binning)));
                xy_start = min(xy_start, data_size-n_points*binning+1);
                
                % Endpoints of Pixel ranges
                xy_end = xy_start + n_points*binning - 1;

                % Upper limits of Pixel (X/Y)Start and n_points X & Y
                xy_start_limit = data_size - binning + 1;
                n_points_limit = floor(data_size/binning);
                
                % Positions for Export ROI
                position = [xy_start, n_points*binning-1];

                notes = "Diffraction Range (in pixels [px])";
                unit_abbreviation = " px";
                binning_text = "binning to ";

            else % "Frames"
                % Frame sampling has slightly different logic to pixel binning
                n_points(source_index) = min(n_points(source_index), ...
                                             floor((data_size(source_index) - xy_start(source_index))/binning) + 1);
                
                % Endpoints of Frame ranges
                xy_start = min(xy_start, data_size - (n_points-1)*binning);
                xy_end = xy_start + (n_points - 1)*binning;
                
                % Upper limits of Frame (X/Y)Start and n_points X & Y
                xy_start_limit = data_size;
                n_points_limit = floor((data_size-1)/binning)+1;
                
                % Positions for Export ROI
                position = [xy_start (n_points-1)*binning];
                
                notes = "Real-space Range (in frames [fr])";
                unit_abbreviation = " fr";
                binning_text = "sampling ";
            end

            % Set (X/Y)Start, n_points X & Y and Binning/Sampling UIs
            set([self.(space+"Partial"+action+"XStart"); ...
                 self.(space+"Partial"+action+"YStart"); ...
                 self.(space+"Partial"+action+"X"); ...
                 self.(space+"Partial"+action+"Y"); ...
                 self.(space+"Partial"+action+unit+"Dist")], ...
                {"Limits"}, ...
                num2cell([xy_start_limit n_points_limit min(data_size)]'.*[0 1],2), ...
                {"Value"}, ...
                num2cell([xy_start n_points binning]'))

            % Try to update Export ROIs
            if action == "Export"
                set(findobj(self.ui_groups.(lower(space)+"_axes"), "Tag", "Export "+space+" ROI"), "Position", position)
            end
            
            points_text = n_points + unit_abbreviation;
            
            % If any binning/sampling add text explaining the change in
            % number of points
            if binning > 1
                points_text = binning_text + points_text + " from " + ...
                     (xy_end - xy_start + 1) + unit_abbreviation;
            end
            
            % If not from 1st to last pixel/frame
            source_index = xy_start > 1 | xy_end < data_size;
            points_text(source_index) = n_points(source_index) + unit_abbreviation + ...
                               ", " + (xy_start(source_index)-1) + "/" + ...
                               (data_size(source_index)-xy_end(source_index)) + ...
                               unit_abbreviation + " offset from start/end";

            % Range notes
            notes = sprintf("%s:\n  X = %s–%s (%s)\n  Y = %s–%s (%s)\n", notes, ["" + xy_start; "" + xy_end; points_text]);
        end

        function [wait_bar, tmr] = import_export_progress(self, process, n_frames, frame_size)
            % Function for progress bar of data import/export, with a `timer()` to update its progress per second
            %
            % Parameters:
            %    self (Quant4D)
            %    process (str) : "Import", "Export"
            %    n_frames (int) : total number of Real space frames (i.e. rx*ry)
            %    frame_size (int) : frame size in bytes
            %
            % Returns:
            %    wait_bar (matlab.ui.Figure) : waitbar to display progress
            %    tmr (timer) : 1 Hz timer to update progress bar information (i.e. import rate)


            % `process` will be 'Import'/'Export', and used for texts like "Import/Export" + "ing/ed"
            wait_bar = progress_dialog(self, sprintf("\n%sing ...\n",process), "Data "+process, true);
            
            % Total time and global variable for processed frames of
            % [this second, last second]
            total_time = tic;
            self.tmp_variables.frame_number = [0 0];
            
            % `timer()` to run the sub function per second
            tmr = timer("TimerFcn", @(~,~)update_waitbar(self, wait_bar), ...
                        "ExecutionMode", "fixedDelay", ...
                        "Name", process);
            
            % Start the timer now
            tmr.start();
            
            % Kill the timer when progress windows closes
            wait_bar.DeleteFcn = {@(~,~,t) kill_timer(self,t), tmr};

            function update_waitbar(self, wait_bar)
                % Update progress per second

                % Current  and previous frame number
                current_frame = self.tmp_variables.frame_number(1);
                previous_frame = self.tmp_variables.frame_number(2);

                % Estimate remaining time based on fraction of frames
                % processed since timer executes @ 1 Hz
                if current_frame == previous_frame
                    remaining_time = 0;
                else
                    remaining_time = (n_frames - current_frame) / ...
                                     (current_frame - previous_frame);
                end

                % update waitbar
                waitbar(current_frame/n_frames, ...
                        wait_bar, ...
                        sprintf("%sed frames: %d/%d\nSpeed: %.2f MiB/s\nElapsed: %s \t|\t Remaining: %s", ...
                                process, current_frame, n_frames, (current_frame - previous_frame) * frame_size/1024^2, ...
                                duration(seconds(floor(toc(total_time))),'Format','mm:ss'), ...
                                duration(floor(seconds(remaining_time)),'Format','mm:ss') ...
                                )...
                         );
                
                % move current frame number to previous frame number slot
                self.tmp_variables.frame_number(2) = current_frame;
            end

            function kill_timer(self, tmr)
                % Function to kill the timer and keep windows disabled when
                % progress windows is closed

                stop(tmr);
                delete(tmr);
                self.enable_windows(false)
            end
        end

        function mask = import_mask(self, space)
            % Function to import mask for given (diffraction/real) space
            %
            % Parameters:
            %    self (Quant4D)
            %    space (str) : "Real", "Diffraction"
            %
            % Returns:
            %    mask (array) : array imported by user to mask Real or Diffraction space


            % get `data_size` from `space`: "n_pixels" or "n_frames"
            if space == "Real"
                space_name = "Real-space";
                data_size = self.dataset_parameters.n_frames;
            else % "Diffraction"
                space_name = "Diffraction";
                data_size = self.dataset_parameters.n_pixels;
            end

            mask = [];
            message = "";
            file_types = '*.tif;*.tiff;*.png;*.jpg;*.jpeg;*.bmp;*.gif';
            
            % open file selection UI
            [file,fpath] = uigetfile({file_types, ['Supported Types (' file_types ')']; ...
                                      '*.*','All Files (*.*)'}, ...
                                      sprintf("Select a mask image with shape [%d,%d]",data_size), ...
                                      "MultiSelect", "off");
            
            % get file extension
            try
                [~,~,extension] = fileparts(file);
            catch
                extension = "";
            end
            
            % force lowercase
            switch lower(extension)
                case {'.tif';'.tiff';'.png';'.jpg';'.jpeg';'.bmp';'.gif'}
                    % permute mask, `imread()` transposes images implicitly
                    mask = permute(imread([fpath,file]), [2 1 3]);
                    
                    % Check size/orientation
                    mask_size = size(mask, [1 2]);
                    
                    % If dimension mismatch
                    if ~isequal(mask_size, data_size)
                        % If dimension transposed
                        if isequal(mask_size, flip(data_size))
                            mask = permute(mask, [2 1 3]);
                            message = message + ...
                                sprintf("Image size [%d,%d] transposed to fit data's %s size [%d,%d].\n", mask_size, space_name, data_size);
                        else
                            notification_dialog(self, "warn", sprintf("Image size [%d,%d] does not fit data's %s size [%d,%d]!", ...
                                mask_size, space_name, data_size),"Dimension Mismatch");
                            return
                        end
                    end
                    % Convert to double
                    mask = double(mask);
                
                case ""
                    % Canceled, etc. -> return now
                    return
                
                otherwise
                    notification_dialog(self, "warn", "File type '*"+extension+"' currently not supported!", "Import Failed");
                    return
            end

            % check for NaNs and Infs, set any to 0
            if any(isnan(mask(:)) | isinf(mask(:)))
                mask(isnan(mask) | isinf(mask)) = 0;
                message = message + "NaN/Inf found in image, and set to 0.\n";
            end

            % Convert RGB to gray scale
            if size(mask,3) > 1
                mask = rgb2gray(mask);
                message = message + "Converted from RGB to grayscale.\n";
            end

            % Try to scale the maximum to 1
            mask_max = max(mask(:));
            if mask_max ~= 0 && mask_max ~= 1
                mask = mask/mask_max;
                message = message+"The maximum was "+mask_max+"; now scaled to 1, by `IMG = IMG/"+mask_max+"`.\n";
            end

            % Notification
            if message ~= ""
                message = "Please note:\n"+message+"\n";
            end
            notification_dialog(self, "help", sprintf(message+"Please check the "+space_name+" Mask image."),'Mask Imported');
            figure(self.figures.(space+"Mask"))
        end

        function plot_all_patterns(self, event)
            % Wrapper function for (re)plotting all images
            %
            % Parameters:
            %    self (Quant4D)
            %    event (event.EventData)
            %
            % Returns:
            %    None

            debug_time = tic;

            % Update images if visible OR not in changing event;
            % include CoMs if in the modes
            for id = self.ui_groups.image_id(contains(self.ui_groups.image_type, ["Primary";"Mask"]) | ...
                                            (ismember(self.Mode.Value, ["CoM" "DPC"]) & ...
                                             self.ui_groups.image_type == "CoM" & ...
                                             self.ui_groups.image_id ~= "ColorWheel"))'
                
                if is_static_event(self, event) || self.figures.(id).Visible
                    plot_image(self, event, id)
                end

            end

            debug_toc(self, event, "", debug_time)
        end

        function plot_image(self, event, id)
            % Generic function for plotting an image on a given axis with brightness/contrast/gamma values
            %
            % Parameters:
            %    self (Quant4D)
            %    event (event.EventData)
            %    id (str) : image identification string
            %
            % Returns:
            %    None

            % Special case for plotting the color wheel
            if id == "ColorWheel"
                plot_colorwheel();
            end

            % get axis and user_data
            ax = self.image_axes.(id);
            user_data = ax.UserData;

            % clear old `image` on `ax`
            delete(findobj(ax, "Tag", "Image "+user_data.space+" "+user_data.type));
            
            % Abort if image not yet ready
            if ~isfield(self.images, id) || isempty(self.images.(id)) %|| isempty(self.masks)
                if isequal(id, self.DisplayImage.Value)
                    self.ImageStatistics.Value = ax.UserData.name;
                end
                return;
            end

            % Raw array is column-major; transposed to row-major `im`
            im = self.images.(id)';

            % special case for color mixing custom masks
            if strcmp(self.Mode.Value, "Custom") && strcmp(self.CustomDetectorInterMask.Value, "Color Mix")
                % otherwise take over the image with a color mix
                switch id
                    case "Real"
                        % Zeros if no masks yet
                        if ~isfield(self.masks,'CustomColorMix')
                            im = zeros(self.dataset_parameters.n_frames, self.dataset_parameters.data_type);
                        else
                            im = self.images.RealColorMix;
                        end
                    case "DiffractionMask"
                        % Zeros if no masks yet
                        if ~isfield(self.masks,'CustomColorMix')
                            im = zeros(self.dataset_parameters.n_pixels, self.dataset_parameters.data_type);
                        else
                            im = self.masks.CustomColorMix;
                        end
                end
            end

            % Put usable values in `image_stats` for statistics
            image_stats = im(~(isnan(im) | isinf(im)));
            
            % Make `image_stats` NaN if no usable values
            if isempty(image_stats)
                image_stats = NaN();
            end

            % Find maximum/minimum/range
            [image_min, image_max] = bounds(image_stats(:));
            image_range = image_max - image_min;
            
            % Brightness between -0.5 and 0.5; Contrast between -Inf and 0.5
            image_brightness = (user_data.brightness-50)/100;
            image_contrast = log2(max(realmin(), user_data.contrast/50))/2; % Avoid log2(0)
            
            % Display limits from brightness/contrast; have the same magnitude to the raw image `im`
            image_low = image_min - (image_brightness - image_contrast)*image_range;
            image_high = image_max - (image_brightness + image_contrast)*image_range;
            
            % Normalize image, and apply display thresholds; `im_norm` is always between 0 and 1
            if image_high == image_low && (image_high <= 1 || image_high >= 0)
                % If display limits are both 1 or 0, then no rescale (e.g. `im` is all 1 or 0)
                im_norm = im;

            elseif image_high > image_low || (image_high == image_low && (image_high > 1 || image_high < 0))
                % Normal case for upper limit > lower limit, just apply the limits than rescale
                im_norm = rescale(im, "InputMin", image_low, "InputMax", image_high);
            
            else
                % Display limits are too close or identical, then make
                % `im_norm` binary; If limits are NaN, make them 0.5
                im_norm = (image_high + image_low)/2;
                im_norm(isnan(im_norm)) = 0.5;
                image_high = im_norm;
                image_low = im_norm;
                im_norm = double(im > im_norm);
            end
            
            % Plot the row-major array as row-major `image` and apply gamma
            im_display = imagesc(ax, ...
                                 im_norm.^user_data.gamma, ...
                                 "Tag", "Image "+user_data.space+" "+user_data.type);
            
            % Plot the background, which zooms with the image, for images that rely on `AlphaData` shading
            background = fill(ax, ...
                              [0.5 ax.XLim(2) ax.XLim(2) 0.5], ...
                              [0.5 0.5 ax.YLim(2) ax.YLim(2)], ...
                              "k", ...
                              "Tag", "Image "+user_data.space+" "+user_data.type);

            % Plot mask opacity on non-mask/non-preview image
            if ~ismember(user_data.type, ["Mask" "Preview"])
                mask = self.images.(user_data.space+"Mask")';
                im_display.AlphaData = (1-user_data.mask_opacity/100)*(1-logical(mask))+logical(mask);
            end
            
            % Shade CoM/DPC Phase with Magnitude
            if id == "CoMPhMag"
                im_display.AlphaData = im_display.AlphaData.*self.images.CoMMagNorm';
            end
            
            % Move the `image` to the bottom level of the axis children
            ax.Children = [setdiff(ax.Children,[im_display; background],'stable'); im_display; background];
            
            % Assign the `im_display` `background` to global handles
            self.image_displays.(id) = im_display;
            self.image_displays.(id+"Background") = background;

            % Plot vector field, if selected
            plot_vector_field();
            
            % Only update statistics if not in changing Event AND it is the "selected" image
            if isequal(id, self.DisplayImage.Value) && is_static_event(self, event)
                update_display_image_stats();
            end

            %%% Sub functions
            % Function to update image statistics
            function update_display_image_stats()
                debug_time = tic;
                
                % Get Histogram axis
                hist_ax = self.HistogramAxes;

                % Update histogram; skip if image unchanged
                if is_different_to_previous(self, 'image_stats', image_stats)
                    
                    % Warn if NaNs/Infs are present
                    if numel(im) ~= numel(image_stats)
                        nanwarn = "Contains NaN/Inf";
                    else
                        nanwarn = "";
                    end

                    % Update ImageStatistics display panel text
                    self.ImageStatistics.Value = ...
                        sprintf('min:% -14.7g std:% -14.7g\nmax:% -14.7g sum:% -14.7g\navg:% -14.7g %s', ...
                        image_min, std(image_stats,0, "all"), image_max, sum(image_stats, "all",'omitnan'), mean(image_stats, "all"), nanwarn);

                    % Delete any previous histogram
                    delete(findobj(hist_ax, "Tag", "HistBars"))

                    % Generate an intensity histogram for the selected image
                    h = histogram(hist_ax, ...
                                  image_stats, ...
                                  128, ...
                                  "FaceColor", "r", ...
                                  "Tag", "HistBars");

                    % Set histogram plot limits
                    if image_max > image_min
                        hist_ax.XLim = [image_min image_max] + [-1 1]*0.02*image_range;
                    else
                        hist_ax.XLim = [-Inf Inf];
                    end
                    
                    % Make sure upper limit is at least 1
                    hist_ax.YLim = [0.5 max([h.BinCounts*1.1, 1])];
                end

                % Update histogram annotations; skip if values unchanged
                if is_different_to_previous(self, 'hist', {ax image_max image_min image_range image_high image_low user_data.gamma self.HistogramLog.Value})
                    % Update ROIs
                    % Draw ROI of range if not yet
                    if isempty(findobj(hist_ax, "Tag", "HistROI"))
                        self.annotations.hist.Box = drawrectangle(hist_ax, ...
                                                                 "Position", [1 1 1 1], ...
                                                                 "LineWidth", 1, ...
                                                                 "MarkerSize", eps(), ...
                                                                 "FaceAlpha", 0.1, ...
                                                                 "InteractionsAllowed", "translate");

                        self.annotations.hist.Hi = drawpoint(hist_ax, "Position",[1 1]);
                        self.annotations.hist.Lo = drawpoint(hist_ax, "Position",[1 1]);
                        
                        % add listeners
                        addlistener([self.annotations.hist.Box, ...
                                     self.annotations.hist.Lo, ...
                                     self.annotations.hist.Hi], ...
                                    "MovingROI", @move_histogram_high_low);
                        user_data.Move = addlistener([self.annotations.hist.Box, ...
                                                      self.annotations.hist.Lo, ...
                                                      self.annotations.hist.Hi], ...
                                                     "ROIMoved", @move_histogram_high_low);
                        
                        % set parameters
                        set([self.annotations.hist.Box, ...
                             self.annotations.hist.Lo, ...
                             self.annotations.hist.Hi], ...
                            "Deletable", false, ...
                            "UserData", user_data, ...
                            "Tag", "HistROI")
                    end

                    % Save current display limits to ROIs
                    self.annotations.hist.Box.UserData = {ax image_max image_min image_range image_high image_low};

                    % Update ROIs if not called from them
                    if ~ismember(event.Source, [self.annotations.hist.Box self.annotations.hist.Lo self.annotations.hist.Hi])
                        move_histogram_high_low(event.Source, event);
                    end

                    % Update other annotations
                    delete(findobj(hist_ax, "Tag", "HistAnnot"))
                    
                    % Gamma line
                    x = linspace(image_low,image_high,100);
                    y = ((x-image_low)/(image_high-image_low)).^user_data.gamma.*range(hist_ax.YLim) + hist_ax.YLim(1);
                    self.annotations.hist.gamCrv = plot(hist_ax, ...
                                                       x, y, ...
                                                       "Color", "k", ...
                                                       "Tag", "HistAnnot");
                    
                    % Print display limits on the histogram
                    self.annotations.hist.note = text(hist_ax, ...
                                                     0.02, 0.96, ...
                                                     sprintf('Hi:% -.3g\nLo:% -.3g', image_high, image_low), ...
                                                     "VerticalAlignment", "top", ...
                                                     "BackgroundColor", "w", ...
                                                     "Units", "normalized", ...
                                                     "FontName", "FixedWidth", ...
                                                     "FontWeight", "bold", ...
                                                     "FontSize", 11, ...
                                                     "Tag", "HistAnnot");
                    self.annotations.hist.note.BackgroundColor(4) = 0.7;
                end

                debug_toc(self, event, "", debug_time)

                % Sub function for ROI update
                function move_histogram_high_low(source, event)
                    if isprop(event,'CurrentPosition')
                        position = event.CurrentPosition;
                    end
                    
                    % Get preset values
                    hist_annotation = self.annotations.hist;
                    hist_ax = self.HistogramAxes;
                    [i_ax, i_max, i_min, i_range, i_hi, i_lo] = deal(hist_annotation.Box.UserData{:});
                    y_lim = hist_ax.YLim;

                    switch source
                        case hist_annotation.Box
                            i_lo = position(1);
                            i_hi = position(1) + position(3);

                        case hist_annotation.Lo
                            i_lo = position(1);

                        case hist_annotation.Hi
                            i_hi = position(1);
                    end
                    
                    % Sort out upper/lower limits
                    i_hi = max(i_lo,i_hi);
                    i_lo = min(i_lo,i_hi);
                    
                    % Find mid-height of the histogram, log- or linear-scale
                    if self.HistogramLog.Value
                        ymid = sqrt(prod(y_lim));
                    else
                        ymid = mean(y_lim);
                    end
                    
                    % Update ROI
                    set([hist_annotation.Box, ...
                         hist_annotation.Hi, ...
                         hist_annotation.Lo], ...
                        {"Position"}, ...
                        {[i_lo, y_lim(1), i_hi-i_lo, y_lim(2)-y_lim(1)]; ...
                         [i_hi ymid]; ...
                         [i_lo ymid]})
                    
                    % Limit ROI translating area
                    drawing_area = [hist_ax.XLim(1), ymid, range(hist_ax.XLim), 0];
                    
                    if any(isinf(drawing_area))
                        drawing_area = "auto";
                    end

                    set([hist_annotation.Box, ...
                         hist_annotation.Hi, ...
                         hist_annotation.Lo], ...
                        "DrawingArea", drawing_area, ...
                        "Visible", self.DisplayContrast.Enable)
                    
                    % Update UI and image if called from ROIs
                    if ismember(source,[hist_annotation.Box, hist_annotation.Hi, hist_annotation.Lo])
                        i_ax.UserData.brightness = clip(double(50+(i_max+i_min-i_hi-i_lo)/2/i_range*100),0,100);
                        i_ax.UserData.contrast = clip(double(2^((i_max-i_min-i_hi+i_lo)/2/i_range*2)*50),0,100);
                        display_callbacks(self, event);
                    end
                end
            end

            % Function to plot a vector field image over top of the DPC or CoM images (either magnitude, angle, or combination)
            function plot_vector_field()
                delete(findobj(ax, "Tag", "VectorField"))
                vec = user_data.vector_field;
                
                if ~vec || ~ismember(self.Mode.Value, ["CoM", "DPC"])
                    return;
                end
                
                % Plot vector arrows over the selected image
                self.annotations.vector_field.(id) = quiver(ax, ...
                                                           1:vec:self.dataset_parameters.n_frames(1), ...    % x location
                                                           1:vec:self.dataset_parameters.n_frames(2), ...    % y location
                                                           self.images.CoMX(1:vec:end, 1:vec:end)'./vec, ... % u component
                                                           self.images.CoMY(1:vec:end, 1:vec:end)'./vec, ... % v component
                                                           1, ...                                           % scale
                                                           "Color", user_data.vector_color, ...
                                                           "LineWidth", 1.5, ...
                                                           "Tag", "VectorField");
            end

            % Function to plot color wheel
            function plot_colorwheel()
                % clear the axis
                cla(self.image_axes.ColorWheel)
                
                % Make ColorWheel for DPC/CoM imaging - this color
                % scheme will stay constant for all DPC/CoM images
                % regardless of their individual parameters like scan
                % or detector rotation for consistency
                width = 512; 
                r = width/2;
                
                [ygrid, xgrid] = meshgrid(1 - r : r);
                
                % Get atan() from -180 to 180
                colorwheel = atan2d(ygrid, xgrid);
                
                % shift the negative values of atan() up by 360
                self.images.ColorWheel = (colorwheel) .* (colorwheel >= 0) + ...
                                        (colorwheel + 360) .* (colorwheel < 0);

                % mask the color wheel to make it a circle
                self.images.ColorWheelMask = xgrid.^2 + ygrid.^2 < r^2;
                axis(self.image_axes.ColorWheel,[0, width+1, 0, width+1]);
                self.image_axes.ColorWheel.UserData.mask_opacity = 100;
            end
        end

        function status = is_different_to_previous(self, name, value)
            % Function to check whether the given name value is changed
            % compared to the previous value, and store the new value
            %
            % Parameters:
            %    self (Quant4D)
            %    name (str) : field name in self.previous_values
            %    value : value of self.previous_values.(name) to be tested for update
            %
            % Returns:
            %    status (bool) : Whether self.previous_values.(name) ~= value

            status = ~isfield(self.previous_values, name) || ...
                     ~isequal(self.previous_values.(name), value);
            if status
                self.previous_values.(name) = value;
            end
        end

        function to_update = to_update_image(self, event)
            % Function to determine whether to update images. Return
            % true if any: 1) `self.CalculationPolicy.Value` is 2
            % (active update) OR 2) `self.CalculationPolicy.Value` is 1
            % (reduced) and not when changing OR 3) is a manual update
            % (from update buttons or detector mode change)
            %
            % Parameters:
            %    self (Quant4D)
            %    event (event.EventData)
            %
            % Returns:
            %    to_update (bool) : Whether or not image(s) should be updated at the time of calling based on self.CalculationPolicy and current user interactions

            calc = self.CalculationPolicy.Value;
            to_update = calc == 2 || ...
                        (calc && is_static_event(self, event)) || ...
                        event.Source == self.UpdateImages || ...
                        event.Source == self.Mode;
        end

        function mock_UI_callbacks(self, source, value)
            % Function to mock UI callbacks.
            %
            % Parameters:
            %    self (Quant4D)
            %    source : UI elements
            %    value (str) : additional information to be passed along to further function calls
            %
            % Returns:
            %    None

            arguments
                self {mustBeA(self, "Quant4D")}
                source
                value {mustBeText} = "";
            end
            
            % Set value if passed in
            if ~strcmp(value, "")
                source.Value = value;
            end
            
            switch source
                case self.UpdateImages
                    % Update all images
                    update_images(self, struct("Source", source, "EventName", "ButtonPushed"))

                case self.DisplayImage
                    % Update Display UI or Select current image
                    display_callbacks(self, struct("Source", source, "EventName", "ValueChanged"))

                case self.SaveImagePrefix
                    % Update image saving prefix
                    save_callbacks(self, struct("Source", source, "EventName", "ValueChanged"))

                case {self.ShowDiffractionAxes, self.ShowRealAxes}
                    % Update axes annotations
                    axis_direction_callbacks(self, struct("Source", source,"EventName", "ButtonPushed"))

                case self.RealROIShape
                    % Update real-space controls
                    realspace_ROI_callbacks(self, struct("Source", source, "EventName", "ValueChanged"));

                case self.CustomDetectorTable
                    % Update Custom Detectors for Main Table selection change
                    custom_detector_callbacks(self, struct("Source", source,"EventName", "SelectionChanged"))

                case self.CustomDetectorDetailsTable
                    % Mock Custom Detector Detail Table edit to update ROI/images
                    custom_detector_callbacks(self,struct("Source", source, "EventName", "CellEdit"))

                case self.SaveTabGroup
                    % Mock changing Save/Export tabs in Save window
                    export_callbacks(self, struct("Source", source, "EventName", "SelectionChanged"))

                case self.ImportFileSelect
                    % Mock import file select button
                    import_select_file(self,struct("Source", source, "EventName", "ButtonPushed"));

                case self.ShowImportWindow
                    % Mock user clicking "Import" button on main UI
                    import_callbacks(self,struct("Source", source, "EventName", "ButtonPushed"));

                case self.Mode
                    % Mock detector mode changed
                    detector_mode_callbacks(self, struct("Source", source, "EventName", "ValueChanged"));

                case self.PreviewButton
                    % Mock "Import Preview" button
                    preview_callbacks(self, struct("Source", source,"EventName", "ButtonPushed"))

                case self.ShowSaveWindow
                    % Mock user clicking "Save" button on main UI
                    save_callbacks(self, struct("Source", source, "EventName", "ButtonPushed"));
            end
        end

        function selection = notification_dialog(self, icon, msg, title_name, option)
            % Wrapper for notification dialog; use `sprintf()` before calling this function to process "\n" in `message`
            %
            % Parameters:
            %    self (Quant4D)
            %    icon (str) : "quest", "list", "help", "warn", "error", "none", ""
            %    msg (str) : dialog message
            %    title_name (str) : dialog title
            %    option : dialog selection options
            %
            % Returns:
            %    selection (str | int) : user response

            arguments
                self; 
                icon {mustBeText, mustBeMember(icon,{"quest", "list", "help", "warn", "error", "none", ""})} = "";
                msg {mustBeText} = "";
                title_name {mustBeText} = "";
                option = ["OK", "Cancel"];
            end

            selection = "";
            
            % Set global default UI font size temporarily
            font_size = 9.5;
            default_font_size = get(0, 'DefaultUIControlFontSize');
            set(0, 'DefaultUIControlFontSize', font_size)
            beep

            switch icon
                case "quest"
                    % `questdlg()` will block all windows and background process
                    if numel(option) > 2
                        selection = questdlg(msg, ...
                                             title_name, ...
                                             option(1), ...
                                             option(2), ...
                                             option(3), ...
                                             option(1));
                    else
                        selection = questdlg(msg, ...
                                             title_name, ...
                                             option(1), ...
                                             option(2), ...
                                             option(1));
                    end
                
                case "list"
                    % `listdlg()` will block all windows and background process
                    selection = listdlg("ListString", option, ...
                                        "SelectionMode", "single", ...
                                        "PromptString", cellstr(split(msg,newline)), ...
                                        "Name", title_name, ...
                                        "ListSize", [300 150]);
                
                case {"help", "warn", "error", "none",""}
                    % The only way to set font size here is Tex; escape
                    % special characters in Tex; Tex is only used for font size
                    msg = "\fontsize{" + font_size + "}" + regexprep(msg, "([\\^_{}])", "\\$1");

                    % Disable windows because `msgbox()` cannot block `uifigure()` windows
                    enable_windows(self,false)
                    f = msgbox(msg, ...
                               title_name, ...
                               icon, ...
                               struct('WindowStyle','modal','Interpreter','tex'));

                    % Enable windows when the notification is gone
                    f.DeleteFcn = {@(~,~) enable_windows(self,true)};

                    % ensure the message is brought to the front
                    figure(f)

                    % Block background process until `msgbox()` is gone
                    uiwait(f)
            end
            
            % Reset global default UI font size
            set(0, "DefaultUIControlFontSize", default_font_size)
        end

        function wait_bar = progress_dialog(self, msg, title_name, interruptible)
            % Wrapper for `waitbar`
            %
            % Parameters:
            %    self (Quant4D)
            %    msg (str) : dialog message
            %    title_name (str) : dialog title
            %    interruptible (bool) : can the dialog be interrupted
            %
            % Returns:
            %    wait_bar (matlab.ui.Figure) – waitbar to display progress
            
            arguments
                self;
                msg {mustBeText} = "";
                title_name {mustBeText} = ""; 
                interruptible (1,1) {mustBeNumericOrLogical} = false;
            end

            % Disable all windows
            enable_windows(self,false)

            % Set mouse cursor to "busy"
            set(self.ui_groups.all_figures, "Pointer", "watch")

            if ~interruptible
                title_name = "(Uninterruptible) "+title_name;
            end

            wait_bar = waitbar(0, ...
                               msg, ...
                               "Name", title_name, ...
                               "WindowStyle", "modal");
            
            % For uninterruptible process:
            if ~interruptible
                % Indeterminate progress bar
                findall(wait_bar,"type","hgjavacomponent").JavaPeer.setIndeterminate(true);
                
                % Disable the close function
                wait_bar.CloseRequestFcn = [];
                
                % Enable windows and reset mouse pointer when the progress windows is gone
                wait_bar.DeleteFcn = @(~,~) enable_windows(self,true);
            end
        end

        function unload_data(self, swap_data)
            % Function to unload data and clean all images; swap_data
            % keeps all previous parameters and simply swaps out data
            %
            % Parameters:
            %    self (Quant4D)
            %    swap_data (bool) : swap dataset (true), unload all data (false)
            %
            % Returns:
            %    None

            arguments
                self
                swap_data (1,:) {mustBeNumericOrLogical} = false;
            end

            % Disable windows for the data unload process
            enable_windows(self,false)

            % reset main UI title
            self.Quant4D_Fig.Name = 'Quant4D';

            % Whether or not to swap dataset only, without changing
            % any existing parameters
            if ~swap_data
                % Clear all Axes
                arrayfun(@(x) cla(x), self.ui_groups.image_axes);
                cla(self.HistogramAxes);
                
                % Clear all parameters, data structures, etc. 
                self.common_parameters = []; 
                self.annotations = [];
                self.images = [];
                self.masks = [];
                self.image_displays = [];
                self.CustomDetectorTable.Data(:,:) = [];
            end

            % Remove all data from GPU if in use
            try
                if self.dataset_parameters.gpu > 0
                    reset(parallel.gpu.GPUDevice.getDevice(self.dataset_parameters.gpu));
                    gpuDevice([]);
                end
            catch
            end

            % Clear data, parameters and Axes
            self.data = [];
            self.memfile = [];
            self.dataset_parameters = [];
            self.previous_values = [];
        end

        function enable_windows(self, state)
            % Function to enable/disable windows/UI; disable is only
            % for notification/progress bar/busy background, etc.
            %
            % Parameters:
            %    self (Quant4D)
            %    state (bool) : enable (true) or disable (false) all windows
            %
            % Returns:
            %    None
            
            arguments
                self
                state (1,1) {mustBeNumericOrLogical} = true;
            end

            % Preview mode or not
            preview_mode = self.Mode.Value == "Preview";

            % Detector Mode UI, keep disabled in Import Preview Mode unless a dataset is loaded
            set(self.ModeGrid.Children, ...
                "Enable", ...
                switch_on_off(self, state && (~preview_mode || ~isempty(self.dataset_parameters))))

            % Real-space ROI controls, keep disabled in Import Preview Mode
            set(self.RealPanel, "Enable",switch_on_off(self, state && ~preview_mode))

            % Other UIs can be enabled in Import Preview Mode
            set([self.ShortcutButtonGrid.Children; ...
                 self.ModePanel; ...
                 self.SettingsPanel; ...
                 self.SavePanel; ...
                 self.ImportPanel], ...
                "Enable", ...
                switch_on_off(self, state))

            % Disable all images when not "on"; visible means disable
            set(self.ui_groups.image_grayout, "Visible", ~state)
            
            % Also reset all windows' mouse pointer when enabling UIs
            if state
                set(self.ui_groups.all_figures,'Pointer','arrow');
            end
        end

        function create_other_windows(self)
            % Function to create other UI windows and Image figures
            %
            % Parameters:
            %    self (Quant4D)
            %
            % Returns:
            %    None
            
            debug_time = tic;

            % Set window position without using `movegui()`, to avoid its implicit `drawnow`
            title_height = self.sys_constants.title_height;
            decor_width = self.sys_constants.decor_width;
            
            % Available sizes of width/height/left/bottom/right/top
            screen_width = self.sys_constants.screen_avail(3);
            screen_height = self.sys_constants.screen_avail(4);
            screen_left = self.sys_constants.screen_avail(1)+decor_width/2;
            screen_bottom = self.sys_constants.screen_avail(2);
            screen_right = screen_left+screen_width-decor_width;
            screen_top = screen_bottom+screen_height-title_height; % top excluding title bar
            horizontal_center = (screen_left+screen_right)/2;
            vertical_center = (screen_bottom+screen_top)/2;
            image_size = self.Quant4D_Fig.Position(4);

            % Create other UI Windows
            self.figures.Settings = move_UI_to_new_figure('Settings', self.SettingsPanel);
            self.figures.Import = move_UI_to_new_figure('Import Data', self.ImportPanel);
            self.figures.Import.Position(1:2) = ([horizontal_center vertical_center]-self.figures.Import.Position(3:4)/2); % Move to center
            
            % Set `self.Fig.Import` window close as "pushing `self.CancelImport"
            self.figures.Import.CloseRequestFcn = @(~,~)import_callbacks(self, struct("Source", self.CancelImport, "EventName",'ButtonPushed'));
            
            % Move to Save UI to the center
            self.figures.Save = move_UI_to_new_figure('Save/Export', self.SavePanel);
            self.figures.Save.Position(1:2) = ([horizontal_center vertical_center] - self.figures.Save.Position(3:4))/2;
            
            % Set `self.Fig.Save` window close as "pushing `self.SaveCloseButton`"
            self.figures.Save.CloseRequestFcn = @(~,~)export_callbacks(self, struct("Source", self.SaveCloseButton, "EventName",'ButtonPushed'));
            
            % Set main windows `self.Quant4D_Fig` other properties and move to top left
            self.Quant4D_Fig.Position(1:2) = [1, self.sys_constants.screen_size(4) - self.Quant4D_Fig.Position(4) - self.sys_constants.title_height];
            self.Quant4D_Fig.SizeChangedFcn = [];
            self.Quant4D_Fig.KeyPressFcn = @key_press;

            % When delete the main window `self.Quant4D_Fig` (e.g. closing), also delete other windows
            self.Quant4D_Fig.DeleteFcn = {@(~,~,figs) delete(figs), structfun(@(x) x, self.figures)};

            % Move Settings UI next to main window
            self.figures.Settings.Position(1:2) = [sum(self.Quant4D_Fig.Position([1,3]))+1, self.Quant4D_Fig.Position(2)];

            % Set limits/values for image window resize options in settings window
            set([self.SetDiffractionWindowWidth, ...
                 self.SetDiffractionWindowHeight, ...
                 self.SetRealWindowWidth, ...
                 self.SetRealWindowHeight], ...
                {"Limits"}, ...
                {[1 screen_width]; ...
                 [1 screen_height]; ...
                 [1 screen_width]; ...
                 [1 screen_height]}, ...
                "Value", ...
                image_size)

            % Create Image Windows with inputs:
            %   id
            %   title
            %   space (Diffraction/Real/ColorWheel/Preview)
            %   type (Primary/Mask/CoM/Test/Preview)
            %   colormap
            %   position/size

            create_axes_figure("ColorWheel",...
                               "Color Wheel for Phase Direction", ...
                               "ColorWheel", ...
                               "CoM", ...
                               "hsv", ...
                               [horizontal_center 1 200 200]);
            axtoolbar(self.image_axes.ColorWheel, {"datacursor"});

            create_axes_figure("Diffraction", ...
                               "Diffraction", ...
                               "Diffraction", ...
                               "Primary", ...
                               "gray", ...
                               [sum(self.figures.Settings.Position([1,3]))+1 self.Quant4D_Fig.Position(2) image_size image_size]); % next to Settings UI
                              %[horizontal_center-image_size/2 screen_top-image_size image_size image_size]); % Top-center
                              
             % add dropdown to diffraction figure to control how
             % patterns are combined (sum, mean, max, std)
             self.diffraction_dropdown.Parent = self.figures.Diffraction;
             self.diffraction_dropdown.ValueChangedFcn = @self.move_real_ROI;
             self.diffraction_dropdown.Position = [0, self.figures.Diffraction.Position(4) - self.diffraction_dropdown.Position(4), 65, 22];

            create_axes_figure("DiffractionMask", ...
                               "Diffraction Mask", ...
                               "Diffraction", ...
                               "Mask", ...
                               "gray", ...
                               [sum(self.figures.Settings.Position([1,3]))+1 1 image_size image_size]); % Below Diffraction
                               %[horizontal_center-image_size/2 1 image_size image_size]); % Bottom-center

            % Diffraction preview image for import
            create_axes_figure("Preview", ...
                               "Preview", ...
                               "Preview", ...
                               "Preview", ...
                               "gray", ...
                               self.figures.Diffraction.Position);
            
            % Place Real-space images on the right, from top to bottom
            image_left = sum(self.figures.Diffraction.Position([1,3]))+1;
            image_bottom = self.Quant4D_Fig.Position(2);
            image_bottom_offset = image_bottom/8;
            
            ids = ["Real"; "CoMPhMag"; "CoMPh"; "CoMMag"; "CoMX"; "CoMY"; "dCoM"; "iCoM"; "RealMask"];
            titles = ["Real-space"; "CoM Phase (Magnitude-shaded)"; "CoM Phase"; "CoM Magnitude"; "CoM X"; "CoM Y"; "dCoM"; "iCoM"; "Real-space Mask"];
            space = "Real";
            types = ["Primary"; "CoM"; "CoM"; "CoM"; "CoM"; "CoM"; "CoM"; "CoM"; "Mask"];
            cmaps = ["gray"; "hsv"; "hsv"; "gray"; "gray"; "gray"; "gray"; "gray"; "gray"];
            position = [image_left, image_bottom, image_size, image_size];
            
            % Real-space image figures
            for i_figure = 1:numel(ids)
                create_axes_figure(ids(i_figure), ...
                                   titles(i_figure), ...
                                   space, ...
                                   types(i_figure), ...
                                   cmaps(i_figure), ...
                                   position);
                position = position - [0 image_bottom_offset 0 0];
            end

            % Debugging figures
            if self.debug
                create_axes_figure("tDiffraction",...
                                   "Test Diffraction", ...
                                   "Diffraction", ...
                                   "Test", ...
                                   "gray", ...
                                   [horizontal_center - image_size/2, 1, image_size, image_size]); % Bottom-center
                
                create_axes_figure("tReal", ...
                                   "Test BF/DF", ...
                                   "Real", ...
                                   "Test", ...
                                   "gray", ...
                                   [image_left, image_bottom, image_size, image_size]);
            end

            % Variable names, image names and image types (tag) for all patterns'/images' figures/axes/images
            self.ui_groups.image_id = string(fieldnames(self.image_axes));                            % ID/fieldnames under `self.image_axes` `self.figures` `self.images` `self.image_dispays` etc
            self.ui_groups.image_space = string(structfun(@(x) x.UserData.space, self.image_axes));   % Spaces ("Real"/"Diffraction")
            self.ui_groups.image_type = string(structfun(@(x) x.UserData.type, self.image_axes));     % Types ("Primary", "CoM" related, "Mask", "Test")
            self.ui_groups.image_name = string(structfun(@(x) x.UserData.name, self.image_axes));     % Names/Titles
            
            % AND their Axes/Figure objects, as well as the gray overlay to disable them
            self.ui_groups.image_axes = arrayfun(@(x) self.image_axes.(x), self.ui_groups.image_id);
            self.ui_groups.image_figures = arrayfun(@(x) self.figures.(x), self.ui_groups.image_id);
            self.ui_groups.image_grayout = arrayfun(@(x) self.figures.(x).UserData.grayout, self.ui_groups.image_id); % Set them visible to disable the axes
            
            % Variable names for all diffraction-sized figures/axes/images AND THEN their Axes objects
            self.ui_groups.diffraction_id = self.ui_groups.image_id(self.ui_groups.image_space == "Diffraction");
            self.ui_groups.diffraction_axes = arrayfun(@(x) self.image_axes.(x), self.ui_groups.diffraction_id);
            
            % Variable names for all real-space-sized figures/axes/images AND THEN their Axes objects
            self.ui_groups.real_id = self.ui_groups.image_id(self.ui_groups.image_space == "Real");
            self.ui_groups.real_axes = arrayfun(@(x) self.image_axes.(x), self.ui_groups.real_id);
            
            % Group all "Show ... Window" buttons related to CoM/DPC
            self.ui_groups.CoM_buttons = [findobj(self.ShowImageWindowsGrid,'-regexp', "Tag",'CoM'); ...
                                         self.ShowColorWheelWindow; ...
                                         self.ShowColorWheelWindow2];
            
            % Group all diffraction detector panels
            self.ui_groups.detector_ui = [self.PreviewGrid; ...
                                         self.AlignmentGrid; ...
                                         self.AnnularDetectorGrid; ...
                                         self.VirtualApertureGrid; ...
                                         self.CustomDetectorGrid];

            % Transfer all detector panels to main window, then delete their old container
            set(flip(self.ui_groups.detector_ui), 'Parent', self.ModePanel);
            delete(self.ModeTabGroup)
            
            % Group all window `figure` `uifigure`
            self.ui_groups.all_figures = [self.Quant4D_Fig; structfun(@(f) f, self.figures)];

            debug_toc(self, [], "", debug_time)


            %%% Sub functions of `otherFigures()`
            % Keyboard shortcuts
            function key_press(~, event)
                debug_time = tic;
                switch event.Key
                    case 'f5'
                        % update with the F5 key
                        if self.UpdateImages.Enable
                            mock_UI_callbacks(self, self.UpdateImages);
                        end
                    case {'o', 'O'}
                        if ismember('control',event.Modifier)
                            mock_UI_callbacks(self, self.ShowImportWindow)
                        end
                    case {'s', 'S'}
                        if ismember('control',event.Modifier)
                            mock_UI_callbacks(self, self.ShowSaveWindow)
                        end
                end
                debug_toc(self, event, "", debug_time)
            end

            % Hide window instead of closing it
            function hide_window(source, ~)
                if isvalid(self)
                    source.Visible = "off";
                else
                    delete(source);
                end
            end

            % Transplant `UI` from its parent to a new separated Figure `ui_figure`
            function ui_figure = move_UI_to_new_figure(name, ui)
                ui_figure = uifigure("Name", name, ...
                                     "Visible", "off", ...
                                     "Position", [1 1 ui.Position(3:4)+2], ...
                                     "AutoResizeChildren", "off", ...
                                     "CloseRequestFcn", @hide_window, ...
                                     "Resize", "off", ...
                                     "KeyPressFcn", @key_press);

                grid_layout = uigridlayout(ui_figure,[1 1],'Padding',[0 0 0 0]);
                ui.Parent = grid_layout;
            end

            % Create Image Window/Axes
            function create_axes_figure(id, name, space, ax_type, color_map, position)
                fig = uifigure("Visible", "off", ...
                               "Name", name, ...
                               "Position", position, ...
                               "MenuBar", "none", ...
                               "NumberTitle", "off", ...
                               "IntegerHandle", "off", ...
                               "Color", self.sys_constants.background_color, ...
                               "WindowButtonDownFcn", @clicked_window, ...
                               "WindowScrollWheelFcn", @scroll_figure, ...
                               "CloseRequestFcn", @hide_window, ...
                               "KeyPressFcn", @key_press, ...
                               "AutoResizeChildren", 'off', ...
                               "SizeChangedFcn", @resize_figure, ...
                               "Tag", space + " " + ax_type);

                % allow for custom axes toolbar
                enableLegacyExplorationModes(fig)

                % An overlay on figure to cover axes; disables the axes when visible
                grayout = annotation(fig, ...
                                     "rectangle", [0 0 1 1], ...
                                     "Visible", "off", ...
                                     "FaceColor", [0.96 0.96 0.96], ...
                                     "FaceAlpha", 0.7);

                % Not `Clipping` axes to let images expand beyond the axes when zooming in
                ax = axes(fig, ...
                          "Color", "k", ...
                          "Colormap", feval(color_map), ...
                          "CLimMode", "manual", ...
                          "Units", "normalized", ...
                          "Position", [0 0 1 1], ...
                          "DataAspectRatio", [1 1 1], ...
                          "XTick", [], ...
                          "YTick", [], ...
                          "XColor", "k", ...
                          "YColor", "k", ...
                          "Box", 1, ...
                          "Clipping", 0, ...
                          "NextPlot", "add", ...
                          "Interactions", [], ...
                          "Tag", space + " " + ax_type);
                
                % Toolbar & its `restoreview()`
                tool_bar = axtoolbar(ax, {"export", "datacursor", "pan", "zoomin", "zoomout", "restoreview"});
                tool_bar.Children(end).ButtonPushedFcn = @restore_view;
                
                % Data Tips
                cursor_mode = datacursormode(fig);
                cursor_mode.UpdateFcn = @show_value;
                set(cursor_mode.UIContextMenu.Children,"Visible", "off")
                
                % Image properties
                if color_map == "gray"
                    vector_color = "r";
                else
                    vector_color = "w";
                end

                ax.UserData = struct("id", id, ...
                                     "name", name, ...
                                     "space", space, ...
                                     "type", ax_type, ...
                                     "colormap", color_map, ...
                                     "invert", false, ...
                                     "mask_opacity", 0, ...
                                     "brightness", 50,...
                                     "contrast", 50,...
                                     "gamma", 1,...
                                     "vector_field", false,...
                                     "vector_color", vector_color);

                fig.UserData = struct("id", id, ...
                                      "name", name, ...
                                      "space", space, ...
                                      "type", ax_type, ...
                                      "grayout", grayout);

                % add references to fig and ax to their respective lists
                self.figures.(id) = fig;
                self.image_axes.(id) = ax;

                %% Sub sub functions
                % "restoreview" goes back to the limits of the actual image, nothing more/less.
                function restore_view(~, event)
                    axis(event.Axes, self.common_parameters.(lower(event.Axes.UserData.space)+"_axes_limit"))
                    event.Axes.Position = [0 0 1 1];
                    self.diffraction_dropdown.Position = [0, self.figures.Diffraction.Position(4) - self.diffraction_dropdown.Position(4), 65, 22];
                end

                % Modify Data Tips to show the raw value from `self.images.(...)`
                function data_tip = show_value(~, event)
                    x = event.Position(1);
                    y = event.Position(2);
                    value = strtrim(sprintf('%14.7g',self.images.(event.Target.Parent.UserData.id)(x,y)));
                    data_tip = sprintf('Value: \\bf%s\n\\rmX: \\bf%g\\rm, Y: \\bf%g', value, x, y);
                end

                % Select image in Display/contrast panel unless DisplayLock
                % is selected, which leaves the selected window fixed,
                % which is especially useful for watching image statistics
                % change as a detector or ROI moves
                function clicked_window(source, ~)
                    id = string(source.UserData.id);
                    if ~self.DisplayLock.Value && self.DisplayImage.Value ~= id && ismember(id, self.DisplayImage.ItemsData)
                        mock_UI_callbacks(self, self.DisplayImage, id)
                    end
                end

                % ensure that the diffraction dropdown stays pinned to the
                % upper left corner of the diffraction figure/axis during
                % resizing
                function resize_figure(source, ~)
                    if source == self.figures.Diffraction
                        self.diffraction_dropdown.Position = [0, self.figures.Diffraction.Position(4) - self.diffraction_dropdown.Position(4), 65, 22];
                    end
                end

                % function to allow the user to zoom via the mouse scroll
                % wheel without having to click the zoom in/out icons on
                % the axes toolbar; all axes in a given space are linked,
                % so this will carry across to all axes in that space
                function scroll_figure(source,event)
                    zoom_ax = source.CurrentAxes;
                    % zoom in/out by 10% (5% on either side) with each
                    % mouse wheel scroll; VerticalScorrlCount == -1 for an
                    % upward scroll and == 1 for a downward scroll
                    zoom_amount = 0.05*[-1 1]*event.VerticalScrollCount;
                    zoom_ax.XLim = zoom_ax.XLim + range(zoom_ax.XLim)*zoom_amount;
                    zoom_ax.YLim = zoom_ax.YLim + range(zoom_ax.YLim)*zoom_amount;

                    % get axis limits for the given space
                    if contains(source.Tag, "Real")
                        lim = self.common_parameters.real_axes_limit;
                    elseif contains(source.Tag, "Diffraction")
                        lim = self.common_parameters.diffraction_axes_limit;
                    end

                    % make sure we don't zoom out too far
                    zoom_ax.XLim = clip(zoom_ax.XLim, lim(1), lim(2));
                    zoom_ax.YLim = clip(zoom_ax.YLim, lim(3), lim(4));
                end
            end
        end

        function selection = check_NaN(self, image, preview)
            % Function to check NaN/Inf in data/image
            %
            % Parameters:
            %    self (Quant4D)
            %    image (array) : image to be checked for the presence of NaNs
            %    preview (bool) : 
            %
            % Returns:
            %    selection

            arguments
                self
                image {mustBeNumericOrLogical} = 0;
                preview (1,1) {mustBeNumericOrLogical} = true;
            end
            
            selection="";
            if any(isnan(image), "all") || any(isinf(image), "all")
                title_text = 'NaN/Inf in Data!';
                message = "There are NaN/Inf values in the data! Which may " + ...
                          "indicate the data structure is not correctly set " + ...
                          "(e.g. wrong Data Type, Byte Order, Data Offset, " + ...
                          "Frame Header/Footer, etc).\n\nIf any data are " + ...
                          "corrupt, NaNs can be set to 0.";

                % For preview only
                if preview
                    selection = notification_dialog(self, ...
                                                    'quest', ...
                                                    sprintf(message), ...
                                                    title_text, ...
                                                    ["Continue", "Set NaNs to 0"]);

                elseif self.dataset_parameters.pixel_binning > 1 || (self.dataset_parameters.frame_footer + self.dataset_parameters.frame_header) > 0
                    selection = notification_dialog(self, ...
                                                    'quest', ...
                                                    sprintf(message+"\n\nRe-importing with corrected configuration is suggested."), ...
                                                    title_text, ...
                                                    ["Continue", "Set NaNs to 0"]);
                
                else
                    selection = notification_dialog(self, ...
                                                    'quest', ...
                                                    sprintf(message+"\n\nDo you want to swap the byte-order?"), ...
                                                    title_text, ...
                                                    ["Yes, try to swap the byte-order", "No"]);
                    
                    % Select the Data Info tab and bring Settings to the front
                    self.SettingsTabGroup.SelectedTab = self.InfoTab;
                    figure(self.Quant4D_Fig)
                    figure(self.figures.Settings) 
                    
                    % Execute the swap byte order callbacks
                    if startsWith(selection, "Yes")
                        dataset_options_callbacks(self,struct("Source",self.SwapByteOrder,"EventName", "ButtonPushed"))
                    end
                end
            end
        end

        % Function to check the size of various screen attributes
        function get_screen_info(self)
            % Get main screen size (MATLAB "pixels")
            self.sys_constants.screen_size = get(0, 'ScreenSize');

            % Get all monitor position/size
            self.sys_constants.monitor_positions = get(0,'MonitorPositions');
            
            % Scale for MATLAB "pixels" vs actual pixels, for high DPI
            self.sys_constants.screen_pixel_scale = self.sys_constants.screen_size(4)/java.awt.Toolkit.getDefaultToolkit.getScreenSize.height;
            
            % A Java window to measure window decorations like "title bar"/"border width"
            jf = javax.swing.JFrame('Test');
            jf.setDefaultCloseOperation(javax.swing.JFrame.DISPOSE_ON_CLOSE);
            jf.pack();
            insets = jf.getInsets();   % Not accurate for Windows OS, due to the transparent shadow
            self.sys_constants.title_height = insets.top*self.sys_constants.screen_pixel_scale;
            self.sys_constants.decor_height = self.sys_constants.title_height + insets.bottom*self.sys_constants.screen_pixel_scale;
            self.sys_constants.decor_width = (insets.left + insets.right)*self.sys_constants.screen_pixel_scale;
            jf.dispose()
            
            % Actual available main screen size excluding taskbar etc
            insets = java.awt.Toolkit.getDefaultToolkit().getScreenInsets(getGraphicsConfiguration(javax.swing.JFrame));
            insets = [insets.left, insets.bottom, insets.right+insets.left, insets.top+insets.bottom] * self.sys_constants.screen_pixel_scale;
            self.sys_constants.screen_avail = [insets(1:2)+1, self.sys_constants.screen_size(3:4)-insets(3:4)];
        end

        % Function to get/set system constants 
        function get_sys_constants(self)
            % Default self background color
            self.sys_constants.background_color = self.Quant4D_Fig.Color;

            % highlight state buttons when enabled
            self.sys_constants.highlight_color = [0.702, 1.00, 0.702];
            
            % Warning color
            self.sys_constants.warning_color = [1.00, 0.65, 0.00];
            
            % Get native endianness
            [~,~,endian] = computer();
            self.sys_constants.system_endianness = lower(endian);
            self.sys_constants.endian_text = struct("l",'Little Endian',"b",'Big Endian');
        end

        % Function to save vector field images
        function save_vector_field(self)
                % Create temporary figure with axes
                fig = figure("Visible", "on");
                ax = axes(fig);
                ax.NextPlot = "replace";
                imagesc(ax, self.images.CoMPh, "AlphaData", self.images.CoMMagNorm);
                set(ax, ...
                    "DataAspectRatio", [1 1 1], ...
                    "XTick", [], ...
                    "YTick", [], ...
                    "YDir", "reverse", ...
                    "Color", "k");
                axis(ax, self.common_parameters.real_axes_limit);
                colormap(ax, hsv);

                % get the vector field sampling (1:1, 1:2, etc)
                vec = self.image_axes.CoMPhMag.UserData.vector_field;

                set(ax, "NextPlot", "add");
                quiver(ax, ...
                       1:vec:self.dataset_parameters.n_frames(1),...
                       1:vec:self.dataset_parameters.n_frames(2),...
                       -self.images.CoMX(1:vec:end,1:vec:end)./vec,...
                       -self.images.CoMY(1:vec:end,1:vec:end)./vec,...
                       1/vec,"w");
                set(ax, ...
                    "DataAspectRatio", [1 1 1], ...
                    "XTick", [], ...
                    "YTick", [], ...
                    "YDir", "reverse", ...
                    "NextPlot", "replace");
                axis(ax, self.common_parameters.real_axes_limit);

                % Save as a .png, .fig, and .pdf (vector image, not pixelated)
                %fig.InvertHardcopy = "off";
                exportgraphics(fig,strcat(self.SaveImagePrefix.Value, "VectField.png"), "Resolution", 1000, "BackgroundColor", "k");
                saveas(fig,strcat(self.SaveImagePrefix.Value, "VectField.fig"));
                exportgraphics(fig,"VectField_vector.pdf", 'ContentType', 'vector', "BackgroundColor","K")
                fig.Visible = "off";

                % write vector field to a comma-separated text file
                writematrix([-self.images.CoMX(1:vec:end,1:vec:end)./vec ...
                             -self.images.CoMY(1:vec:end,1:vec:end)./vec], ...
                             strcat(self.SaveImagePrefix.Value, "vector_field.txt"));
                
                close(fig);
        end

        % Function to delete plotted detectors if they exist
        function clear_detectors(self)
            % Transmitted Beam alignment
            delete(findobj(self.image_axes.Diffraction, "Tag","TransBeamAnnot"))

            % Annular/Round detectors and Segmented detectors
            delete(findobj(self.image_axes.Diffraction, '-regexp', "Tag", "AnnDetrAnnot"))
            delete(findobj(self.image_axes.Diffraction, "Tag", "SegDetrAnnot"))

            % Virtual apertures
            delete(findobj(self.image_axes.Diffraction, "Tag", "VrApertAnnot"))

            % Custom detectors - hide Custom ROIs only
            set(findobj(self.image_axes.Diffraction.Children, '-regexp', "Tag", "Custom "), "Visible", false);

            % Scan direction alignment
            delete(findobj(self.image_axes.Diffraction, "Tag", "ScanDirAnnot"))
        end

        % Function to draw Real-space ROI of various shapes on real space image(s)
        function draw_real_ROI(self, event, roi_type)
            % Delete all previous ROIs
            delete(findobj(self.ui_groups.real_axes, "Tag",'Real-space ROI'))

            % set roi polygon color
            color = [1 0.5 0.5];

            % Special case for drawing polygon ROI
            if roi_type == "poly"
                % List for available real-space images
                real_sace_images = self.ui_groups.image_space == "Real" & ...
                                   self.ui_groups.image_type ~= "Mask" & ...
                                   ismember(self.ui_groups.image_id,self.DisplayImage.ItemsData);

                selection = notification_dialog(self, ...
                                          'list', ...
                                          sprintf("Select a Real-space Image to draw a polygon ROI.\n\n" + ...
                                            "Press 'Esc' to cancel during drawing. Please refer to MATLAB's 'drawpolygon' for more tips.\n"), ...
                                          "Draw Polygon ROI", ...
                                          self.ui_groups.image_name(real_sace_images));
                
                % Revert to "full" is canceled
                if isempty(selection)
                    mock_UI_callbacks(self, self.RealROIShape, "full");
                    return;
                end
                
                % Bring selected image window to front
                options = self.ui_groups.image_id(real_sace_images);
                selection_index = options(selection);
                ax = self.image_axes.(selection_index);
                figure(self.figures.(selection_index))
                
                % Disable UIs until drawing finishes
                enable_windows(self, false)
                
                % Enable the selected image only
                self.figures.(selection_index).UserData.grayout.Visible = "off";
                
                % Draw temporary polygon for positions
                tmp_polygon = drawpolygon(ax, "Color", color);
                polygon_position = tmp_polygon.Position;
                delete(tmp_polygon)

                % Re-enable all windows
                enable_windows(self,true)
                
                % Revert to "full" is canceled
                if isempty(polygon_position)
                    mock_UI_callbacks(self, self.RealROIShape, "full");
                    return;
                end
            end
            
            % Draw ROIs on Real-space images, except the mask image
            real_space_limits = range([self.image_axes.Real.XLim; self.image_axes.Real.YLim]'); 
            pos = [self.RealROIFrameX.Value self.RealROIFrameY.Value];

            for selection_index = self.ui_groups.image_id(self.ui_groups.image_space == "Real" & self.ui_groups.image_type ~= "Mask")'
                switch roi_type
                    case "full"
                        roi = drawrectangle(self.image_axes.(selection_index), ...
                                            "Position", [1 1 real_space_limits], ...
                                            "Visible", 0, ...
                                            "EdgeAlpha", 0, ...
                                            "FaceAlpha", 0);
                    
                    case 'point'
                        roi = drawpoint(self.image_axes.(selection_index), ...
                                        "Position",pos);
                    
                    case 'ellipse'
                        roi = drawellipse(self.image_axes.(selection_index), ...
                                          "Center", pos, ...
                                          "SemiAxes", min(0.1*real_space_limits)*[1 1], ...
                                          "FaceAlpha", 0);
                    
                    case 'rectangle'
                        roi = drawrectangle(self.image_axes.(selection_index), ...
                                            "Position", [pos-0.1*real_space_limits, 0.2*real_space_limits], ...
                                            "Rotatable", true, ...
                                            "FaceAlpha",0);
                    
                    case 'poly'
                        roi = drawpolygon(self.image_axes.(selection_index), ...
                                          "Position", polygon_position, ...
                                          "FaceAlpha", 0);
                    
                    case "file"
                        roi = drawrectangle(self.image_axes.(selection_index), ...
                                            "Position", [1 1 real_space_limits], ...
                                            "Visible", 0, ...
                                            "EdgeAlpha", 0, ...
                                            "FaceAlpha",0);
                        bw = visboundaries(self.image_axes.(selection_index), ...
                                           bwboundaries(self.images.RealROIFile'), ...
                                           "Color",color, ...
                                           "EnhanceVisibility",0);
                        bw.Tag = 'Real-space ROI';
                end

                set(roi, ...
                    "Deletable", false, ...
                    "Color", color, ...
                    "Tag", "Real-space ROI");

                roi.UserData.Move = addlistener(roi, "MovingROI", @self.move_real_ROI);
                addlistener(roi, "ROIMoved", @self.move_real_ROI);
                self.annotations.RealROI.(selection_index) = roi;
            end

            move_real_ROI(self, self.annotations.RealROI.Real, event)
        end

        % Function to move Real-space ROIs on real space image(s)
        function move_real_ROI(self, source, event)
            debug_time = tic;
            
            % Update panel values for individual probe positions
            roi = self.annotations.RealROI.Real;
            x = self.RealROIFrameX.Value;
            y = self.RealROIFrameY.Value;
            
            switch source
                case self.RealROIFrameX
                    % Force X >= 1
                    x = max(1, event.Value);
                
                case self.RealROIFrameY
                    % Force Y >= 1
                    y = max(1, event.Value);

                case self.diffraction_dropdown
                
                otherwise % E.g. ROIs
                    roi = source;
                    switch self.RealROIShape.Value
                        case {'rectangle', 'full', 'file'}
                            position = source.Position(1:2) + source.Position(3:4)/2;
                            x = position(1);
                            y = position(2);
                        case 'point'
                            x = source.Position(1);
                            y = source.Position(2);
                        case 'ellipse'
                            x = source.Center(1);
                            y = source.Center(2);
                        case 'poly'
                            % avoid any warnings that arise when:
                            % 'Polyshape has duplicate vertices,
                            % intersections, or other inconsistencies
                            % that may produce inaccurate or unexpected
                            % results. Input data has been modified to
                            % create a well-defined polyshape.'
                            warning('off','MATLAB:polyshape:repairedBySimplify');
                            [x, y] = centroid(polyshape(source.Position));
                    end
            end

            x = round(x);
            y = round(y);

            % Set current ROI position if called from `self.RealROIFrameX` or `self.RealROIFrameY`, and it's a point ROI
            if ismember(source, [self.RealROIFrameX, self.RealROIFrameY]) && self.RealROIShape.Value == "point"
                roi.Position = [x y];
            end
            
            % Update UI
            set_external_source(self, event,[self.RealROIFrameX, self.RealROIFrameY],{"Value"},{x;y})
            
            % Only update ROIs on other visible figures; update all when not in "changing" Event
            roi_struct = structfun(@(i) i, self.annotations.RealROI);
            roi_struct = roi_struct(arrayfun(@(i) ancestor(i,'figure').Visible, roi_struct) | is_static_event(self, event));
            
            % Sync existing properties of positions etc.
            for prop = ["Position" "Center" "SemiAxes" "RotationAngle"]
                if isprop(roi, prop)
                    set_external_source(self, event, roi_struct, prop, roi.(prop));
                end
            end

            % Update images
            if to_update_image(self, event)
                % generate a mask for displaying diffraction pattern
                switch self.RealROIShape.Value
                    case "full"
                        mask_real = true(self.dataset_parameters.n_frames);
                    
                    case 'point'
                        mask_real = false(self.dataset_parameters.n_frames);
                        mask_real(x, y) = true;
                    
                    case 'file'
                        mask_real = self.images.RealROIFile;
                    
                    otherwise
                        mask_real = createMask(self.annotations.RealROI.Real, self.image_displays.Real)';
                end

                % Convert to single/double
                mask_real = cast(mask_real,self.dataset_parameters.data_type);

                % Invert mask?
                if self.RealROIInvert.Value
                    mask_real = max(mask_real,[], "all") - mask_real;
                end

                % Store the mask for plotting/saving
                self.images.RealMask = mask_real;
                self.masks.real = mask_real;

                % Update diffraction pattern for the specified ROI; special
                % case to speed up `point` as it does not require the
                % entire dataset to be multiplied
                if strcmp(self.RealROIShape.Value, "point")
                    self.images.Diffraction = gather(reshape(self.data(:,mask_real==1), self.dataset_parameters.n_pixels));
                else
                    switch self.diffraction_dropdown.Value
                        case 'max'
                            self.images.Diffraction = gather(reshape(max(self.data.*reshape(mask_real, 1, []), [],2), self.dataset_parameters.n_pixels));

                        case 'std'
                            self.images.Diffraction = gather(reshape(std(self.data.*reshape(mask_real, 1, []), [],2), self.dataset_parameters.n_pixels));

                        otherwise % sum, mean, sqrt, ln, log10
                            self.images.Diffraction = gather(reshape(self.data*reshape(mask_real, [], 1), self.dataset_parameters.n_pixels));
                    end
                end
                
                % add operation on top of summed data
                switch self.diffraction_dropdown.Value
                    case 'mean'
                        self.images.Diffraction = self.images.Diffraction / sum(mask_real, "all");

                    case 'sqrt'
                        self.images.Diffraction = real(sqrt(self.images.Diffraction));
                    
                    case 'ln'
                        self.images.Diffraction = clip(real(log(self.images.Diffraction)),0,Inf);
                    
                    case 'log10'
                        self.images.Diffraction = clip(real(log10(self.images.Diffraction)),0,Inf);
                end

                plot_all_patterns(self, event)
            end

            debug_toc(self, event, "", debug_time)
        end

        function get_fields(self, tree_node, variable_struct)
            if ~isstruct(variable_struct)
                return
            end
            
            fnames = fieldnames(variable_struct);

            for i_field = 1:numel(fnames)
                field_name = fnames{i_field};

                item = variable_struct.(field_name);

                % recursively interrogate struct
                if isa(item,'struct')
                    % only add uitreenode if it doesn't already exists
                    parent = findobj(tree_node,'Text',field_name,'Type','uitreenode');
                    if isempty(parent) || ~isvalid(parent)
                        parent = uitreenode(tree_node, "Text", field_name);
                    end
                    get_fields(self, parent, item)
                end

                % only add uitreenode if it doesn't already exists
                h = findobj(tree_node,'Text',field_name,'Type','uitreenode');
                if isempty(h) || ~isvalid(h)
                    uitreenode(tree_node, "Text", field_name);
                end
            end
        end

    end


    % Callbacks that handle component events
    methods (Access = private)

        % Code that executes after component creation
        function startup_function(self, debug)
            % Code that executes after component creation
            %
            % Parameters:
            %    self (Quant4D)
            %    debug: Boolean to enable/disable debug timings
            %
            % Returns:
            %    Quant4D class encapsulating all UI components,
            %    parameters, and data 
            
            arguments
                self;
                debug (1,1) {mustBeNumericOrLogical} = false;
            end

            debug_time = tic;

            % Non-0 values if debugging
            self.debug = debug;

            % Hide until startup process is ready
            self.Quant4D_Fig.Visible = "off"; 

            % get/set system info
            get_screen_info(self)
            get_sys_constants(self)
            get_memory(self);
            get_GPU(self);

            % Disable histogram interactions
            self.HistogramAxes.Interactions = [];
            
            % Setup "Custom Detector" tables
            set(self.CustomDetectorTable, ...
                'SelectionType','row', ...
                'Multiselect',0, ...
                'Data',table('Size',[0 6], ...
                             'VariableTypes',{'string','string','string','logical','logical','double'}, ...
                             'VariableNames',{'ID','Type','Label', 'Enable','Show','Weight'}));
            self.CustomDetectorDetailsTable.ColumnFormat = {'bank','bank','bank'};
            
            % Create Other Panel and Image Windows
            create_other_windows(self)

            % Keep UIs disabled
            enable_windows(self,false)

            % Reset self UI and data, which enters Import Preview Mode
            reset_Quant4D(self, struct("Source", "startup_function", "EventName",[]))

            % make main self UI visible
            self.Quant4D_Fig.Visible = "on";

            % Plot axes display directions
            mock_UI_callbacks(self, self.ShowDiffractionAxes);
            mock_UI_callbacks(self, self.ShowRealAxes)
            
            % Link Axes limits for zooming, `drawnow` implied
            linkaxes(self.ui_groups.real_axes);
            linkaxes(self.ui_groups.diffraction_axes);

            % populate variable viewer 
            variable_viewer(self, struct())

            debug_toc(self, [], "`startup_function` finished", debug_time)
        end

        % Callback function: CancelImport, ImportData, ReimportMenu, 
        % ...and 1 other component
        function import_callbacks(self, event)
            % Function called when the user clicks ImportData,
            % CancelImport, or ShowImportWindow (on the main UI). 
            %
            % Parameters:
            %    self (Quant4D)
            %    event (event.EventData)
            %
            % Returns:
            %    None

            switch event.Source
                case self.ShowImportWindow
                    figure(self.figures.Import)
                    
                    % Enter Import Preview Mode
                    if self.Mode.Value ~= "Preview"
                        mock_UI_callbacks(self, self.Mode, "Preview");
                    end

                case self.CancelImport
                    % Hide window when closing
                    self.figures.Import.Visible = "off";
                    
                    % Try to re-enter previous detector mode from Import Preview Mode
                    if self.Mode.Value == "Preview" && isfield(self.common_parameters,'detector_mode')
                        mock_UI_callbacks(self, self.Mode, self.common_parameters.detector_mode);
                    end

                case self.ReimportMenu
                    % Re-import the current dataset, mostly for debugging
                    if ~isfield(self.tmp_variables,'prev_D')
                        return;
                    end
                    
                    unload_data(self)
                    self.dataset_parameters = self.tmp_variables.prev_D;
                    import_data(self, event)

                case {self.ImportData self.PreviewButton}
                    % When the "Import Data" or "Preview" button is pressed
                    self.tmp_variables.Preview = [];

                    if ~isfile(self.ImportFilePath.Value)
                        notification_dialog(self, ...
                                            "warn", ...
                                            'The entered file path is invalid!', ...
                                            'Invalid File!');
                    
                    elseif self.ImportDataType.Value == "unknown"
                        notification_dialog(self, ...
                                            "warn", ...
                                            'Select the correct data type!', ...
                                            'Select Data Type!');
                    
                    else
                        if event.Source == self.ImportData
                            % Import data
                            self.figures.Import.Visible = "off";
                            
                            % unload data unless `SwapDataset` is ticked
                            unload_data(self, self.SwapDataset.Value)
                            
                            % gather all options from the Import UI, preview mode = false
                            self.dataset_parameters = gather_import_options(self, false);
                            
                            % Backup current `self.D`
                            self.tmp_variables.prev_D = self.dataset_parameters;
                            import_data(self, event)
                        else
                            % gather all options from the Import UI, preview mode = true
                            self.tmp_variables.Preview = gather_import_options(self, true);
                        end
                    end

                case {self.SwapDiffractionXY self.SwapRealXY}
                    % Refresh axes settings etc when dimensions swapped
                    prepare_data(self, event)

            end
        end

        % Callback function: ImportFilePath, ImportFileSelect
        function import_select_file(self, event)
            % Function called when the user clicks Select or updates
            % the file path on the Import UI (`ImportFileSelect` and
            % `ImportFilePath`, respectively)
            %
            % Parameters:
            %    self (Quant4D)
            %    event (event.EventData)
            %
            % Returns:
            %    None

            debug_time = tic;

            if event.Source == self.ImportFileSelect
                % Get user to select a file
                [fileName, fileDir] = uigetfile({'*.raw;*.mib;*.mrc;*.dm3;*.dm4;*.npy;*.h5;*.hdf5;*.hspy','Supported Formats'; ...
                                                 '*.*','All Files'}, ...
                                                 'Select 4DSTEM Dataset');
                
                % Force to show
                set(self.figures.Import,"Visible", "off","Visible", "on");
                
                if fileName
                    self.ImportFilePath.Value = fullfile(fileDir, fileName);
                end
            end

            if isfile(self.ImportFilePath.Value)
                % get file directory and extension
                [fileDir, ~, fileExt] = fileparts(self.ImportFilePath.Value);

                % change to directory containing dataset for future saving
                cd(fileDir)

                % get file size in bytes
                self.tmp_variables.FileSize = dir(self.ImportFilePath.Value).bytes;
                
                % Display actual file size in bytes and GiB
                self.ImportActualFilesize.Text = sprintf('%d bytes, %.1f GiB',self.tmp_variables.FileSize,self.tmp_variables.FileSize/1024^3);

                switch lower(fileExt)
                    case ".mib"
                        % Medipix data
                        self.Medipix.Value = true;
                    
                    case ".mrc"
                        % MRC data
                        self.MRC.Value = true;
                    
                    case {".dm3"; ".dm4"}
                        % Gatan K2/K3 data
                        self.DM34.Value = true;
                    
                    case {".h5"; ".hdf5"; ".hspy"}
                        self.HDF5.Value = true;
                    
                    case {".raw"}
                        self.EMPAD.Value = true;
                    
                    otherwise
                        self.Custom.Value = true;
                end
            
            else
                % if the file doesn't exist, revert to starting point
                self.ImportActualFilesize.Text = "";
                self.tmp_variables.FileSize = 0;
                
            end

            debug_toc(self, event, "", debug_time)

            % Further file info
            import_file_type(self, event)
        end

        % Callback function: FileTypeButtonGroup, SubDataset
        function import_file_type(self, event)
            % Function called when the user selects a new file type
            % category (`FileTypeButtonGroup`) or selects a new `SubDataset`
            % 
            % Parameters:
            %    self (Quant4D)
            %    event (event.EventData)
            %
            % Returns:
            %    None

            % Make an initial guess at the file dimensions (assume ~square field of view: NFrX≈NFrY)
            debug_time = tic;

            % Medipix data are saved as a .mib file of varying bit-depth as unsigned integers of the next highest class
            %   (i.e. 12-bit is saved as a 16-bit unsigned integer) with big-endian ordering.
            % EMPAD data are saved as a .raw file with 32-bit depth with little endian ordering.
            % Fiji/ImageJ tend to save their files with big-endian ordering, though this is also system- and user-dependent.

            notes = "";
            err = 0;
            self.ImportDataType.Items = {'Select Data Type';
                                        '8-bit Signed';
                                        '8-bit Unsigned';
                                        '16-bit Signed';
                                        '16-bit Unsigned';
                                        '32-bit Real';
                                        '32-bit Signed';
                                        '32-bit Unsigned';
                                        '64-bit Real';
                                        '64-bit Signed';
                                        '64-bit Unsigned'};

            self.ImportDataType.ItemsData = {'unknown';
                                            'int8';
                                            'uint8';
                                            'int16';
                                            'uint16';
                                            'single';
                                            'int32';
                                            'uint32';
                                            'double';
                                            'int64';
                                            'uint64'};

            self.tmp_variables.dm = [];
            self.tmp_variables.h5 = [];
            set([self.DataOffset self.FrameHeader self.FrameFooter], "Value",0)
            self.tmp_variables.fileTail = 0;
            self.ImportByteOrder.Value = "l";
            self.ImportDataType.Value = "unknown";
            
            if event.Source == self.ImportFileSelect
                set(self.SubDataset, "Items",{}, "Enable", "off")
            end
            
            if isfile(self.ImportFilePath.Value)
                switch self.FileTypeButtonGroup.SelectedObject
                    case self.EMPAD
                        self.FrameFooter.Value = 1024;
                        self.ImportDataType.Value = "single";
                        self.ImportPixelsX.Value = 128;
                        self.ImportPixelsY.Value = 128;
                        notes = sprintf('Pixels:\t128x128\n32-bit Real\n** EMPAD data have 1024-byte frame footers');
                        guess_frames_from_size(self);
                        get_dims_from_name(self, self.ImportFilePath.Value)

                        % check if file size matches (i.e. likely an EMPAD
                        % file), or if it suits better to set FrameHeader,
                        % FrameFoot, and DataOffset to 0 (i.e. a .raw
                        % binary file from simulation or other)
                        file_size = self.DataOffset.Value ...
                                    + (self.FrameHeader.Value...
                                       + self.ImportPixelsX.Value ...
                                       * self.ImportPixelsY.Value ...
                                       * self.byte_size.(self.ImportDataType.Value) ...
                                       + self.FrameFooter.Value ...
                                       ) ...
                                    * (self.ImportFramesX.Value* self.ImportFramesX.Value);
                        if file_size > dir(self.ImportFilePath.Value).bytes
                            test_size = self.ImportPixelsX.Value * ...
                                        self.ImportPixelsY.Value * ...
                                        self.ImportFramesX.Value * ...
                                        self.ImportFramesX.Value * ...
                                        self.byte_size.(self.ImportDataType.Value);
                            if test_size == dir(self.ImportFilePath.Value).bytes
                                self.Custom.Value = 1;
                                self.FrameFooter.Value = 0;
                                self.FrameHeader.Value = 0;
                                self.DataOffset.Value = 0;
                            end
                        end

                    case self.Medipix
                        self.ImportDataType.Items = ["Select Data Type"; ["1 or 6";"12";"24"]+"-bit Padded Unsigned"];
                        self.ImportDataType.ItemsData = {"unknown";"uint8";"uint16";"uint32"};
                        fid = fopen(self.ImportFilePath.Value,"r");
                        fmeta = strsplit(fread(fid, 128, 'uint8=>char')', ',');
                        
                        % Signature character in header
                        if numel(fmeta) >= 7 && ismember(lower(fmeta{7}(1)), ["r", "u"])
                            % Re-read with known header size
                            frewind(fid)
                            fmeta = strsplit(fread(fid, str2double(fmeta{3}), 'uint8=>char')', ',');
                            
                            dtype = lower(fmeta{7});
                            bitsize = str2double(fmeta(end-1));
                            
                            if dtype(1) == 'u'
                                switch bitsize
                                    case {1; 6}, self.ImportDataType.Value = "uint8";
                                    case 12, self.ImportDataType.Value = "uint16";
                                    case 24, self.ImportDataType.Value = "uint32";
                                end
                            end
                            
                            self.FrameHeader.Value = str2double(fmeta{3});
                            self.ImportByteOrder.Value = "b";
                            self.ImportPixelsX.Value = str2double(fmeta{5});
                            self.ImportPixelsY.Value = str2double(fmeta{6});
                            notes = sprintf(['Dim: X = %s, Y = %s\nData type: %s\nPixel depth: %d bit\n' ...
                                             'Frame header: %s bytes\nBig endian'], fmeta{5}, fmeta{6}, fmeta{7}, bitsize, fmeta{3});
                            guess_frames_from_size(self);
                            get_dims_from_name(self, self.ImportFilePath.Value)
                        
                        else
                            notes = 'Unrecognizable as a Medipix/.mib file.';
                            err = -1;
                        end
                        fclose(fid);

                    case self.MRC
                        % Read in MRC header - first 1024 bytes
                        fid = fopen(self.ImportFilePath.Value,"r");
                        fseek(fid,208,'bof');
                        map = fread(fid, [1, 4], 'uint8=>char');
                        
                        % Signature characters
                        if map == "MAP "
                            % Bytes for Endianness
                            e = fread(fid, 2, "uint8");
                            
                            if e(1) == 68 && ismember(e(2), [65, 68])
                                self.ImportByteOrder.Value = "l";
                                bo = 'Little Endian';
                            
                            elseif e(1) == 17 && e(2) == 17
                                self.ImportByteOrder.Value = "b";
                                bo = 'Big Endian';
                            
                            else
                                bo = 'Unknown Endianness';
                            
                            end

                            frewind(fid);
                            
                            % X, Y and Z, only 3D
                            dim = fread(fid,3,"uint32");
                            
                            self.ImportPixelsX.Value = dim(1);
                            self.ImportPixelsY.Value = dim(2);
                            self.ImportFramesX.Value = dim(3);
                            
                            guessFramesFromDimZ(dim(3))
                            get_dims_from_name(self, self.ImportFilePath.Value)

                            dtype = fread(fid,1,"uint32");
                            
                            switch dtype
                                case 0
                                    self.ImportDataType.Value = "int8";
                                    tnote = "8-bit Signed Integer";
                                
                                case 1
                                    self.ImportDataType.Value = "int16";
                                    tnote = "16-bit Signed Integer";
                                
                                case 2
                                    self.ImportDataType.Value = "single";
                                    tnote = "32-bit Real Float";
                                
                                case 3
                                    tnote = "16-bit Complex Signed Integer, unsupported";
                                
                                case 4
                                    tnote = "32-bit Complex Float, unsupported";
                                
                                case 6
                                    self.ImportDataType.Value = "uint16";
                                    tnote = "16-bit Unsigned Integer";
                                
                                otherwise
                                    tnote = "Uknown data type";
                            end

                            self.DataOffset.Value = 1024;
                            notes = sprintf('Dim: X = %d, Y = %d, Z = %d\n%s, %s\n** MRC files have a 1024-byte data offset', ...
                                dim, tnote, bo);
                        else
                            notes = sprintf('Unrecognizable as MRC.\n\n"MAP " word missed.');
                            err = -1;
                        end
                        fclose(fid);

                    case self.DM34
                        % Read .dm3/4 tag values
                        try self.tmp_variables.dm = dmInfo(self.ImportFilePath.Value);catch;end
                        
                        if iscell(self.tmp_variables.dm) && numel(self.tmp_variables.dm) > 1
                            % List all images' names in `self.SubDataset`
                            pdim = zeros(numel(self.tmp_variables.dm)-1, 1);
                            self.SubDataset.Enable = "on";
                            for i = 1:numel(pdim)
                                self.SubDataset.Items{i} = char(self.tmp_variables.dm{i}.Name);
                                pdim(i) = prod(cell2mat(self.tmp_variables.dm{i}.Dimensions));
                            end
                            
                            % Select sub-image with the largest dimension; unless manual selected
                            if event.Source == self.SubDataset
                                self.SubDataset.Value = event.Value;
                            else
                                [~, i] = max(pdim);
                                self.SubDataset.Value = self.SubDataset.Items{i};
                            end
                            
                            % Info of selected sub-image
                            dm = self.tmp_variables.dm{[strcmp(self.SubDataset.Items, self.SubDataset.Value), false]};
                            finfo = self.tmp_variables.dm{end};
                            
                            % Read dimensions
                            dims = dm.Dimensions;
                            
                            % Fill missing dimensions as 1
                            for i = 1:4
                                if i > numel(dims)
                                    dims{i} = 1;
                                end
                            end

                            set([self.ImportPixelsX, ...
                                 self.ImportPixelsY, ...
                                 self.ImportFramesX, ...
                                 self.ImportFramesY], ...
                                {"Value"}, dims)
                            
                            % Find offset, file tail, data type, byte-order of dataset
                            self.DataOffset.Value = dm.Data.offset;
                            try self.ImportDataType.Value = dm.Data.dataType; catch;end
                            self.tmp_variables.fileTail = finfo.fileSize - dm.Data.offset - dm.Data.size;
                            
                            % If pixels are not scalars (e.g. complex image)
                            if dm.ImageDataType.pixel ~= "scalar"
                                self.ImportDataType.Value = "unknown";
                            end

                            % Is it little endian?
                            if finfo.liEndian
                                self.ImportByteOrder.Value = "l";
                                bo = 'Little Endian';
                            else
                                self.ImportByteOrder.Value = "b";
                                bo = 'Big Endian';
                            end

                            notes = sprintf("Dim: X = %d, Y = %d, Z = %d, W = %d\nDM%d, %s\nData-type: %s\n" ...
                                +"Selected sub-image's offset is %d bytes.", ...
                                dims{:}, finfo.version, bo, dm.ImageDataType.full, dm.Data.offset);

                            if dims{4} == 1
                                guessFramesFromDimZ(dims{3});
                            end

                        else
                            notes = "Read DM file error: " + self.tmp_variables.dm;
                            err = -1;
                        end

                    case self.HDF5
                        try
                            self.tmp_variables.h5 = h5_datasets(self, self.ImportFilePath.Value);
                        catch
                            notes = 'Read HDF5 file error';
                            err = -1;
                        end

                        if ~err
                            self.SubDataset.Enable = "on";
                            % Select sub-image with the 1st largest dimension; unless manual selected
                            if event.Source ~= self.SubDataset
                                % List all images' names in `self.SubDataset`
                                pdim = zeros(numel(self.tmp_variables.h5)-1, 1);
                                for i = 1:numel(pdim)
                                    self.SubDataset.Items{i} = char(self.tmp_variables.h5(i).Name);
                                    pdim(i) = prod(self.tmp_variables.h5(i).Dataspace.Size);
                                end
                                [~, i] = max(pdim);
                                self.SubDataset.Value = self.SubDataset.Items{i};
                            end
                            
                            % Info of selected sub-image
                            h5i = self.tmp_variables.h5([strcmp(self.SubDataset.Items, self.SubDataset.Value), false]);
                            
                            % Read dimensions
                            dims = h5i.Dataspace.Size;
                            
                            % Fill missing dimensions as 1
                            for i = 1:4
                                if i > numel(dims)
                                    dims(i) = 1;
                                end
                            end

                            % set Import UI values
                            set([self.ImportPixelsX; ...
                                 self.ImportPixelsY; ...
                                 self.ImportFramesX; ...
                                 self.ImportFramesY], ...
                                {"Value"},num2cell(dims)')
                            
                            % Find offset, file tail, data type, byte-order of dataset
                            if h5i.offset == -1
                                self.DataOffset.Value = 0;
                                noteoffs = 'This dataset is not "contiguous", thus data offset is unknown.';
                            else
                                self.DataOffset.Value = h5i.offset;
                                noteoffs = "Selected dataset's offset is "+h5i.offset+" bytes.";
                            end

                            self.tmp_variables.fileTail = self.tmp_variables.h5(end).size - self.DataOffset.Value - h5i.size;
                            
                            % If data type is unknown
                            if ~isempty(h5i.type)
                                self.ImportDataType.Value = h5i.type;
                            end

                            if endsWith(h5i.byte_order, "_BE")
                                self.ImportByteOrder.Value = "b";
                                bo = 'Big Endian';
                            else
                                self.ImportByteOrder.Value = "l";
                                bo = 'Little Endian';
                            end

                            notes = sprintf("Dim: X = %d, Y = %d, Z = %d, W = %d\n%s, %s\n%s", dims, bo, h5i.Datatype.Type, noteoffs);
                            
                            if dims(4) == 1
                                guessFramesFromDimZ(dims(3));
                            end
                        end

                    otherwise %case self.Custom
                        get_dims_from_name(self, self.ImportFilePath.Value)
                        self.ImportDataType.Value = "single";
                        notes = "Custom import";

                end
            else
                notes = "File path is invalid";
                err = -1;
            end

            self.ImportFileMetadata.Value = notes;

            if self.ImportDataType.Value == "unknown" &&  err ~= -1
                notification_dialog(self, ...
                                    "warn", ...
                                    "The data type indicated in the file's metadata is not supported/recognized.", ...
                                    "Invalid Data Type!");
            end

            debug_toc(self, event, "", debug_time)

            % Reset import range selections
            range_import_export(self, struct("Source", self.ImportPixelsX, "EventName", []));
            range_import_export(self, struct("Source", self.ImportFramesX, "EventName", []));
            import_box_input(self, event)
        end

        % Value changed function: DataOffset, 
        % ...and 22 other components
        function import_box_input(self, event)
            % Function called when the user interacts with the Import UI
            % 
            % Parameters:
            %    self (Quant4D)
            %    event (event.EventData)
            %
            % Returns:
            %    None

            debug_time = tic;
            
            % initialize parameters
            self.ImportEstimatedFilesize.Text = "";
            notes = "";
            diffraction_event = event;
            real_event = event;

            if isfile(self.ImportFilePath.Value)
                % Update Diffraction and Real-space import ranges; use dummy event if source is not a range UI
                if ~contains(event.Source.Tag, "Diffraction")
                    diffraction_event = struct("Source",self.DiffractionPartialImportPixelsDist, "Value",self.DiffractionPartialImportPixelsDist.Value);
                end
                if ~contains(event.Source.Tag, "Real")
                    real_event = struct("Source",self.RealPartialImportFramesDist, "Value",self.RealPartialImportFramesDist.Value);
                end

                [diffraction_note, ~, ~, n_pixels, ~] = range_import_export(self, diffraction_event);
                [real_note, ~, ~, n_frames, ~] = range_import_export(self, real_event);
                notes = diffraction_note + real_note;
                
                % Enable/Disable Range UIs
                set(self.DiffractionPartialImportGrid.Children, "Enable", self.ImportPartialPixels.Value)
                set(self.RealPartialImportGrid.Children, "Enable", self.ImportPartialFrames.Value)
                
                % Current dataset dimensions
                irng = [n_pixels n_frames];
                
                % Allow for virtual memory mapping in some situations
                if self.FrameHeader.Value == 0 && self.FrameFooter.Value == 0 ...
                        && (~self.HDF5.Value || self.DataOffset.Value) ...
                        && self.ImportByteOrder.Value == self.sys_constants.system_endianness && ~contains(self.ImportDataType.Value,'int') ...
                        && isequal([self.ImportPixelsX.Value self.ImportPixelsY.Value self.ImportFramesX.Value self.ImportFramesY.Value], irng)
                    self.MemoryType.Enable = "on";
                else
                    self.MemoryType.Enable = "off";
                    self.MemoryType.Value = "Physical Memory";
                end

                % Calculate dataset size and memory usage
                if self.ImportDataType.Value ~= "unknown"
                    bytesize = self.byte_size.(self.ImportDataType.Value);
                    self.tmp_variables.EstSize = self.DataOffset.Value + self.tmp_variables.fileTail ...
                        + (self.FrameHeader.Value+self.ImportPixelsX.Value*self.ImportPixelsY.Value*bytesize+self.FrameFooter.Value) ...
                        * self.ImportFramesX.Value*self.ImportFramesY.Value;
                    self.ImportEstimatedFilesize.Text = sprintf('%d bytes, %.1f GiB',self.tmp_variables.EstSize,self.tmp_variables.EstSize/1024^3);

                    if contains(self.ImportDataType.Value,'int')
                        if bytesize > 4
                            f = "double";
                        else
                            f = "single";
                        end
                        bytesize = self.byte_size.(f);
                        notes = notes+"\nDataset will be converted into "+bytesize*8+"-bit Real.";
                    end
                    notes = notes+"\nImport by "+self.MemoryType.Value+"\n"+check_memory(self, event, n_pixels, n_frames, bytesize);
                    notes = notes+"\n\n"+check_GPU_memory(self, n_pixels, n_frames);
                end
                
                % Allow to swap dataset/keep parameters if the dimensions are identical
                self.SwapDataset.Enable = ~isempty(self.dataset_parameters) && isequal(irng, [self.dataset_parameters.n_pixels(1) self.dataset_parameters.n_pixels(2) self.dataset_parameters.n_frames(1) self.dataset_parameters.n_frames(2)]);
                if ~self.SwapDataset.Enable
                    self.SwapDataset.Value = false;
                end
                
                if self.SwapDataset.Value
                    notes = notes+"\n\nSwapping dataset - keep current setups/alignments etc.";
                end
            else
                % default to GPU off when no file path is present
                self.GPU.Value = 0;
            end

            self.ImportSummary.Value = sprintf(notes);

            debug_toc(self, event, "", debug_time)
        end

        % Callback function: AutoSaveImage, SaveDirectoryButton, 
        % ...and 12 other components
        function save_callbacks(self, event)
            % Function called when the user interacts with the Save/Export UI
            % 
            % Parameters:
            %    self (Quant4D)
            %    event (event.EventData)
            %
            % Returns:
            %    None

            debug_time = tic;
            
            % Try to update image name prefix
            update_prefix(self, event)

            switch event.Source
                case self.ShowSaveWindow
                    figure(self.figures.Save)
                    % Trigger tab change callbacks defined in `@self.export_callbacks()`
                    mock_UI_callbacks(self, self.SaveTabGroup);
                
                case self.SaveDirectoryButton
                    directory = uigetdir(self.SaveDirectoryPath.Value, 'Select Directory to Save Images');
                    drawnow
                    figure(self.figures.Save)
                    if directory
                        self.SaveDirectoryPath.Value = directory;
                    end

                case self.SaveDirectoryPath
                
                case {self.SaveImagePrefix self.SavePrefixAngleInner self.SavePrefixAngleOuter}
                
                case self.SaveImageList % Save image list selection change
                    % If user selects all of the images in the list, tick the "Save All" checkbox
                    self.SaveImageSelectAll.Value = numel(self.SaveImageList.Value) == numel(self.SaveImageList.Items);
                
                case {self.AutoSaveImage self.SaveExport} % Save images/Auto-save images or Export data
                    if self.SaveDirectoryPath.Value == "" || isempty(self.SaveDirectoryPath.Value)
                        notification_dialog(self, "warn",sprintf("Please specify the directory!"),'Directory Missing');
                    else
                        % Create directory if not exists
                        [success, error_message] = mkdir(self.SaveDirectoryPath.Value);
                        if ~success
                            notification_dialog(self, "warn",sprintf("Failed to create directory!\n\n"+error_message),'Directory Error');
                        else
                            % Save images if called from `self.AutoSaveImage` or currently the `self.SaveImagesTab` is selected
                            if self.SaveTabGroup.SelectedTab == self.SaveImagesTab || event.Source == self.AutoSaveImage
                                % Save images
                                save_images(self);
                            else
                                % Export data
                                export_callbacks(self, event)
                            end
                        end
                    end
                
                case self.SaveImageSelectAll % Select all/none
                    if event.Value
                        self.SaveImageList.Value = self.SaveImageList.ItemsData;
                    else
                        self.SaveImageList.Value = {};
                    end
                
                case {self.SaveImagePNG self.SaveImageAnnotations}
                    % Enable/Disable PNG options
                    self.SaveImageAnnotations.Enable = self.SaveImagePNG.Value;
                    set([self.SaveImageDPI self.SaveImgAnnotDPILabel], ...
                        "Enable", ...
                        self.SaveImageAnnotations.Value && self.SaveImagePNG.Value)
            end

            debug_toc(self, event, "", debug_time)
        end

        % Callback function: DiffractionPartialExportPixelsDist, 
        % ...and 27 other components
        function export_callbacks(self, event)
            % Function called when the user interacts with the Save/Export UI
            % 
            % Parameters:
            %    self (Quant4D)
            %    event (event.EventData)
            %
            % Returns:
            %    None

            debug_time = tic;

            switch event.Source
                case self.SaveCloseButton % Close button on Save/Export Window
                     % Try to remove Export ROIs
                    delete(findobj(self.ui_groups.image_axes,'-regexp', "Tag",'Export .... ROI'))
                    
                    % Reset button color
                    self.SaveCloseButton.BackgroundColor = self.sys_constants.background_color;

                    % hide save window
                    self.figures.Save.Visible = "off";

                case {self.SaveTabGroup self.ExportPartialPixels self.ExportPartialFrames} % Tab change or enable/disable partial export
                     % Try to delete old ROIs
                    delete(findobj(self.ui_groups.image_axes,'-regexp', "Tag",'Export .... ROI'))

                    % Try to update export range
                    if ~isempty(self.dataset_parameters)
                        update_export_range(self, event);
                    end
                    
                    if self.SaveTabGroup.SelectedTab == self.ExportDatasetTab && self.figures.Save.Visible
                        % To start Export Data Mode
                        self.SaveExport.Text = "Export Data";

                        % Draw ROIs & add listening functions for live updates on all Real and Diffraction space images
                        for id = self.ui_groups.image_id(self.ui_groups.image_space ~= "ColorWheel" & self.ui_groups.image_type ~= "Mask")
                            self.annotations.Export.(id) = drawrectangle(self.image_axes.(id), ...
                                                                        "Position", [1 1 0 0], ...
                                                                        "Color", "y", ...
                                                                        "Deletable", 0, ...
                                                                        'FaceAlpha', 0, ...
                                                                        'FaceSelectable', 0);
                            self.annotations.Export.(id).Tag = "Export " + self.image_axes.(id).UserData.space + " ROI";
                            
                            % add listeners for ROI annotation movement
                            self.annotations.Export.(id).UserData.Move = addlistener(self.annotations.Export.(id), "MovingROI", @move_export_annotation);
                            addlistener(self.annotations.Export.(id), "ROIMoved", @move_export_annotation);
                        end

                        % Force ROIs to update
                        export_callbacks(self, struct("Source", self.DiffractionPartialExportXStart, ...
                                                     "EventName", "ValueChanged", ...
                                                     "Value", self.DiffractionPartialExportXStart.Value))

                        export_callbacks(self, struct("Source", self.RealPartialExportXStart, ...
                                                     "EventName", "ValueChanged", ...
                                                     "Value", self.RealPartialExportXStart.Value))
                        
                        % Show/Hide ROIs and enable/disable UIs if (not) selecting whole ranges
                        set(findobj(self.ui_groups.diffraction_axes, "Tag",'Export Diffraction ROI'), "Visible", self.ExportPartialPixels.Value)
                        set(findobj(self.ui_groups.real_axes, "Tag",'Export Real ROI'), "Visible", self.ExportPartialFrames.Value)
                        set(self.RealPartialExportGrid.Children, "Enable", self.ExportPartialFrames.Value)
                        set(self.DiffractionPartialExportGrid.Children, "Enable", self.ExportPartialPixels.Value)
                        
                        % Set close button color to hint/link with the ROIs
                        if self.ExportPartialPixels.Value || self.ExportPartialFrames.Value
                            c = 'y';
                        else
                            c = self.sys_constants.background_color;
                        end
                    
                    else % For "Save Images"
                        self.SaveExport.Text = "Save Images";
                        c = self.sys_constants.background_color;
                    end

                    % Color the close button to hint/link with the ROIs
                    self.SaveCloseButton.BackgroundColor = c;

                case {self.ExportDimensionSuffix self.ExportDataType self.ExportByteOrder}
                    update_export_range(self, event);
                
                case self.SaveExport % Export Button
                    try
                        export_data(self, event);
                    catch ME
                        % delete the progress dialog and export file
                        try delete(self.tmp_variables.progress_dialog); catch; end
                        try delete(self.tmp_variables.efile); catch; end
                        
                        % Reshape dataset to 2D
                        try self.data = reshape(self.data, prod(self.dataset_parameters.n_pixels), []);  catch; end
                        enable_windows(self,true)

                        % pass along error message
                        rethrow(ME)
                    end
            end

            debug_toc(self, event, "", debug_time)
        end

        % Value changed function: ReverseDiffractionX, 
        % ...and 7 other components
        function axis_direction_callbacks(self, event)
            % Function called when the user modifies the axis orientation
            % in diffraction or real space
            % 
            % Parameters:
            %    self (Quant4D)
            %    event (event.EventData)
            %
            % Returns:
            %    None

            % Function to flip/rotate image axes
            debug_time = tic;

            % Space, "Real" or "Diffraction"
            space = event.Source.Tag;
            
            % For axis direction
            axis_direction = ["normal" "reverse"];
            
            % Get X/Y-axis direction and rotation options of diffraction/real-space
            reverse_x = struct('Diffraction', self.ReverseDiffractionX.Value, 'Real', self.ReverseRealX.Value);
            reverse_y = struct('Diffraction', self.ReverseDiffractionY.Value, 'Real', self.ReverseRealY.Value);
            rotate_view = struct('Diffraction', self.RotateDiffraction.Value, 'Real', self.RotateReal.Value);
            
            % Set axis directions and rotations of either diffraction or real-space images
            set(self.ui_groups.(lower(space)+"_axes"), ...
                "XDir", axis_direction(reverse_x.(space)+1), ...
                "YDir", axis_direction(reverse_y.(space)+1), ...
                'View', [rotate_view.(space), 90])

            % set state button icon color based on value
            for state_button = [self.ReverseDiffractionY, ...
                                self.ReverseDiffractionX, ...
                                self.ShowDiffractionAxes, ...
                                self.ReverseRealY, ...
                                self.ReverseRealX, ...
                                self.ShowRealAxes]
                change_icon_background(self, state_button)
            end

            % Sync ColorWheel with real-space axes direction
            if space == "Real"
                set(self.image_axes.ColorWheel, ...
                    {"XDir" "YDir" 'View'}, ...
                    get(self.image_axes.Real,{"XDir" "YDir" 'View'}));
            end
            
            % X/Y labels of axis annotations
            labels = struct('x', struct('Diffraction', "kx",'Real', "rx"), ...
                            'y', struct('Diffraction', "ky",'Real', "ry"));
            
            % Update axis annotations
            arrayfun(@(x) draw_axis_direction(self, x, space), self.ui_groups.(lower(space)+"_id"));

            debug_toc(self, event, "", debug_time)

            function draw_axis_direction(self, id, space)
                % Internal function to draw the axis annotations; relies on
                % global variables (`labels`, `reverse_x`, `reverse_y`, and
                % `rotate_view`) from `axis_direction_callbacks`
                %
                % Parameters:
                %    self (Quant4D)
                %    id (str): figure/axes/image id
                %    space (str): "Diffraction" or "Real" for the given `id`
                %
                % Returns:
                %    None
            
                fig = self.figures.(id);
                
                % Colors of X/Y axes
                color_x = "r";
                color_y = 'g';
                
                % Draw annotations on `figure`
                % delete(findall(fig,'-depth',2, "Tag",'AxeDir')) % Always delete old and draw new annotations
                if isempty(findall(fig,'-depth',2, "Tag",'AxeDir')) || ~isfield(fig.UserData, 'axis_annotation')
                    fig.UserData.axis_annotation = [];
                
                    % Draw scan directions on Diffraction images
                    if space == "Diffraction"
                        draw_axis_direction(self, id, "Real");
                    end
                
                    x_arrow = annotation(fig, "arrow");
                    x_text = annotation(fig, "textbox", "String", labels.x.(space));
                    y_arrow = annotation(fig, "arrow");
                    y_text = annotation(fig, "textbox", "String", labels.y.(space));
                
                    set([x_arrow, y_arrow], ...
                        "LineWidth", 1, ...
                        "HeadLength", 3, ...
                        "HeadWidth", 3, ...
                        "HeadStyle", "plain")
                
                    set([x_text, y_text], ...
                        "FontWeight", "bold", ...
                        "HorizontalAlignment", "center", ...
                        "VerticalAlignment", "middle")
                
                    set([x_arrow; y_arrow; x_text; y_text], ...
                        'Units', "pixels", ...
                        "PickableParts", "no", ...
                        "Tag", "AxeDir", ....
                        {"Color"}, {color_x; color_y; color_x; color_y})
                    
                    % Scan direction annotation at 5:8 for "Diffraction"
                    fig.UserData.axis_annotation = [x_arrow; y_arrow; x_text; y_text; fig.UserData.axis_annotation];
                    uistack(fig.UserData.axis_annotation,'bottom')
                end
                
                % Set annotation positions/directions
                %  `l`/`t`: length for arrow/total;
                %  `xy`: [arrow origin, arrow X, arrow Y, label X, label Y] positions
                l = 4;
                t = 12;
                xy = [-t -t; l -t; -t l; t -t; -t t];
                
                % Offset from bottom-left
                offset = 22;
                
                % X/Y flip
                xy_flip = 1 - [reverse_x.(space), reverse_y.(space)]*2;
                
                % Axes rotation (clockwise)
                R = rotation_matrix(self, -rotate_view.(space));
                
                update_annotation_positions(fig.UserData.axis_annotation(1:4), offset*[1 1], xy.*xy_flip*R)
                set(fig.UserData.axis_annotation(1:4), "Visible",self.("Show"+space+"Axes").Value)
                
                % Set scan directions on Diffraction patterns
                if space == "Diffraction"
                    l = 1;
                    t = 9;
                    xy = [-t -t; l -t; -t l; t -t; -t t];
                    Rscan = rotation_matrix(self, self.ScanDirectionSlider.Value);
                    scan_flip_y = 1 - 2*[0 self.FlipScanDirectionY.Value];
                    update_annotation_positions(fig.UserData.axis_annotation(5:end), offset*[2.8 1], xy.*scan_flip_y*Rscan.*xy_flip*R)
                
                    % Warning color if scan directions not aligned
                    if ~isfield(self.common_parameters,'scan_direction_initialized') || ~self.common_parameters.scan_direction_initialized
                        color_x = self.sys_constants.warning_color;
                        color_y = color_x;
                    end
                
                    % Only visible when:
                    % 1) show Diffraction annotation AND
                    % 2) not during scan direction alignment AND
                    % 3) in CoM/DPC modes
                    set(fig.UserData.axis_annotation(5:8), ...
                        {"Color"}, {color_x;color_y;color_x;color_y}, ...
                        "Visible", self.ShowDiffractionAxes.Value && ...
                        ~self.ScanDirectionLock.Value && ...
                        any(self.Mode.Value == ["CoM" "DPC"]))
                end
            
                function update_annotation_positions(annotation_group, annot_offset, annot_xy)
                    % Function to update annotation positions
                    %
                    % Parameters:
                    %    annotation_group (4,1) graphics_array: group of arrow and textbox annotations for scan/diffraction direction annotations
                    %    annotation_offset (1,2) float: offset from bottom left corner of the figure
                    %    annotation_xy (5,2) int: [arrow origin, arrow X, arrow Y, label X, label Y] positions
                    %
                    % Returns:
                    %    None

                    % Arrow position: [ Origin XY, Vector XY ];
                    arrow_position_x = [annot_offset + annot_xy(1,:), annot_xy(2,:) - annot_xy(1,:)];
                    arrow_position_y = [annot_offset + annot_xy(1,:), annot_xy(3,:) - annot_xy(1,:)];

                    % Label position: [ Center XY, width, height ]
                    arrow_label_x = [annot_offset + annot_xy(4,:), 0, 0];
                    arrow_label_y = [annot_offset + annot_xy(5,:), 0, 0];

                    % update annotation positions
                    set(annotation_group, ...
                        {"Position"}, ...
                        {arrow_position_x; ...
                         arrow_position_y; ...
                         arrow_label_x; ...
                         arrow_label_y})
                end

            end
        end

        % Callback function: DispColorMap, DispColorMapInvert, 
        % ...and 24 other components
        function display_callbacks(self, event)
            % Function to update all aspects of the image display,
            % including brightness, contrast, gamma, colormap, histogram,
            % vector field, and mask opacity.
            % 
            % Parameters:
            %    self (Quant4D)
            %    event (event.EventData)
            %
            % Returns:
            %    None
            
            debug_time = tic;
            
            id = self.DisplayImage.Value;
            user_data = self.image_axes.(id).UserData;
            source = event.Source;

            % Initial contrast will be set as the total range of min:max
            % A change in contrast will expand or contract the width of the range
            % Initial brightness will be also set as the total range of min:max
            % A change in brightness will result in shift of the range up or down
            % Initial gamma is set to 1
            % A change in gamma will result in a power law change in contrast I' = I^gamma
            switch source
                case self.HistogramLog 
                    % set state button icon color based on value
                    change_icon_background(self, self.HistogramLog)

                    % Log-scale option of histogram
                    if self.HistogramLog.Value
                        self.HistogramAxes.YScale = 'log';
                    else
                        self.HistogramAxes.YScale = 'linear';
                    end

                case self.DisplayLock
                    % Lock "current" image
                    % set state button icon color based on value
                    change_icon_background(self, self.DisplayLock)
                    self.DisplayImage.BackgroundColor = self.DisplayTab.BackgroundColor;

                case self.DisplayVectorField
                    % Vector field
                    user_data.vector_field = event.Value;

                case self.DisplayVectorColor
                    % Vector field color
                    color = uisetcolor(user_data.vector_color);

                    % Early return if canceled
                    if isequal(color, 0)
                        return;
                    end
                    user_data.vector_color = color;

                case self.DispColorMap
                    % Colormap
                    user_data.colormap = event.Value;
                    cmap = str2func(user_data.colormap);
                    cm = cmap();
                    
                    % Whether to invert colormap
                    if user_data.invert
                        cm = flipud(cmap());
                    end
                    colormap(self.image_axes.(id), cm)
                
                case self.DispColorMapInvert
                    % set state button icon color based on value
                    change_icon_background(self, self.DispColorMapInvert)

                    % Invert colormap
                    user_data.invert = event.Value;
                    cmap = str2func(user_data.colormap);
                    cm = cmap();
                    
                    % Whether to invert colormap
                    if user_data.invert
                        cm = flipud(cmap());
                    end
                    colormap(self.image_axes.(id), cm)
                
                case self.DisplayBrightnessReset
                    % Reset brightness
                    user_data.brightness = 50;
                
                case self.DisplayContrastReset
                    % Reset contrast
                    user_data.contrast = 50;
                
                case self.DisplayGammaReset
                    % Reset gamma
                    user_data.gamma = 1;
                
                case {self.DisplayBrightnessSpinner, self.DisplayBrightness}
                    % Brightness
                    user_data.brightness = event.Value;
                
                case {self.DisplayContrastSpinner, self.DisplayContrast}
                    % Contrast
                    user_data.contrast = event.Value;
                
                case {self.DisplayGamma, self.DisplayGammaSpinner}
                    % Gamma
                    user_data.gamma = event.Value;
                
                case {self.DisplayMaskOpacitySlider, self.DisplayMaskOpacitySpinner}
                    % Mask opacity
                    user_data.mask_opacity = event.Value;
                
                otherwise   % e.g. self.DisplayImage
                    % Bring selected image to front
                    figure(self.figures.(id))
                    
                    % Update GUIs by values stored in `self.image_axes.(id).UserData` for the current selected image
                    set([self.DisplayVectorField; ...
                         self.DispColorMap; ...
                         self.DispColorMapInvert], ...
                        {"Value"}, ...
                        {user_data.vector_field; ...
                         user_data.colormap; ...
                         user_data.invert})

                    self.DisplayVectorColor.BackgroundColor = user_data.vector_color;
                    
                    % Enable vector field UIs if: 1) in CoM/DPC mode AND 2) real-space image selected
                    set([self.DisplayVectorField; ...
                         self.DispVecFieldLabel; ...
                         self.DisplayVectorColor], ...
                        "Enable", ismember(self.Mode.Value, ["CoM" "DPC"]) && user_data.space == "Real")
                    
                    % Disable brightness/contrast/colormap UIs if: (CoM/DPC) "Phase" and "ColorWheel for Phase" images
                    set([findobj(self.DispContrastsGrid.Children,'-not',"type",'uibutton'); ...
                         self.DispColorMap;self.DispColorMapInvert], ...
                        "Enable", ~contains(user_data.name, "Phase"));
                    
                    % Disable mask opacity UIs if: ColorWheel/Mask/Preview images selected
                    set([self.ShowMaskWindow; ...
                         self.DisplayMaskOpacitySpinner; ...
                         self.DisplayMaskOpacitySlider], ...
                        "Enable", user_data.space ~= "ColorWheel" && ~ismember(user_data.type, ["Mask" "Preview"]))
            end

            % Update UI
            set_external_source(self, event,[self.DisplayBrightnessSpinner, self.DisplayBrightness], "Value",user_data.brightness)
            set_external_source(self, event,[self.DisplayContrastSpinner, self.DisplayContrast], "Value",user_data.contrast)
            set_external_source(self, event,[self.DisplayGammaSpinner, self.DisplayGamma], "Value",user_data.gamma)
            set_external_source(self, event,[self.DisplayMaskOpacitySpinner, self.DisplayMaskOpacitySlider], "Value",user_data.mask_opacity)

            % Update properties stored by the `axes`
            self.image_axes.(id).UserData = user_data;
            
            % Re-plot image
            plot_image(self, event, id);

            debug_toc(self, event, "", debug_time)
        end

        % Callback function: RealROIFrameX, RealROIFrameX, RealROIFrameY, 
        % ...and 3 other components
        function realspace_ROI_callbacks(self, event)
            % Function to update the real space ROI based on the selected
            % type and location from the main UI, as well as to update the
            % diffraction pattern accordingly. 
            % 
            % Parameters:
            %    self (Quant4D)
            %    event (event.EventData)
            %
            % Returns:
            %    None

            debug_time = tic;

            switch event.Source
                case self.UpdateImages
                    % Draw ROI if doesn't yet exist and update
                    % diffraction image
                    if isempty(findobj(self.ui_groups.real_axes, "Tag","Real-space ROI"))
                        mock_UI_callbacks(self, self.RealROIShape)
                    else
                        move_real_ROI(self, self.annotations.RealROI.Real, event)
                    end
                
                case self.RealROIShape
                    roi_type = self.RealROIShape.Value;
                    if roi_type == "file"
                        self.images.RealROIFile = import_mask(self, "Real");
                        
                        % if ROI import from file is canceled, revert 
                        if isempty(self.images.RealROIFile)
                            roi_type = "full";
                        end
                    end

                    % Update GUI if changed programmatically
                    self.RealROIShape.Value = roi_type;

                    % Panel enable/disable
                    set([self.RealROIGrid.Children; ...
                         self.RealROIFrameLabel], ...
                        "Enable", roi_type == "point")

                    % Allow for inversion of the ROI if not full field
                    self.RealROIInvert.Enable = roi_type ~= "full";
                    
                    % If disabled, then set to off
                    self.RealROIInvert.Value = self.RealROIInvert.Value && ...
                                              self.RealROIInvert.Enable;
                    
                    % Draw ROIs
                    draw_real_ROI(self, event, roi_type);
                
                case {self.RealROIFrameX, self.RealROIFrameY}
                    % move the real space ROI according to user input
                    % on frame (x,y) spinners
                    move_real_ROI(self, event.Source, event)
                
                otherwise

                    % set state button icon color based on value
                    change_icon_background(self, self.RealROIInvert)
                        
                    % run the listener to update any/all other ROIs and
                    % the diffraction pattern
                    move_real_ROI(self, self.annotations.RealROI.Real, event)
            end

            debug_toc(self, event, "", debug_time)
        end

        % Value changed function: Mode
        function detector_mode_callbacks(self, event)
            % Function called when the mode changes, either by the user or
            % programmatically (i.e. Preview -> Alignment, or between any
            % of the available imaging modes). 
            % 
            % Parameters:
            %    self (Quant4D)
            %    event (event.EventData)
            %
            % Returns:
            %    None

            debug_time = tic;
            dmod = self.Mode.Value;

            % Enable windows
            enable_windows(self,false)
            
            % Clear ROIs on Diffraction
            clear_detectors(self);

            % Clear Real-space images if not switching to alignment or preview
            if ~ismember(dmod, ["Alignment" "Preview"])
                delete(findobj(self.ui_groups.real_axes(~contains({self.ui_groups.real_axes.Tag}, "Mask")),'Type','image'));
            end

            % Enable/Disable CoM/DPC related UI/images/buttons
            set(self.ui_groups.CoM_buttons, ...
                "Enable", any(dmod == ["CoM" "DPC"]));
            
            if ismember(dmod, ["CoM" "DPC"])
                self.DisplayImage.Items = self.ui_groups.image_name;
                self.DisplayImage.ItemsData = self.ui_groups.image_id;

                % Substitute "CoM"/"DPC" in image names, window titles and
                % button texts
                mode_prefix = dmod(1:3);
                self.DisplayImage.Items = replace(self.ui_groups.image_name, ["CoM" "DPC"], mode_prefix);
                set(self.ui_groups.image_figures, {"Name"},cellstr(self.DisplayImage.Items)')
                set(self.ui_groups.CoM_buttons, {"Text"}, cellstr(replace(get(self.ui_groups.CoM_buttons, "Text"), ["CoM" "DPC"], mode_prefix)))
            
                % show Windows tab in the Settings UI when in DPC/CoM
                self.SettingsTabGroup.SelectedTab = self.WindowsTab;
                
            else
                % Image dropdown texts
                self.DisplayImage.Items = self.ui_groups.image_name(self.ui_groups.image_type ~= "CoM");
                
                % Image dropdown values
                self.DisplayImage.ItemsData = self.ui_groups.image_id(self.ui_groups.image_type ~= "CoM");
                
                % Image windows
                set(self.ui_groups.image_figures(self.ui_groups.image_type == "CoM"), "Visible", "off")

                % show Display tab in the Settings UI when not in DPC/CoM
                self.SettingsTabGroup.SelectedTab = self.DisplayTab;
            end

            % Show primary diffraction/real-space image when mode changes unless in Preview mode
            set([self.figures.Diffraction; self.figures.Real], "Visible", dmod ~= "Preview")
            
            % Special case for Import Preview Mode
            if dmod == "Preview"
                % Keep only "Preview" image
                self.DisplayImage.Items = "Preview";
                self.DisplayImage.ItemsData = "Preview";
                
                % Hide other UIs
                set([self.MiscTab, ...
                     self.InfoTab, ...
                     self.ExportDatasetTab], ...
                    "Parent", [])

                set([self.figures.Import, ...
                     self.figures.Preview, ...
                     self.figures.Settings], ...
                    "Visible", "on")
            else
                % Note current mode
                self.common_parameters.detector_mode = self.Mode.Value;
                
                % Remove "Preview" image
                preview_index = self.DisplayImage.ItemsData == "Preview";
                self.DisplayImage.Items(preview_index) = [];
                self.DisplayImage.ItemsData(preview_index) = [];
                self.figures.Preview.Visible = "off";
                
                % Show all UIs
                set([self.MiscTab, ...
                     self.InfoTab], ...
                    "Parent", self.SettingsTabGroup)

                set(self.ExportDatasetTab, "Parent", self.SaveTabGroup)
            end

            % Define images in the saving list
            self.SaveImageList.Items = self.DisplayImage.ItemsData;
            self.SaveImageList.ItemsData = self.SaveImageList.Items;
            
            % Update Image saving prefix
            mock_UI_callbacks(self, self.SaveImagePrefix)
            
            % Update diffraction axis annotations
            mock_UI_callbacks(self, self.ShowDiffractionAxes)

            % Set detector size when transmitted beam is aligned the first time
            if isfield(self.common_parameters,'transmitted_beam_init') && ...
               ~self.common_parameters.transmitted_beam_init && ...
               dmod ~= "Alignment"
                set([self.InnerAnnularRadius; ...
                     self.OuterAnnularRadius; ...
                     self.VirtualApertureR], ...
                    {"Value"}, ...
                    {self.TransBeamR.Value; ...
                     (self.TransBeamR.Value + self.common_parameters.max_radius)/3; ...
                     self.TransBeamR.Value})
                self.common_parameters.virtual_aperture_center = self.center;
                self.common_parameters.transmitted_beam_init = true;
            end

            % Diffraction detector UI
            set(self.ui_groups.detector_ui, "Visible", "off");
            
            % Hide Math Tab
            self.MathTab.Parent = [];
            self.RealPanel.Visible = "on";
            
            switch dmod
                case "Preview"
                    self.PreviewGrid.Visible = "on";
                    self.RealPanel.Visible = "off";
                    preview_callbacks(self, event)
                
                case "Alignment"
                    self.AlignmentGrid.Visible = "on";
                    transmitted_beam_callbacks(self, event)
                
                case {"Annular", "CoM", "DPC"}
                    self.AnnularDetectorGrid.Visible = "on";
                    annular_detector_callbacks(self, event)
                    if dmod ~= "Annular" % 'CoM' OR 'DPC'
                        % show scan direction panel
                        self.ScanDirectionPanel.Visible = "on";

                        % if DPC show segmented detector panel, else hide
                        if dmod == "DPC"
                            self.SegmentedDetectorPanel.Visible = "on";
                        else
                            self.SegmentedDetectorPanel.Visible = "off";
                        end

                        % Plot ColorWheel
                        plot_image(self, event, "ColorWheel")
                        
                        % bring ColorWheel and CoM Phase Magnitude to the
                        % front
                        figure(self.figures.CoMPhMag);
                        figure(self.figures.ColorWheel)
                        
                        % Flashing to align scan direction
                        if ~self.common_parameters.scan_direction_initialized
                            flash_background(self, self.ScanDirectionGrid);
                        end
                    
                    else
                        % Hide segmented detector and scan direction panels
                        % if not in DPC or CoM
                        self.SegmentedDetectorPanel.Visible = "off";
                        self.ScanDirectionPanel.Visible = "off";
                    
                    end
                
                case "Virtual"
                    % Show Virtual aperture panel
                    self.VirtualApertureGrid.Visible = "on";
                    virtual_aperture_callbacks(self, event);
                
                case "Custom"
                    % Show custom detector panel
                    self.CustomDetectorGrid.Visible = "on";

                    % Add Math tab to the Settings UI
                    self.MathTab.Parent = self.SettingsTabGroup;

                    custom_detector_callbacks(self, event)
                    
                    % Bring the diffraction mask to the front
                    figure(self.figures.DiffractionMask)
            end

            debug_toc(self, event, "", debug_time)
        end

        % Value changed function: AnnularStep, DetectorCoordinatePosition, 
        % ...and 2 other components
        function detector_coordinates_callbacks(self, event)
            % Function called when the users selects a different coordinate
            % system ("Polar" or "Cartesian"), positioning system
            % ("Relative" or "Absolute"), or unit ("mrad" or "pixels"); as
            % well as if the user changes the annular integration step
            % size.
            % 
            % Parameters:
            %    self (Quant4D)
            %    event (event.EventData)
            %
            % Returns:
            %    None

            % "Polar" necessitates "Relative"
            switch event.Source
                case self.DetectorCoordinateSystem
                    if self.DetectorCoordinateSystem.Value == "Polar"
                        self.DetectorCoordinatePosition.Value = "Relative";
                    end
                
                case self.DetectorCoordinatePosition
                    if self.DetectorCoordinatePosition.Value == "Absolute"
                        self.DetectorCoordinateSystem.Value = "Cartesian";
                    end
            end

            % Set diffraction scale based on coordinates used
            if self.DetectorCoordinateUnit.Value == "mrad"
                self.diff_scale = self.mradPx.Value;
            else
                % "pixels" are 1:1
                self.diff_scale = 1;
            end
            
            % Set relative center of the diffraction pattern
            if self.DetectorCoordinatePosition.Value == "Relative"
                self.center_rel = self.center;
            else
                % "Absolute" is relative to 
                self.center_rel = [0 0];
            end
            
            if event.Source == self.AnnularStep
                annular_detector_callbacks(self, event)
                
            end

            % Update UI
            mock_event = struct("Source", self.DetectorCoordinateSystem, ...
                                "EventName", "UpdateCoord");

            switch self.Mode.Value
                case {'Annular' 'DPC' 'CoM'}
                    annular_detector_callbacks(self, mock_event)
                
                case "Virtual"
                    virtual_aperture_callbacks(self, mock_event)
                
                case "Custom"
                    custom_detector_callbacks(self, mock_event)
            end
        end

        % Button pushed function: SwapByteOrder, SwapDiffractionXY, 
        % ...and 1 other component
        function dataset_options_callbacks(self, event)
            % Function called when the user request a swap of data byte
            % ordering (i.e. big endian -> little endian), real space x,y
            % (i.e. [kx, ky, rx, ry] -> [kx, ky, ry, rx]), or diffraction
            % space x,y (i.e. [kx, ky, rx, ry] -> [ky, kx, rx, ry]).
            % 
            % Parameters:
            %    self (Quant4D)
            %    event (event.EventData)
            %
            % Returns:
            %    None

            switch event.Source
                case self.SwapByteOrder % Swap byte-order
                    message = "Swapping byte order ...";
                    self.tmp_variables.progress_dialog = progress_dialog(self, sprintf("\n%s\n",message), "Byte Order Swap");

                    try
                        self.data = swapbytes(self.data);
                    catch
                        if self.dataset_parameters.gpu
                            waitbar(0,self.tmp_variables.progress_dialog,message+sprintf("\nIt seems GPU has not enough memory.\nUsing CPU for this process ..."))
                            self.data = gather(self.data);
                            self.data = swapbytes(self.data);
                            self.data = gpuArray(self.data);
                        else
                            delete(self.tmp_variables.progress_dialog)
                            notification_dialog(self, "error", "It seems the system has not enough memory for this process! " + ...
                                "Maybe try to increase system's virtual memory.", "Out of Memory")
                            return
                        end
                    end
                    
                    % update data info at `self.dataset_parameters.byte_orer`
                    bo = struct("l", "b", "b", "l");
                    self.dataset_parameters.byte_orer = bo.(self.dataset_parameters.byte_orer);
                    
                    self.DatasetInfo.Value = get_import_info(self);
                    
                    mock_UI_callbacks(self, self.UpdateImages)
                    
                    delete(self.tmp_variables.progress_dialog)
                    selection = notification_dialog(self,'quest', "Is the current byte-order correct?",'Byte Order Swap',["Yes", "No. Revert"]);
                    
                    % Run the process again if selected "No ....."
                    if startsWith(selection, "No")
                        dataset_options_callbacks(self,struct("Source",self.SwapByteOrder,"EventName", ""))
                    end

                case {self.SwapDiffractionXY self.SwapRealXY}
                    % Diffraction or real-space
                    if event.Source.Tag == "Diffraction"
                        unit = "pixels";
                    else
                        % Delete all Real-space ROIs;
                        unit = "frames";
                        delete(findobj(self.ui_groups.real_axes, "Tag",'Real-space ROI'));
                        self.common_parameters.transmitted_beam_init = true;
                    end

                    % Swap X/Y dimensions
                    
                    % n_pixels_file or n_frames_file
                    self.dataset_parameters.("n_"+unit+"_file") = fliplr(self.dataset_parameters.("n_"+unit+"_file"));
                    
                    % n_pixels or n_frames
                    self.dataset_parameters.("n_"+unit) = fliplr(self.dataset_parameters.("n_"+unit));
                    
                    % pixels_start or frames_start
                    self.dataset_parameters.(unit+"_start") = fliplr(self.dataset_parameters.(unit+"_start"));
                    
                    % Re-prepare the imported data
                    import_callbacks(self, event)
                    self.DatasetInfo.Value = get_import_info(self);

                case self.PreviewButton
                    % Check data NaN/Inf, without asking to sway byte-order
                    selection = check_NaN(self, self.images.Preview, true);

                    if strcmp(selection,'Set NaNs to 0')
                        self.data(isnan(self.data(:)))=0;
                    end

                otherwise
                    self.DatasetInfo.Value = get_import_info(self);
                    
                    % Check data NaN/Inf, ask whether to sway byte-order
                    selection = check_NaN(self, self.images.Diffraction, false);
                    if strcmp(selection,'Set NaNs to 0')
                        self.data(isnan(self.data(:)))=0;
                    end

            end
        end

        % Callback function: PreviewButton, PreviewFrameX, PreviewFrameY, 
        % ...and 9 other components
        function preview_callbacks(self, event)
            % Function called when the user request to preview a
            % diffraction pattern before importing.
            % 
            % Parameters:
            %    self (Quant4D)
            %    event (event.EventData)
            %
            % Returns:
            %    None

            switch event.Source
                case self.Mode % Entering mode
                    cla(self.image_axes.Preview);
                    
                    % Clear previous preview
                    self.images.Preview = [];
                    
                    % Enable windows
                    enable_windows(self,true)

                case self.UpdateImages % Update image
                    % Preview
                    mock_UI_callbacks(self, self.PreviewButton)

                case {self.PreviewFrameX self.PreviewFrameY} % Preview Frame X/Y
                    % Force Frame X/Y minimum as 1
                    event.Source.Value = max(event.Value, 1);
                    
                    % Preview
                    mock_UI_callbacks(self, self.PreviewButton)

                case {self.PreviewFrame_1_1;  self.PreviewFrame_X2_1;  self.PreviewFrame_X_1; % Preview location buttons
                      self.PreviewFrame_1_Y2; self.PreviewFrame_X2_Y2; self.PreviewFrame_X_Y2;
                      self.PreviewFrame_1_Y;  self.PreviewFrame_X2_Y;  self.PreviewFrame_X_Y}
                    
                    % Get limits from Frame X/Y UIs
                    X = self.PreviewFrameX.Limits(2);
                    Y = self.PreviewFrameY.Limits(2);

                    % Evaluate the text on buttons (i.e. [X/2, Y])
                    xy = min(ceil(eval(event.Source.Text)), [X Y]);
                    
                    % Set values of Frame X/Y UIs
                    set([self.PreviewFrameX, self.PreviewFrameY], ...
                        {"Value"}, ...
                        {xy(1); xy(2)});
                    
                    % Preview
                    mock_UI_callbacks(self, self.PreviewButton)

                case self.PreviewButton
                    cla(self.image_axes.Preview);
                    
                    % Get parameters
                    import_callbacks(self, event);
                    params = self.tmp_variables.Preview;
                    frame_x = self.PreviewFrameX.Value-1;
                    frame_y = self.PreviewFrameY.Value-1;

                    if ~isempty(params)
                        n_pixels_x = params.n_pixels_file(1);
                        n_pixels_y = params.n_pixels_file(2);
                        n_frames_x = params.n_frames_file(1);
                        n_frames_y = params.n_frames_file(2);

                        self.common_parameters.PreviewAxLim = [0.51, n_pixels_x + .49, 0.51, n_pixels_y + .49];
                        set(self.image_axes.Preview, ...
                            "XLim", self.common_parameters.PreviewAxLim(1:2), ...
                            "YLim", self.common_parameters.PreviewAxLim(3:4));

                        try
                            if ~isempty(params.h5ds) % Preview HDF5
                                file_id = H5F.open(params.file_path);
                                dataset_id = H5D.open(file_id, params.h5ds);
                                file_space_id = H5S.create_simple(4, [n_frames_y n_frames_x n_pixels_y n_pixels_x], []);
                                memory_space_id = H5S.create_simple(2, [n_pixels_y n_pixels_x], []);
                                
                                % C-like array indices for H5 low-level APIs
                                H5S.select_hyperslab(file_space_id, 'H5S_SELECT_SET', [frame_y frame_x 0 0], [], [], [1 1 n_pixels_y n_pixels_x]);
                                frame = H5D.read(dataset_id, 'H5ML_DEFAULT', memory_space_id, file_space_id, 'H5P_DEFAULT');

                            else % Preview others
                                file_id = fopen(params.file_path, "r");
                                
                                % Move cursor to end of the to-be-read frame, for testing
                                err = fseek(file_id, params.offset + (1 + frame_x + frame_y*n_frames_x)*(params.frame_header + n_pixels_x*n_pixels_y*params.byte_size + params.frame_footer), 'bof');
                                
                                if err == -1
                                    throw(MException("",""));
                                end
                                
                                % Move cursor to start of the to-be-read frame
                                fseek(file_id, -(n_pixels_x*n_pixels_y*params.byte_size + params.frame_footer), 'cof');
                                frame = fread(file_id, [n_pixels_x, n_pixels_y], params.data_type, 0, params.byte_orer);
                            end

                            self.images.Preview = frame;
                            
                            % Plot image
                            plot_image(self, event, "Preview")
                            
                            % Check NaN
                            dataset_options_callbacks(self, event)
                        
                        catch
                            notification_dialog(self, ...
                                                "error", ...
                                                "Errors occurred during preview! Maybe reached end-of-file.", ...
                                                "Error during Preview!");

                        end
                        % Close opened handles
                        try
                            if ~isempty(params.h5ds)
                                H5S.close(memory_space_id);
                                H5S.close(file_space_id);
                                H5D.close(dataset_id);
                                H5F.close(file_id);
                            else
                                fclose(file_id);
                            end
                        catch
                        end
                    end
            end

        end

        % Callback function: Alpha, TBAutoAlign, TBCrossAlign, TransBeamR, 
        % ...and 12 other components
        function transmitted_beam_callbacks(self, event)
            % Function called when the user interacts with UI elements on
            % the `Alignment` tab of the main UI (i.e. convergence angle,
            % transmitted beam x/y/radius, AutoAlign, etc.)
            % 
            % Parameters:
            %    self (Quant4D)
            %    event (event.EventData)
            %
            % Returns:
            %    None

            debug_time = tic;
            switch event.Source
                case self.Mode % Entering mode
                    % Create transmitted beam annotation, allow for disk as large as the entire diffraction pattern
                    self.annotations.TransBeam = drawcircle(self.image_axes.Diffraction, ...
                                                           "Center", self.center, ...
                                                           "Radius", self.TransBeamR.Value, ...
                                                           "Color", "b",...
                                                           "DrawingArea", "unlimited", ...
                                                           "Deletable", false, ...
                                                           "EdgeAlpha", 0.7, ...
                                                           "FaceAlpha", 0, ...
                                                           "Tag", "TransBeamAnnot");
                    self.annotations.TransBeam.UserData.Move = addlistener(self.annotations.TransBeam, "MovingROI", @self.move_transmitted_beam);
                    addlistener(self.annotations.TransBeam, "ROIMoved", @self.move_transmitted_beam);
                    
                    % Select `Diffraction` image
                    mock_UI_callbacks(self, self.DisplayImage, "Diffraction");
                    
                    % If this is the initializing alignment, then do swap byte check and auto-align
                    if ~self.common_parameters.transmitted_beam_init
                        dataset_options_callbacks(self, event);
                        auto_align(self);
                    end

                    % Enable windows
                    enable_windows(self,true)
                
                case self.UpdateImages
                    % Update images
                    % Create a summed image of all diffraction patterns simply for alignment and calibration
                    self.images.DiffractionMask = ones(self.dataset_parameters.n_pixels, self.dataset_parameters.data_type);
                    self.images.Real = gather(reshape(reshape(self.images.DiffractionMask,1,[])*self.data, self.dataset_parameters.n_frames));
                
                case self.TBAutoAlign
                    % Auto-align
                    auto_align(self);
                
                case self.TBCrossAlign
                    % Align transmitted beam via two crossed lines
                    cross_align(self);
            end
            % Update dependent variables
            move_transmitted_beam(self, event.Source, event);

            debug_toc(self, event, "", debug_time)
        end

        % Callback function: AnnularRadiusLink, AutoCurl, 
        % ...and 20 other components
        function annular_detector_callbacks(self, event)
            % Function called when the user interacts with UI elements on
            % the `Annular/Round`, `Segmented (DPC)`, and `Center of Mass`
            % tabs of the main UI (i.e. inner/outer annular angles,
            % segmented detector controls, scan direction alignment, etc.)
            % 
            % Parameters:
            %    self (Quant4D)
            %    event (event.EventData)
            %
            % Returns:
            %    None

            debug_time = tic;
            
            % Absolute pixel coordinates of central beam; only changes in
            % `transmitted_beam_callbacks()`
            transmitted_beam_center = self.center;
            
            % Detector mode; when changed this callback will be called
            dmod = self.Mode.Value;

            % set state button icon color based on value
            change_icon_background(self, self.FlipScanDirectionY)
            change_icon_background(self, self.AnnularRadiusLink)

            switch event.Source
                case self.DetectorCoordinateSystem % Change coordinate options
                    % set UI limits
                    limitAnnUI()

                case {self.Mode, self.AnnularStep} % Entering current mode
                    % set UI limits
                    limitAnnUI()

                    % Lock scan directions first upon entering annular modes
                    self.ScanDirectionLock.Value = false;
                    
                    % UI enable/disable
                    enableAnnUI()
                    
                    % Update annular integral mask
                    integrate_annular()
                    
                    % Draw detectors
                    draw_annular_detector();

                    % Draw segmented detectors if in DPC mode
                    if dmod == "DPC"
                        draw_segmented_detector();
                    end
                    
                    % Update UI/ROIs
                    move_annular_detector(event.Source, event)
                    
                    % Enable windows
                    enable_windows(self,true)

                case {self.InnerAnnularRadius self.InnerAnnularRadiusSpinner ...
                      self.OuterAnnularRadius self.OuterAnnularRadiusSpinner ...
                      self.DetectorRotationSlider self.DetectorRotationSpinner ...
                      self.ScanDirectionSlider self.ScanDirectionSpinner ...
                      self.AnnularRadiusLink self.NSeg self.NRung ...
                      self.FlipScanDirectionY self.UpdateImages}
                    % Update UI/ROIs
                    move_annular_detector(event.Source, event)

                case self.ScanDirectionLock
                    if self.ScanDirectionLock.Value
                        self.ScanDirectionLock.Icon = 'unlock.png'; 
                    else
                        self.ScanDirectionLock.Icon = 'lock.png';
                    end

                    % Flag scan directions as aligned
                    self.common_parameters.scan_direction_initialized = true;
                    
                    % Enable/Disable GUI elements
                    enableAnnUI()
                    
                    % Try to remove existing scan direction ROIs
                    delete(findobj(self.image_axes.Diffraction, "Tag",'ScanDirAnnot'));
                    
                    % Draw annotations
                    if self.ScanDirectionLock.Value
                        draw_scan_direction();
                    end

                    % Update diffraction axes annotations
                    mock_UI_callbacks(self, self.ShowDiffractionAxes)

                case self.AutoCurl
                    % display a progress dialog for user
                    self.tmp_variables.progress_dialog = progress_dialog(self, sprintf('Automatically estimating scan \norientation my minimizing curl...'), "Auto scan orientation");
                    
                    % minimize curl and update UI/ROIs twice for precision
                    for ii=1:2
                        minimize_curl()
                        move_annular_detector(event.Source, event)
                    end
                    
                    % automatically close out the scan direction routine
                    self.ScanDirectionLock.Value = false;
                    annular_detector_callbacks(self, struct("Source",self.ScanDirectionLock, "EventName", "ValueChanged", "Value", false, "PreviousValue", true))

                    % Close progress bar and Enable panel objects
                    delete(self.tmp_variables.progress_dialog);
            end

            debug_toc(self, event, "", debug_time)


            %% Sub functions
            % Function to try to automatically find angle between
            % diffraction space and real space by minimizing center of mass
            % curl
            function minimize_curl()
                % find the curl for all angles
                CoM = zeros([2,fliplr(self.dataset_parameters.n_frames)]);
                CoM(1,:,:) = self.images.CoMX';
                CoM(2,:,:) = self.images.CoMY';

                if all(isnan(CoM(:)))
                    notification_dialog(self, ...
                                        "warn", ...
                                        "CoM is all NaNs! This caused " + ...
                                        "minimize_curl() to fail. Try " + ...
                                        "changing the CoM detector and " + ...
                                        "repeating.", ...
                                        "Automatic Curl Minimization Failed");
                    return
                end

                % set up angles
                theta = reshape(0:359,[1,1,360]) + self.ScanDirectionSlider.Value;
                R_applied = [cosd(-self.ScanDirectionSpinner.Value) -sind(-self.ScanDirectionSpinner.Value);
                             sind(-self.ScanDirectionSpinner.Value)  cosd(-self.ScanDirectionSpinner.Value)];
                R = permute([cosd(theta) -sind(theta); ...
                             sind(theta)  cosd(theta)],[3,1,2]);
                
                % undo rotation by ScanDir angle via R_applied
                rotCoM = tensorprod(R,tensorprod(R_applied,CoM,2,1),3,1);
                
                %rotCoM = tensorprod(R,CoM,3,1);
                [dFx_dx,dFx_dy] = gradient(permute(squeeze(rotCoM(:,1,:,:)),[2,3,1]));
                [dFy_dx,dFy_dy] = gradient(permute(squeeze(rotCoM(:,2,:,:)),[2,3,1]));
                cav = squeeze(mean(abs(0.5*(dFy_dx-dFx_dy)),[1,2]));
                div = squeeze(sum(dFx_dx + dFy_dy,[1,2]));
                
                % try transpose
                [dFx_dx,dFx_dy] = gradient(permute(squeeze(rotCoM(:,1,:,:)),[3,2,1]));
                [dFy_dx,dFy_dy] = gradient(permute(squeeze(rotCoM(:,2,:,:)),[3,2,1]));
                cav(:,2) = squeeze(mean(abs(0.5*(dFy_dx-dFx_dy)),[1,2]));
                div(:,2) = squeeze(sum(dFx_dx + dFy_dy,[1,2]));

                % refine theta value
                thetaIdx = find(cav==min(cav(:)));
                if numel(thetaIdx)>1
                    [~,idx] = max(div(thetaIdx));
                    thetaIdx = thetaIdx(idx);
                end

                [thetaIdx,transVal] = ind2sub(size(cav),thetaIdx);
                transVal = transVal - 1;
                thetaCoarse = theta(thetaIdx)-self.ScanDirectionSlider.Value;
                theta = reshape(thetaCoarse-1:0.1:thetaCoarse+1,[1,1,21]);
                R = permute([cosd(theta) -sind(theta);sind(theta) cosd(theta)],[3,1,2]);
                rotCoM = tensorprod(R,CoM,3,1);

                if transVal==1
                    [~,dFx_dy] = gradient(permute(squeeze(rotCoM(:,1,:,:)),[3,2,1]));
                    [dFy_dx,~] = gradient(permute(squeeze(rotCoM(:,2,:,:)),[3,2,1]));
                
                else
                    [~,dFx_dy] = gradient(permute(squeeze(rotCoM(:,1,:,:)),[2,3,1]));
                    [dFy_dx,~] = gradient(permute(squeeze(rotCoM(:,2,:,:)),[2,3,1]));
                end
                
                cav = squeeze(mean(abs(0.5*(dFy_dx-dFx_dy)),[1,2]));
                thetaVal = theta(cav==min(cav)) + self.ScanDirectionSlider.Value;
                
                self.ScanDirectionSlider.Value = wrapTo180(thetaVal);
                self.ScanDirectionSpinner.Value = wrapTo180(thetaVal);
                self.FlipScanDirectionY.Value = xor(self.FlipScanDirectionY.Value,transVal);
            end

            % Function to update Annular detector UI limits/labels when coordinate options change
            function limitAnnUI()
                set([self.AnnRi_NFLabel self.AnnRo_NFLabel], ...
                    'Text', ...
                    self.DetectorCoordinateUnit.Value)
                set([self.InnerAnnularRadiusSpinner; ...
                     self.OuterAnnularRadiusSpinner], ...
                    "Limits", ...
                    [0 self.common_parameters.max_radius*self.diff_scale], ...
                    'Step', ...
                    self.AnnularStep.Value)
                inner_radius = clip(round(self.InnerAnnularRadius.Value*self.mradPx.Value/self.AnnularStep.Value)*self.AnnularStep.Value, 0, self.InnerAnnularRadius.Limits(2));
                outer_radius = clip(round(self.OuterAnnularRadius.Value*self.mradPx.Value/self.AnnularStep.Value)*self.AnnularStep.Value, 0, self.OuterAnnularRadius.Limits(2));
                set_external_source(self, event, ...
                                    [self.InnerAnnularRadiusSpinner; ...
                                     self.OuterAnnularRadiusSpinner; ...
                                     self.InnerAnnularRadius; ...
                                     self.OuterAnnularRadius], ...
                                    {"Value"}, ...
                                    {inner_radius; ...
                                     outer_radius; ...
                                     min(inner_radius/self.mradPx.Value, self.common_parameters.max_radius); ...
                                     min(outer_radius/self.mradPx.Value, self.common_parameters.max_radius)}); 
            end

            % Function to enable/disable UI
            function enableAnnUI()
                % Enable segmented panel
                set(self.SegmentedDetectorGrid.Children, "Enable",switch_on_off(self, dmod == "DPC"))

                % Change Enable state of scan direction UIs, except `self.ScanDirectionLock`
                set(setdiff(self.ScanDirectionGrid.Children,self.ScanDirectionLock), ...
                    "Enable", ...
                    switch_on_off(self, self.ScanDirectionLock.Value))

                % enable ScanDirectionLock if in CoM/DPC mode, else disable
                self.ScanDirectionLock.Enable = ismember(dmod, ["CoM" "DPC"]);
                
                % Highlight to align Scanning Direction
                if self.ScanDirectionLock.Enable && ~self.common_parameters.scan_direction_initialized
                    background_color = self.sys_constants.warning_color;
                else
                    background_color = self.sys_constants.background_color;
                end
                
                % Set scan direction panel color
                self.ScanDirectionGrid.BackgroundColor = background_color;
            end

            % Function to live update annular/round/segmented detectors
            function move_annular_detector(source, event)
                inner_radius = self.InnerAnnularRadius.Value;
                outer_radius = self.OuterAnnularRadius.Value;
                detector_rotation = self.DetectorRotationSlider.Value;
                scan_direction = self.ScanDirectionSlider.Value;
                flip_scan_y = 1-2*self.FlipScanDirectionY.Value;

                % Cases for different detectors
                if contains(source.Tag,'AnnDetr')
                    moveAnnR()
                elseif contains(source.Tag,'SegDetr')
                    move_segmented_detector()
                elseif contains(source.Tag,'ScanDir')
                    move_scan()
                else % self.Mode self.UpdateImages
                    moveAnnR();
                    
                    % Update scan directions as well
                    if self.ScanDirectionLock.Value
                        move_scan();
                    end
                end

                % Whether to update images
                if to_update_image(self, event)
                    % Skip calculations of new BF/DF `self.images.Real` if
                    % annular radii are not changed
                    if is_different_to_previous(self,'AnnR',[inner_radius outer_radius]) || is_static_event(self, event)
                        % 2D matrix of distances from central beam, X/Y on the 1st/2nd dimensions
                        mask_ann = sqrt( ((1:self.dataset_parameters.n_pixels(1))-transmitted_beam_center(1))'.^2 + ((1:self.dataset_parameters.n_pixels(2))-transmitted_beam_center(2)).^2 );
                        mask_ann = mask_ann >= inner_radius & mask_ann <= outer_radius;
                        self.images.DiffractionMask = mask_ann;
                        self.masks.annular = mask_ann;
                        
                        % The plus 1 is because the array begins at 0, but is 1-indexed.
                        adf_inner = clip(round(inner_radius*self.mradPx.Value/self.AnnularStep.Value) + 1, 1, self.common_parameters.max_radius);
                        adf_outer = clip(round(outer_radius*self.mradPx.Value/self.AnnularStep.Value) + 1, 1, self.common_parameters.max_radius);
                        self.images.Real = gather(sum(self.images.annular_images(:, :,adf_inner:adf_outer), 3,'omitnan'));
                    end

                    % CoM/DPC calculations; skip if parameters unchanged
                    if ismember(dmod, ["CoM", "DPC"])
                        if is_different_to_previous(self,'CoM_P',[inner_radius outer_radius scan_direction flip_scan_y detector_rotation]) || is_static_event(self, event)
                            calculate_CoM();
                        end
                    end
                    % Update images
                    plot_all_patterns(self, event)
                end

                % Sub sub functions
                % Sub sub function for annular radii
                function moveAnnR()
                    scale = self.diff_scale;
                    
                    % given the AnnularStep (in mrad), round detector step
                    % size (in pixels)
                    annular_pixel_step = self.AnnularStep.Value/self.mradPx.Value;

                    switch source
                        case self.annotations.inner_annulus
                            inner_radius = round(event.CurrentRadius/annular_pixel_step) * annular_pixel_step;
                        case self.annotations.outer_annulus
                            outer_radius = round(event.CurrentRadius/annular_pixel_step) * annular_pixel_step;
                        case self.InnerAnnularRadius
                            inner_radius = round(event.Value/annular_pixel_step) * annular_pixel_step;
                        case self.OuterAnnularRadius
                            outer_radius = round(event.Value/annular_pixel_step) * annular_pixel_step;
                        case self.InnerAnnularRadiusSpinner
                            inner_radius = round(event.Value/self.AnnularStep.Value)*self.AnnularStep.Value/self.diff_scale;
                        case self.OuterAnnularRadiusSpinner
                            outer_radius = round(event.Value/self.AnnularStep.Value)*self.AnnularStep.Value/self.diff_scale;
                        otherwise % {self.AnnularRadiusLink, self.Mode self.UpdateImages}
                            self.common_parameters.detector_width = outer_radius - inner_radius;
                    end

                    % If inner/outer detector radii are linked
                    if self.AnnularRadiusLink.Value
                        detector_width = self.common_parameters.detector_width;
                        if contains(source.Tag,'RI')
                            inner_radius = min(inner_radius, self.common_parameters.max_radius-detector_width);
                            outer_radius = inner_radius + detector_width;
                        elseif contains(source.Tag,'RO')
                            outer_radius = max(outer_radius, detector_width);
                            inner_radius = outer_radius - detector_width;
                        end
                    end
                    
                    % Restrict Inner/Outer radii
                    if contains(source.Tag,'RI')
                        inner_radius = clip(inner_radius, 0, outer_radius);
                    elseif contains(source.Tag,'RO')
                        outer_radius = clip(outer_radius, inner_radius, self.common_parameters.max_radius);
                    end
                    
                    % Update ROI
                    set([self.annotations.inner_annulus;self.annotations.outer_annulus], ...
                        {'Radius'}, {inner_radius;outer_radius})
                    
                    % Update UI with Limits check
                    set_external_source(self, event, ...
                                        [self.InnerAnnularRadius; ...
                                         self.OuterAnnularRadius; ...
                                         self.InnerAnnularRadiusSpinner; ...
                                         self.OuterAnnularRadiusSpinner], ...
                                        {"Value"}, ...
                                        {inner_radius; ...
                                         outer_radius; ...
                                         min(inner_radius*scale, self.common_parameters.max_radius*scale); ...
                                         min(outer_radius*scale, self.common_parameters.max_radius*scale)});
                    
                    % Update saving prefix
                    if is_static_event(self, event)
                        mock_UI_callbacks(self, self.SaveImagePrefix)
                    end

                    % Whether to update segments as well
                    if dmod == "DPC"
                        move_segmented_detector();
                    end
                end

                % Sub sub function for segmented detector
                function move_segmented_detector()
                    switch source
                        case {self.DetectorRotationSlider self.DetectorRotationSpinner}
                            detector_rotation = event.Value;
                        case self.annotations.SegDetrP0
                            rxy = (event.CurrentPosition-transmitted_beam_center);
                            detector_rotation = atan2d(rxy(2), rxy(1));
                        case {self.NSeg self.NRung}
                            draw_segmented_detector();
                    end

                    % Update UI
                    set_external_source(self, event, [self.DetectorRotationSlider, self.DetectorRotationSpinner], "Value",detector_rotation)
                    
                    % Update ROI
                    pos0 = [inner_radius, 0; outer_radius, 0; (inner_radius+outer_radius)/2, 0]*rotation_matrix(self, detector_rotation)+transmitted_beam_center;
                    set([self.annotations.SegDetrL0 self.annotations.SegDetrP0],{"Position"},{pos0(1:2,:);pos0(3,:)});
                    set(self.annotations.segmented_detector_circle,{'Radius'}, num2cell((1:self.NRung.Value-1)'/self.NRung.Value*(outer_radius - inner_radius) + inner_radius))
                    
                    % Use 3D matrix for positions, then put the 1st/2nd dimensions (2x2 array) in each cell for each segment
                    t = detector_rotation+360*(reshape(1:self.NSeg.Value,1,1,[])-.5)/self.NSeg.Value;
                    set(self.annotations.segmented_detector_line,{"Position"},squeeze(num2cell([inner_radius;outer_radius].*[cosd(t) sind(t)]+transmitted_beam_center, 1:2)))
                end

                % Sub sub function for scan directions
                function move_scan()
                    % Use polar relative pixel coordinates for calculation
                    svx = self.annotations.ScanDir.xc.Center - transmitted_beam_center;
                    svy = self.annotations.ScanDir.yc.Center - transmitted_beam_center;

                    switch source
                        case self.annotations.ScanDir.xc
                            svx = event.CurrentCenter - transmitted_beam_center;
                            scan_direction = atan2d(svx(2), svx(1));
                        case self.annotations.ScanDir.yc
                            svy = (event.CurrentCenter - transmitted_beam_center)*flip_scan_y;
                            scan_direction = -atan2d(svy(1), svy(2));
                        case {self.ScanDirectionSlider self.ScanDirectionSpinner}
                            scan_direction = event.Value;
                        case self.FlipScanDirectionY
                    end

                    % Convert back to Cartesian absolute pixel coordinates for annotations
                    [x1,y1] = pol2cart(deg2rad(scan_direction), sqrt(sum(svx.^2)));
                    sp1 = [x1 y1] + transmitted_beam_center;
                    [x2,y2] = pol2cart(deg2rad(scan_direction+90*flip_scan_y), sqrt(sum(svy.^2)));
                    sp2 = [x2 y2] + transmitted_beam_center;
                    
                    % Not limiting annotation positions
                    set([self.annotations.ScanDir.xl self.annotations.ScanDir.yl],{"Position"},{[transmitted_beam_center;sp1];[transmitted_beam_center;sp2]})
                    set_external_source(self, event, [self.annotations.ScanDir.xc, self.annotations.ScanDir.yc],{"Center"},{sp1;sp2})
                    set_external_source(self, event, [self.ScanDirectionSlider, self.ScanDirectionSpinner], "Value",scan_direction)
                end
            end

            % Function to draw annular/round/segmented detectors
            function draw_annular_detector()
                % delete any annular detector annotations
                delete(findobj(self.image_axes.Diffraction,'-regexp', "Tag",'AnnDetrAnnot'))
                
                % draw inner and outer circles
                self.annotations.inner_annulus = drawcircle(self.image_axes.Diffraction, ...
                                                           "Center", transmitted_beam_center, ...
                                                           "Radius", 1, ...
                                                           "Color", "r", ...
                                                           "Tag", "AnnDetrAnnot RI");
                self.annotations.outer_annulus = drawcircle(self.image_axes.Diffraction, ...
                                                           "Center", transmitted_beam_center, ...
                                                           "Radius", 2, ...
                                                           "Color", "m", ...
                                                           "Tag", "AnnDetrAnnot RO");
                
                % add listener for live update during user interaction
                addlistener([self.annotations.inner_annulus, ...
                             self.annotations.outer_annulus], ...
                            "MovingROI", @move_annular_detector);
                
                u.Move = addlistener([self.annotations.inner_annulus, ...
                                      self.annotations.outer_annulus], ...
                                     "ROIMoved", @move_annular_detector);

                % set properties for inner and out annulus annotations
                set([self.annotations.inner_annulus self.annotations.outer_annulus], ...
                    "FaceAlpha", 0, ...
                    "FaceSelectable", 0, ...
                    "LineWidth", 4, ...
                    "DrawingArea", "unlimited", ...
                    "Deletable", 0, ...
                    "InteractionsAllowed", "reshape", ...
                    "UserData", u);
            end

            % Function to draw segmented annotations
            function draw_segmented_detector()
                % delete any old segmented detector annotations
                delete(findobj(self.image_axes.Diffraction, "Tag",'SegDetrAnnot'))
                
                self.annotations.segmented_detector_circle = gobjects(self.NRung.Value-1,1);
                self.annotations.segmented_detector_line = gobjects(self.NSeg.Value,1);

                % plot the lines between segments
                for i = 1:self.NSeg.Value
                    self.annotations.segmented_detector_line(i) = drawline(self.image_axes.Diffraction, ...
                                                                          "Position", [0 1; 0 1] + transmitted_beam_center, ...
                                                                          "Color", "b", ...
                                                                          "LineWidth", 2);
                end
                % Zero-degree line
                self.annotations.SegDetrL0 = drawline(self.image_axes.Diffraction, ...
                                                     "Position", [transmitted_beam_center;transmitted_beam_center], ...
                                                     "Color", "w", ...
                                                     "StripeColor", "k", ...
                                                     "LineWidth", 1.5, ...
                                                     "EdgeAlpha", 0.7);

                % plot the circles between rungs
                for i = 1:self.NRung.Value - 1
                    self.annotations.segmented_detector_circle(i) = drawcircle(self.image_axes.Diffraction, ...
                                                                              "Center", transmitted_beam_center, ...
                                                                              "Radius", 1, ...
                                                                              "Color", "y", ...
                                                                              "LineWidth", 2, ...
                                                                              "FaceAlpha", 0, ...
                                                                              "FaceSelectable", false);
                end
                
                % Zero-degree point
                self.annotations.SegDetrP0 = drawpoint(self.image_axes.Diffraction, ...
                                                      "Position", transmitted_beam_center, ...
                                                      "Color", "w", ...
                                                      "LabelTextColor", "w", ...
                                                      "LabelAlpha", 0, ...
                                                      "Label", "0", ...
                                                      "Deletable", 0, ...
                                                      "Tag", "SegDetrAnnot");
                
                % add listeners to segment annotations
                addlistener(self.annotations.SegDetrP0, "MovingROI", @move_annular_detector);
                self.annotations.SegDetrP0.UserData.Move = addlistener(self.annotations.SegDetrP0, "ROIMoved", @move_annular_detector);
                
                % set segment annotation parameters
                set([self.annotations.SegDetrL0; ...
                     self.annotations.segmented_detector_circle; ...
                     self.annotations.segmented_detector_line], ...
                    "InteractionsAllowed", "none", ...
                    "Tag", "SegDetrAnnot");
            end

            % Function to draw Scan Direction alignment annotations
            function draw_scan_direction()
                p1 = transmitted_beam_center+[self.common_parameters.max_radius/2 0];
                p2 = transmitted_beam_center+[0 self.common_parameters.max_radius/2];
                
                self.annotations.ScanDir.xl = drawline(self.image_axes.Diffraction, ...
                                                      "Position", [transmitted_beam_center;p1], ...
                                                      "Color","r", ...
                                                      'LabelTextColor',"r", ...
                                                      'Label','Scan X');

                self.annotations.ScanDir.yl = drawline(self.image_axes.Diffraction, ...
                                                      "Position", [transmitted_beam_center;p2], ...
                                                      "Color", 'g', ...
                                                      'LabelTextColor', 'g', ...
                                                      'Label', 'Scan Y');

                self.annotations.ScanDir.xc = drawcircle(self.image_axes.Diffraction, ...
                                                        "Center", p1, ...
                                                        'Radius', self.TransBeamR.Value);

                self.annotations.ScanDir.yc = drawcircle(self.image_axes.Diffraction, ...
                                                        "Center", p2, ...
                                                        'Radius', self.TransBeamR.Value);
                
                % add listeners to scan direction annotations
                addlistener([self.annotations.ScanDir.xc; ...
                             self.annotations.ScanDir.yc], ...
                            "MovingROI", @move_annular_detector);
                u.Move = addlistener([self.annotations.ScanDir.xc; ...
                                      self.annotations.ScanDir.yc], ...
                                     "ROIMoved", @move_annular_detector);

                % set scan direction annotation parameters
                set([self.annotations.ScanDir.xc; ...
                     self.annotations.ScanDir.yc], ...
                    "Color", [0 0.5 1], ...
                    "FaceAlpha", 0, ...
                    "UserData",u)
                set([self.annotations.ScanDir.xl; ...
                     self.annotations.ScanDir.yl], ...
                    "MarkerSize", 1, ...
                    "LineWidth",1, ...
                    "LabelAlpha",0, ...
                    "InteractionsAllowed", "none")
                set([self.annotations.ScanDir.xc; ...
                     self.annotations.ScanDir.yc; ...
                     self.annotations.ScanDir.xl; ...
                     self.annotations.ScanDir.yl], ...
                    "Deletable", false, ...
                    "DrawingArea", "unlimited", ...
                    "Tag", "ScanDirAnnot")

                % update annular detector
                move_annular_detector(event.Source, event)
            end

            % Integrate the annular detector for the primary real-space
            % pattern `self.Axes.Real` with step size self.AnnularStep.Value
            function integrate_annular()
                debug_time = tic;
                
                % Rerun the annular integration based on the newly aligned location of the transmitted disk
                message = "Generating radial masks (takes a while) ...";
                
                if is_different_to_previous(self,'B0',self.center) || (event.Source == self.AnnularStep && ~strcmp(self.Mode.Value,'Alignment'))
                    self.tmp_variables.progress_dialog = progress_dialog(self, sprintf("\n%s\n",message), "Annular Integration");
                    
                    % Make pixel array for mask
                    [ygrid, xgrid] = meshgrid(1:self.dataset_parameters.n_pixels(2), 1:self.dataset_parameters.n_pixels(1));
                    
                    % Integrate in self.AnnularStep (mrad) increments all the way out to the furthest corner; put these on the 3rd dimension
                    dist = reshape(0:self.AnnularStep.Value/self.mradPx.Value:self.common_parameters.max_radius, 1, 1, []);
                    mask_ann = sqrt((xgrid-self.center(1)).^2 + (ygrid-self.center(2)).^2);
                    mask_ann = reshape(mask_ann >= dist & mask_ann < dist+self.AnnularStep.Value/self.mradPx.Value, [], numel(dist))';
                    mask_ann = cast(mask_ann,self.dataset_parameters.data_type);
                    
                    % Multiply data by the annular masks
                    try
                        self.images.annular_images = reshape((mask_ann*self.data)', self.dataset_parameters.n_frames(1), self.dataset_parameters.n_frames(2), []);
                    catch ME
                        if self.dataset_parameters.gpu
                            waitbar(0,self.tmp_variables.progress_dialog,message+sprintf("\nIt seems the GPU does not have enough memory.\nUsing CPU for this process ..."))
                            self.images.annular_images = reshape((mask_ann*gather(self.data))', self.dataset_parameters.n_frames(1), self.dataset_parameters.n_frames(2), []);
                            try 
                                % Move the integrated images to GPU
                                self.images.annular_images = gpuArray(self.images.annular_images);
                            catch
                            end
                        else
                            delete(self.tmp_variables.progress_dialog)
                            notification_dialog(self, ...
                                                "error", ...
                                                "It seems the system has not enough memory for this process! " ...
                                                 + "Maybe try to increase system's virtual memory.", ...
                                                "Out of Memory")
                            rethrow(ME)
                        end
                    end

                    % Close progress window
                    delete(self.tmp_variables.progress_dialog);
                end

                debug_toc(self, [], "", debug_time)
            end

            % Calculate the CoM images
            function calculate_CoM()
                debug_time = tic;
                if ~isfield(self.masks, "annular")
                    return;
                end

                inner_radius = self.InnerAnnularRadius.Value;
                outer_radius = self.OuterAnnularRadius.Value;
                scan_direction = self.ScanDirectionSlider.Value;
                flip_scan_y = 1-2*self.FlipScanDirectionY.Value;
                detector_rotation = self.DetectorRotationSlider.Value;

                [CoMX, CoMY] = integrate_CoM();
                self.images.CoMX = CoMX;
                self.images.CoMY = CoMY;

                % CoM magnitude is the length of the vector -- in mrad
                self.images.CoMMag = sqrt(CoMX.^2 + CoMY.^2);
                self.images.CoMMagNorm = rescale(self.images.CoMMag);
                
                % CoM angle was calculated from the arctangent of the difference images (CoMX and CoMY)
                self.images.CoMPh = atan2(CoMY,CoMX);
                
                % Adjust atan2 range from [-pi/2:pi/2) to [0:2pi)
                self.images.CoMPh(self.images.CoMPh < 0) = self.images.CoMPh(self.images.CoMPh < 0) + 2*pi;
                self.images.CoMPhMag = self.images.CoMPh;

                % Make iCoM/iDPC and dCoM/dDPC images - based on maths from Lazic et al.,
                % (https://doi.org/10.1016/j.ultramic.2015.10.011)
                %         [ky, kx] = meshgrid(floor(-self.dataset_parameters.n_framesY/2):floor(-self.dataset_parameters.n_framesY/2)+self.dataset_parameters.n_framesY-1, ...
                %           floor(-self.dataset_parameters.n_framesX/2):floor(-self.dataset_parameters.n_framesX/2)+self.dataset_parameters.n_framesX-1);
                [ky, kx] = meshgrid((1:self.dataset_parameters.n_frames(2)) - self.common_parameters.real_space_center(2), ...
                                    (1:self.dataset_parameters.n_frames(1)) - self.common_parameters.real_space_center(1));

                kr = sqrt(kx.^2+ky.^2);
                
                % a zero pixel will mess up the maths here
                kr(kr == 0) = 1;
                
                % prepare for FFTs
                kx = fftshift(kx);
                ky = fftshift(ky);
                kr = fftshift(kr);

                % generate band-pass filter 
                bandpass_filter = kr<=self.BandpassFilterHigh.Value & kr>=self.BandpassFilterLow.Value;

                % integrated center of mass
                self.images.iCoM = real(ifft2(kx.*fft2(CoMX)./(2*pi*1j*kr.^2).*bandpass_filter) + ...
                                       ifft2(ky.*fft2(CoMY)./(2*pi*1j*kr.^2).*bandpass_filter));
                
                % differential center of mass
                self.images.dCoM = real(ifft2(2*pi*1i*kx.*fft2(CoMX).*bandpass_filter +...
                                             2*pi*1i*ky.*fft2(CoMY).*bandpass_filter));

                debug_toc(self, [], "", debug_time)

                %% Sub sub function
                function [CoMX,CoMY] = integrate_CoM()
                    R_scan = rotation_matrix(self, scan_direction);
                    R_detector = rotation_matrix(self, detector_rotation);
                    
                    % Make pixel array for masks
                    [ygrid, xgrid] = meshgrid(((1:self.dataset_parameters.n_pixels(2))-transmitted_beam_center(2))*flip_scan_y, ...
                                               (1:self.dataset_parameters.n_pixels(1))-transmitted_beam_center(1));
                    
                    im_real = cast(reshape(self.masks.annular,1,[]),self.dataset_parameters.data_type)*self.data;

                    % switch between detector types (except annular/round)
                    if dmod == "CoM"
                        % Mask off diffraction pattern: less than outer angle & greater than inner angle
                        CoM = zeros(prod(self.dataset_parameters.n_frames), 2, 'like',self.data);
                        
                        % Integrated mass of each diffraction pattern within the mask:
                        % Center of Mass adjusted to the center of the diffraction pattern
                        CoM(:,1) = cast(reshape(xgrid.*self.masks.annular,1,[]), self.dataset_parameters.data_type) * self.data./im_real;
                        CoM(:,2) = cast(reshape(ygrid.*self.masks.annular,1,[]), self.dataset_parameters.data_type) * self.data./im_real;
                        
                        % Adjust for scan rotation
                        CoM = CoM*R_scan;
                    
                    elseif dmod == "DPC"
                        nrung = self.NRung.Value;
                        nseg = self.NSeg.Value;
                        rdist = ygrid.^2 + xgrid.^2;

                        % Calculate the atan of all pixel positions within the image
                        
                        % Get atan (-180, 180], then
                        % subtract off any detector rotation applied, then
                        % shift atan by half of a segment span
                        a = atan2d(ygrid,xgrid) - detector_rotation + 180/nseg;
                        
                        % shift the negative values of atan up by 360
                        a(a < 0) = a(a < 0) + 360;
                        
                        % Get total range of atan from [0,360)
                        a(a >= 360) = a(a >= 360)-360;
                        
                        % Preallocate a DPC/CoM vector image that will be
                        % the sum of all segments (i.e. DPC_A, DPC_B, ...)
                        CoM_length = zeros(nrung*nseg,2,self.dataset_parameters.data_type);
                        self.masks.Seg = zeros(nrung*nseg,prod(self.dataset_parameters.n_pixels),'logical');
                        
                        for j = 1:nrung
                            for i = 1:nseg
                                % Define vectors k1 and k2 that correspond
                                % to the inner and outer angles of the
                                % detector for a given number of rungs
                                k1 = (j-1)*(outer_radius-inner_radius)/nrung+inner_radius;
                                k2 = (j)*(outer_radius-inner_radius)/nrung+inner_radius;
                                
                                % less than outer angle & greater than/equal
                                % to inner angle & greater than the start
                                % of the segment angle & less than the end
                                % of the segment angle
                                self.masks.Seg(nseg*(j-1)+i,:) = reshape( ...
                                    rdist < k2^2 & ...
                                    rdist >= k1^2 & ...
                                    a >= (i-1)*360/nseg & ...
                                    a < (i)*360/nseg, [], 1);

                                % Find center of mass of each segment in each rung, and adjust for scan and detector rotation
                                t = (i-1)*360/nseg + detector_rotation;
                                CoM_length(nseg*(j-1)+i,:) = 2*sind(360/nseg/2) / (3*360/nseg/2) ...
                                    * (k1^3-k2^3)/(k1^2-k2^2) * [cosd(t) sind(t)] * R_scan * R_detector;
                            end
                        end

                        % integrated mass of each diffraction pattern within the mask:
                        CoM = (self.masks.Seg*self.data./im_real)'*CoM_length;
                    end

                    % Convert to mrad and pull out x and y components of the CoM
                    CoM = gather(reshape(CoM, [self.dataset_parameters.n_frames 2])*self.mradPx.Value);
                    CoMX = CoM(:,:,1);  CoMY = CoM(:,:,2);
                end

            end

        end

        % Callback function: VirtualApertureInvert, VirtualApertureMirror, 
        % ...and 21 other components
        function virtual_aperture_callbacks(self, event)
            % Function called to during all virtual aperture interactions,
            % including entering the `Virtual Aperture` mode, drawing
            % virtual aperture annotations, and updating UI elements.
            % 
            % Parameters:
            %    self (Quant4D)
            %    event (event.EventData)
            %
            % Returns:
            %    None

            debug_time = tic;

            switch event.Source
                case self.Mode % Entering mode
                    % Update UI limits
                    limit_virtual_aperture_UI(self)
                    
                    % Enable/Disable UIs
                    enable_virtual_aperture_UI(self)
                    
                    % Draw ROIs
                    draw_virtual_aperture_annotation(self)
                    
                    % Update ROI/UI
                    move_virtual_aperture(self, event.Source, event)
                    
                    % Enable windows
                    enable_windows(self,true)
                
                case self.VirtualApertureMirror % Mirror enable/disable
                    
                    % set state button icon color based on value
                    change_icon_background(self, self.VirtualApertureMirror)

                    % Enable/Disable UIs
                    enable_virtual_aperture_UI(self)
                    
                    % Draw ROIs
                    draw_virtual_aperture_annotation(self)
                    
                    % Update ROI/UI
                    move_virtual_aperture(self, event.Source, event)
                
                case self.VirtualApertureSymmetry % Symmetric option
                    % Draw ROIs
                    draw_virtual_aperture_annotation(self)
                    
                    % Update ROI/UI
                    move_virtual_aperture(self, event.Source, event)
                
                case self.DetectorCoordinateSystem % Coordinate options
                    % Update UI limits
                    limit_virtual_aperture_UI(self)
                    
                    % Update UI coordinate values
                    move_virtual_aperture(self, event.Source, event)
                
                case {self.VirtualApertureReset; self.VirtualApertureInvert; ...
                      self.VirtualApertureR; self.VirtualApertureRSpinner; ...
                      self.VirtualApertureX; self.VirtualApertureXSpinner; ...
                      self.VirtualApertureY; self.VirtualApertureYSpinner; ...
                      self.VirtualApertureMirrorRotation; self.VirtualApertureMirrorRotationSpinner; ...
                      self.VirtualApertureRotateCCW; self.VirtualApertureRotateCW; self.UpdateImages}
                    
                    % set state button icon color based on value
                    change_icon_background(self, self.VirtualApertureInvert)
                    
                    % Update ROI/UI
                    move_virtual_aperture(self, event.Source, event)
            end

            debug_toc(self, event, "", debug_time)
        end

        % Callback function: CDDelResetMenu, CustomDetectorColor, 
        % ...and 22 other components
        function custom_detector_callbacks(self, event)
            % 
            % 
            % Parameters:
            %    self (Quant4D)
            %    event (event.EventData)
            %
            % Returns:
            %    None

            % Central beam location
            b0 = self.center;

            % Current selected row in Main Table `sel`, and the ROI group `ROI`
            if self.CustomDetectorTable.Selection > height(self.CustomDetectorTable.Data)
                self.CustomDetectorTable.Selection = [];
            end
            
            % set state button icon color based on value
            for state_button = [self.CustomDetectorInvert, ...
                                self.CustomDetectorMirror, ...
                                self.CustomDetectorFlipHorizontal, ...
                                self.CustomDetectorFlipVertical, ...
                                self.CustomDetectorTranspose]
                change_icon_background(self, state_button)
            end

            sel = self.CustomDetectorTable.Data(self.CustomDetectorTable.Selection, :); 
            ROI = {[]};
            
            if ~isempty(sel)
                ROI = self.annotations.Custom.(sel.ID);
            end

            switch event.Source
                case self.DetectorCoordinateSystem % Coordinate options
                    % Update UI coordinate systems
                    limit_custom_detector_UI()
                    
                    % Update ROI/mask/images
                    move_custom_ROI(ROI{1}, event);

                case {self.UpdateImages self.CustomDetectorInterMask self.Evaluate}
                    % Update ROI/mask/images
                    move_custom_ROI(ROI{1}, event);

                case self.Mode % Entering current mode
                    if ~isfield(self.annotations,'Custom')
                        self.annotations.Custom = [];
                    end

                    % Update UI coordinate systems
                    limit_custom_detector_UI()
                    
                    % Update Enable/Show states of all ROI groups
                    update_enable_show_ROI()
                    
                    % Update for selection change
                    if ~isempty(ROI)
                        mock_UI_callbacks(self, self.CustomDetectorTable)
                    end
                    
                    % Enable windows
                    enable_windows(self,true)

                case self.CustomDetectorTable % Main table
                    % Update Enable/Show states of all ROI groups
                    if event.EventName == "CellEdit"
                        update_enable_show_ROI()
                    end
                    
                    % Update UI and images
                    update_custom_detector_UI();
                    %if ~isempty(ROI{1})
                    move_custom_ROI(ROI{1}, event);
                    %end

                case self.CustomDetectorDeleteMask % Delete selected mask
                    % Early return if no mask selected
                    if isempty(sel)
                        return;
                    end

                    % Delete Annotations, remove field from self.A.Custom and any mask associated with the detector
                    delete(findobj(self.image_axes.Diffraction.Children, "Tag", "Custom " + sel.ID));
                    self.annotations.Custom.(sel.ID) = [];
                    self.annotations.Custom = rmfield(self.annotations.Custom,sel.ID);
                    self.masks.Custom.(sel.ID) = [];
                    self.masks.Custom = rmfield(self.masks.Custom,sel.ID);
                    self.images.Custom.(sel.ID) = [];
                    self.images.Custom = rmfield(self.images.Custom,sel.ID);
                    
                    % Remove item from main table
                    self.CustomDetectorTable.Data(self.CustomDetectorTable.Selection,:) = [];
                    
                    % Update selection
                    if isempty(self.CustomDetectorTable.Data)
                        % No selection if empty
                        self.CustomDetectorTable.Selection = [];
                        ROI = {[]};

                    elseif isempty(self.CustomDetectorTable.Selection)
                        self.CustomDetectorTable.Selection = height(self.CustomDetectorTable.Data);
                        ROI = self.annotations.Custom.(self.CustomDetectorTable.Data.ID(self.CustomDetectorTable.Selection));
                    
                    else
                        % Select last if exceeds table
                        self.CustomDetectorTable.Selection = min(self.CustomDetectorTable.Selection,height(self.CustomDetectorTable.Data));
                        ROI = self.annotations.Custom.(self.CustomDetectorTable.Data.ID(self.CustomDetectorTable.Selection));
                    end

                    % Update for selection change
                    mock_UI_callbacks(self, self.CustomDetectorTable)

                case self.CDDelResetMenu
                    % Remove all masks; Reset
                    delete(findobj(self.image_axes.Diffraction.Children,'-regexp', "Tag", "Custom "));
                    self.CustomDetectorTable.Data(:,:) = [];
                    self.annotations.Custom = [];
                    self.masks.Custom = [];
                    self.images.Custom = [];
                    ROI = {[]};
                    self.CustomDetectorTable.Selection = [];
                    
                    % Update for selection change
                    mock_UI_callbacks(self, self.CustomDetectorTable)

                case {self.CustomDetectorNewCircle; % Create new mask
                      self.CustomDetectorNewGrid;
                      self.CustomDetectorNewGridNoCenter;
                      self.CustomDetectorNewBandpass;
                      self.CustomDetectorNewWedge;
                      self.CustomDetectorNewPolygon;
                      self.CustomDetectorNewFromFile;
                      self.CustomDetectorNewMath}
                    % Character before 'A'
                    idl = "@";

                    % Last ID characters
                    if ~isempty(self.CustomDetectorTable.Data)
                        idl = self.CustomDetectorTable.Data(end,:).ID;
                    end 
                    
                    % warn on maximum number of custom detectors
                    if idl == "ZZ"
                        notification_dialog(self, "warn", "Mask ID can not go beyond 'ZZ'!", "Maximum Custom Detectors Capacity Reached");
                        return
                    end

                    % Serial numbers of Last ID characters, e.g. 3 for "C" or [1 2] for "AB"
                    nidl = double(char(idl))-64;
                    
                    % Convert to one single serial number for Last ID
                    nidl = (numel(nidl)-1)*nidl(1)*26 + nidl(end);
                    
                    % New ID, e.g. 'AA' for 26, "b" for 1
                    id = replace(char([floor(nidl/26), rem(nidl, 26)+1]+64),'@',"");
                    
                    % Preset values
                    self.CustomDetectorMirror.Value = 0;
                    self.CustomDetectorInvert.Value = 0;
                    self.CustomDetectorIntraMask.Value = "Union";

                    switch event.Source
                        case self.CustomDetectorNewCircle
                            roi_type = "Circle";

                        case self.CustomDetectorNewGrid
                            roi_type = "Grid";

                        case self.CustomDetectorNewGridNoCenter
                            roi_type = "GridNoCenter";
                        
                        case self.CustomDetectorNewBandpass
                            roi_type = "Bandpass";
                        
                        case self.CustomDetectorNewWedge
                            roi_type = "Wedge";
                            self.CustomDetectorMirror.Value = 1;
                        
                        case self.CustomDetectorNewPolygon
                            roi_type = "Polygon";
                        
                        case self.CustomDetectorNewFromFile, roi_type = "File";
                            mask = import_mask(self, "Diffraction");
                            % Early return if `[]` (failed/canceled)
                            if isempty(mask)
                                return
                            end
                            self.masks.Custom.(id) = mask;
                        
                        case self.CustomDetectorNewMath
                            roi_type = "Math";
                    end

                    ROI = drawCDROI(id, roi_type);
                    
                    % Early return if draw ROI failed, e.g. polygon canceled.
                    if isempty(ROI)
                        return;
                    end
                    
                    % Store the ROI group
                    self.annotations.Custom.(id) = ROI;
                    
                    % Add row to Main Table
                    self.CustomDetectorTable.Data(end + 1,:) = {id, roi_type, id, true, true, 1};
                    
                    % Select the last, just added row
                    self.CustomDetectorTable.Selection = height(self.CustomDetectorTable.Data);
                    
                    % Color the Label in Main Table
                    color_custom_detector_table_label(self.CustomDetectorTable.Selection,self.annotations.Custom.(id){1}.UserData.Color);
                    
                    % Update for selection change
                    mock_UI_callbacks(self, self.CustomDetectorTable)

                case {self.CustomDetectorIntraMask, self.CustomDetectorInvert, self.CustomDetectorMirror} % Intra-mask, Invert Mask, Mirror Mask
                    % Update values in `UserData` for current mask
                    ROI{1}.UserData.IntraMask = self.CustomDetectorIntraMask.Value;
                    ROI{1}.UserData.Inverted = self.CustomDetectorInvert.Value;
                    ROI{1}.UserData.Mirrored = self.CustomDetectorMirror.Value;
                    ROI = drawCDROI(sel.ID, sel.Type);
                    
                    % Re-drawn ROI
                    self.annotations.Custom.(sel.ID) = ROI;
                    
                    % Update for selection change
                    mock_UI_callbacks(self, self.CustomDetectorTable)

                case self.CustomDetectorColor  % Change the color of mask annotations
                    % Open color selection palette
                    color = uisetcolor(ROI{1}.UserData.Color);
                    
                    % If color unchanged
                    if isequal(color, ROI{1}.UserData.Color)
                        return;
                    end
                    ROI{1}.UserData.Color = color;

                    % make sure all overlays change color with main overlay
                    cellfun(@(r) set(findobj(r,"-property", "Color"), "Color", color),ROI);
                    color_custom_detector_table_label(self.CustomDetectorTable.Selection, color);
                    
                    % Update UI
                    update_custom_detector_UI()
                    
                    % changing mask color in "Color Mix" mode requires images to be re-plotted to match
                    if strcmp(self.CustomDetectorInterMask.Value, "Color Mix")
                        plot_custom_mask(event, "")
                    end

                case {self.CustomDetectorFlipHorizontal self.CustomDetectorFlipVertical self.CustomDetectorTranspose} % Flip and Transpose
                    % Whether diffraction is rotated by +/-90°
                    r90 = mod(self.RotateDiffraction.Value,180) == 90;

                    if sel.Type == "File"
                        % Transform the imported image array, then update/create mask from the transformed image
                        switch event.Source
                            case {self.CustomDetectorFlipHorizontal self.CustomDetectorFlipVertical}
                                % flip custom mask across horizontal/vertical axis
                                if (r90 && event.Source == self.CustomDetectorFlipHorizontal) || (~r90 && event.Source == self.CustomDetectorFlipVertical)
                                    % Visually Flip X
                                    self.masks.Custom.(sel.ID) = flipud(self.masks.Custom.(sel.ID));
                                else
                                    % Visually Flip Y
                                    self.masks.Custom.(sel.ID) = fliplr(self.masks.Custom.(sel.ID));
                                end

                            case self.CustomDetectorTranspose
                                % transpose custom mask (only available if diffraction pattern is square)
                                self.masks.Custom.(sel.ID) = self.masks.Custom.(sel.ID)';
                        end

                        % Update Images
                        move_custom_ROI(ROI{1}, event);

                    else
                        % Convert Detail Table positions to Cartesian relative (pixel or mrad)
                        details_table = self.CustomDetectorDetailsTable.Data(:, 1:2);
                        if self.DetectorCoordinateSystem.Value == "Cartesian"
                            xycr = details_table - (self.center-self.center_rel)*self.diff_scale;
                        else
                            xycr = details_table(:, 1).*[cosd(details_table(:, 2)) sind(details_table(:, 2))];
                        end

                        switch event.Source
                            case {self.CustomDetectorFlipHorizontal self.CustomDetectorFlipVertical}
                                % flip custom mask across horizontal/vertical axis
                                if (r90 && event.Source == self.CustomDetectorFlipHorizontal) || (~r90 && event.Source == self.CustomDetectorFlipVertical)
                                    % Flip X
                                    xycr(:,1) = -xycr(:,1);
                                else
                                    % Flip Y
                                    xycr(:,2) = -xycr(:,2);
                                end
                                
                            case self.CustomDetectorTranspose % transpose custom mask
                                % Swap X/Y
                                xycr = fliplr(xycr);
                        end

                        % Convert from Cartesian relative (pixel or mrad) back to whatever it should be
                        if self.DetectorCoordinateSystem.Value == "Cartesian"
                            self.CustomDetectorDetailsTable.Data(:, 1:2) = xycr + (self.center-self.center_rel)*self.diff_scale;
                        else
                            self.CustomDetectorDetailsTable.Data(:, 1:2) = [sqrt(sum(xycr.^2,2)), atan2d(xycr(:,2), xycr(:,1))];
                        end
                        
                        % Trigger Detail Table editing callbacks
                        mock_UI_callbacks(self, self.CustomDetectorDetailsTable)
                    end

                case {self.CustomDetectorRotateCCW, self.CustomDetectorRotateCW} % Rotate detector
                    % Clockwise if odd numbers of "Reverse X" "Reverse Y" "Rotate Clockwise" are true
                    rot = self.CustomDetectorRotationStep.Value*(1-2*rem(self.ReverseDiffractionX.Value+self.ReverseDiffractionY.Value+(event.Source == self.CustomDetectorRotateCW),2));
                    
                    if sel.Type == "File"
                        % Transform the imported image array, then update/create mask from the transformed image
                        self.masks.Custom.(sel.ID) = rot90(self.masks.Custom.(sel.ID), rot/90);
                        
                        % Update Images
                        move_custom_ROI(ROI{1}, event);
                    
                    else
                        % Edit coordinates in `self.CustomDetectorDetailsTable` and trigger its callbacks to rotate ROIs
                        if self.DetectorCoordinateSystem.Value == "Cartesian"
                            % If absolute then convert to relative then convert back, before/after rotation
                            R = rotation_matrix(self, rot);
                            rrb0 = (self.center-self.center_rel)*self.diff_scale;
                            self.CustomDetectorDetailsTable.Data(:, 1:2) = ((self.CustomDetectorDetailsTable.Data(:, 1:2)-rrb0)*R + rrb0);
                        else
                            self.CustomDetectorDetailsTable.Data(:, 2) = mod(self.CustomDetectorDetailsTable.Data(:, 2)+rot, 360);
                        end
                        
                        % Trigger Detail Table editing callbacks
                        mock_UI_callbacks(self, self.CustomDetectorDetailsTable)
                    end

                case self.CustomDetectorDetailsTable % Detail Table
                    % Determine Cartesian absolute pixel position from
                    % Detail Table (may be polar/relative/mrad)
                    details_table = self.CustomDetectorDetailsTable.Data;

                    if self.DetectorCoordinateSystem.Value == "Cartesian"
                        p = details_table(:, 1:2)/self.diff_scale + self.center_rel;
                    else
                        p = details_table(:, 1)/self.diff_scale.*[cosd(details_table(:, 2)) sind(details_table(:, 2))] + self.center_rel;
                    end

                    % Sync ROIs positions with the edited Detail Table
                    switch sel.Type
                        case {"Circle", "Grid", "GridNoCenter"}
                            r = details_table(1, 3);
                            % If edited the 2nd R ([2 3] in table) then use
                            % that, instead of the default 1st R
                            if isprop(event, "Indices") && isequal(event.Indices, [2 3])
                                r = str2double(event.EditData);
                            end
                            
                            ROI{1}.Center = p(1, :);
                            ROI{1}.Radius = r/self.diff_scale;

                            if height(p) > 1
                                ROI{2}.Center = p(2, :);
                                ROI{2}.Radius = r/self.diff_scale;
                            end

                        case "Bandpass"
                            color = p(1, :);
                            % If edited the 2nd X or Y ([2 1] or [2 2] in
                            % table), then use that value, instead of the
                            % default 1st X/Y
                            if isprop(event, "Indices") && event.Indices(1) == 2 && any(event.Indices(2) == [1 2])
                                color = p(2, :);
                            end

                            ROI{1}.Center = color; 
                            ROI{1}.Radius = details_table(1, 3)/self.diff_scale;
                            ROI{2}.Center = color;
                            ROI{2}.Radius = details_table(2, 3)/self.diff_scale;

                        case "Wedge"
                            ROI{1}.Position = p(1, :);
                            ROI{2}.Position = p(2, :);

                        case "Polygon"
                            ROI{1}.Position = p;
                    end

                    % Update Images
                    move_custom_ROI(ROI{1}, event);
                
                otherwise
                    error("Undefined")

            end


            %%% Sub functions
            % Function to return font color (black or white) based on input color
            function color = font_color(c)
                % Dark color criterion
                color = [0 0 0] + (c.^2*[0.299;0.587;0.114] < 0.25);
            end

            % Function to color Main Table
            function color_custom_detector_table_label(selection, color)
                addStyle(self.CustomDetectorTable, ...
                         uistyle("BackgroundColor",color,'FontColor',font_color(color)), ...
                         'cell',[selection, 3])
            end

            % Function to update UI labels; actually Custom Detector UIs have no limits
            function limit_custom_detector_UI()
                unit = " " + self.DetectorCoordinateUnit.Value;
                
                if self.DetectorCoordinateSystem.Value == "Polar"
                    self.CustomDetectorDetailsTable.ColumnName(1:3) = {"ρ"+unit, "θ °", "R"+unit};
                else
                    self.CustomDetectorDetailsTable.ColumnName(1:3) = {"X"+unit, "Y"+unit, "R"+unit};
                end
            end

            % Function to update enable/show state of ROIs based on Main Table
            function update_enable_show_ROI()
                for i = 1:height(self.CustomDetectorTable.Data)
                    ri = self.CustomDetectorTable.Data(i, :);
                    cellfun(@(r) set(findobj(r,'-property',"Visible"),"Visible", ri.Show && ri.Enable), ...
                        self.annotations.Custom.(ri.ID));
                end
            end

            % Function to update UI
            function update_custom_detector_UI()
                % Try to resize columns
                self.CustomDetectorDetailsTable.ColumnWidth = {"1x","1x","1x"};
                self.CustomDetectorTable.ColumnWidth = {"fit", "fit", "1x", "fit", "fit", "fit"};

                if ~isempty(self.CustomDetectorTable.Data)
                    self.CustomDetectorTable.Data(end + 1,:) = self.CustomDetectorTable.Data(end,:);
                    self.CustomDetectorTable.Data(end,:)=[];
                end
                
                % Disable Detail UI if no ROI selected
                self.CustomDetectorDetailsPanel.Enable = switch_on_off(self, ~isempty(self.CustomDetectorTable.Selection));

                if isempty(self.CustomDetectorTable.Selection)
                    self.CustomDetectorDetailsTable.Data = [];
                    set([self.CustomDetectorDetailsGrid self.CustomDetectorRotationGrid], "BackgroundColor","w");
                else
                    % Set component options based on current mask item
                    user_data = self.annotations.Custom.(self.CustomDetectorTable.Data.ID(self.CustomDetectorTable.Selection)){1}.UserData;
                    set([self.CustomDetectorInvert; ...
                         self.CustomDetectorIntraMask; ...
                         self.CustomDetectorMirror], ...
                        {"Value"}, ...
                        {user_data.Inverted; ...
                         user_data.IntraMask; ...
                         user_data.Mirrored})
                    
                    % Set Detail UI color; white font if darker background color
                    set([self.CustomDetectorDetailsGrid; ...
                         self.CustomDetectorRotationGrid; ...
                         self.CustomDetectorDetailsTable], ...
                        "BackgroundColor",user_data.Color)

                    self.CDIntraCombLabel.FontColor = font_color(user_data.Color);
                    self.CustomDetectorDetailsTable.ForegroundColor = font_color(user_data.Color);
                    
                    % Enable/Disable UI
                    set([self.CustomDetectorMirror; ...
                         self.CustomDetectorIntraMask; ...
                         self.CustomDetectorRotationStep; ...
                         self.CustomDetectorTranspose], ...
                        {"Enable"},{0;0;1;1})
                    
                    equ = "";
                    
                    switch user_data.Type
                        case "Circle"
                            self.CustomDetectorMirror.Enable = "on";
                            self.CustomDetectorIntraMask.Enable = self.CustomDetectorMirror.Value;
                        
                        case "Wedge"
                            self.CustomDetectorMirror.Enable = "on";
                        
                        case {"Grid","GridNoCenter"}
                            self.CustomDetectorIntraMask.Enable = "on";
                        
                        case "Bandpass"
                        
                        case "Polygon"
                        
                        case "File"
                            % Allow transpose/rotate 90° if diffraction
                            % image is square
                            self.CustomDetectorTranspose.Enable = ~range(self.dataset_parameters.n_pixels);
                            set(self.CustomDetectorRotationStep, ...
                                "Value", 180 - ~range(self.dataset_parameters.n_pixels)*90, ...
                                "Enable", "off");
                        
                        case "Math"
                            equ = user_data.Math;
                    end
                    
                    % Put formula on Math UI
                    self.MathFormula.Value = equ;
                end
            end

            % Function to draw annotations
            function ROI = drawCDROI(id, roi_type)
                % parameters
                r0 = self.TransBeamR.Value;
                xmin = 0;
                xmax = self.dataset_parameters.n_pixels(1)+1;
                ymin = 0;
                ymax = self.dataset_parameters.n_pixels(2)+1;

                % Initial values
                p1 = [];
                r1 = [];
                p2 = [];
                r2 = [];
                user_data = struct("ID", id, ...
                                   "Type", roi_type, ...
                                   "Color", rand(1,3), ...
                                   "Mirrored", self.CustomDetectorMirror.Value, ...
                                   "IntraMask", self.CustomDetectorIntraMask.Value, ...
                                   "Inverted", self.CustomDetectorInvert.Value);

                % If the ROIs already exist, get their current color/position/radius & UserData
                if isfield(self.annotations.Custom, id)
                    ROI = self.annotations.Custom.(id);
                    user_data = ROI{1}.UserData;

                    if isprop(ROI{1}, "Position")
                        p1 = ROI{1}.Position;
                    end
                    
                    if isprop(ROI{1}, "Center")
                        p1 = ROI{1}.Center;
                        r1 = ROI{1}.Radius;
                    end

                    if isprop(ROI{2}, "Position")
                        p2 = ROI{2}.Position;
                    end
                    
                    if isprop(ROI{2}, "Center")
                        p2 = ROI{2}.Center;
                        r2 = ROI{2}.Radius;
                    end
                    
                    % Remove old ROIs
                    delete(ROI{1});
                    delete(ROI{2});
                    delete(ROI{3});
                end

                % Draw ROIs
                ROI = cell(3,1);
                switch roi_type
                    case "Circle"
                        % Initial disk identical to the central beam
                        if isempty(p1)
                            p1 = b0;
                            r1 = r0;
                        end
                        
                        % draw main circle
                        ROI{1} = drawcircle(self.image_axes.Diffraction, ...
                                            "Center", p1, ...
                                            "Radius", r1);

                        % draw mirrored circle if enabled by user
                        if user_data.Mirrored
                            ROI{2} = drawcircle(self.image_axes.Diffraction, ...
                                                "Center", -p1+2*b0, ...
                                                "Radius", r1, ...
                                                "InteractionsAllowed", "none");
                        end

                        % set parameters
                        set([ROI{1} ROI{2}], ...
                            "FaceAlpha", 0, ...
                            "FaceSelectable", 0, ...
                            "DrawingArea", "unlimited");
                    
                    case {"Grid","GridNoCenter"}
                        % draw pair of apertures with starting size of transmitted disk
                        if isempty(p2)
                            p1 = b0 + [xmax-xmin 0]/4;
                            p2 = b0 + [0 ymax-ymin]/4;
                            r1 = r0;
                        end

                        % draw two circles for basis vectors
                        ROI{1} = drawcircle(self.image_axes.Diffraction, ...
                                            "Center", p1, ...
                                            "Radius", r1);

                        ROI{2} = drawcircle(self.image_axes.Diffraction, ...
                                            "Center", p2, ...
                                            "Radius", r1);

                        % set parameters
                        set([ROI{1} ROI{2}], ...
                            "FaceAlpha", 0, ...
                            "FaceSelectable", 0, ...
                            "DrawingArea", "unlimited")
                    
                    case "Bandpass"
                        % draw two circles for the user to resize, centered on the optic axis
                        if isempty(r2)
                            r1 = r0;
                            r2 = (xmax-xmin)/4 + r0/2;
                        end

                        % draw inner and outer circles of the band-pass
                        ROI{1} = drawcircle(self.image_axes.Diffraction, ...
                                            "Center", b0, ...
                                            "Radius",r1);

                        ROI{2} = drawcircle(self.image_axes.Diffraction, ...
                                            "Center", b0, ...
                                            "Radius", r2);

                        % set parameters
                        set([ROI{1} ROI{2}], ...
                            "FaceAlpha", 0, ...
                            "DrawingArea", "unlimited", ...
                            "FaceSelectable", false);

                        % draw a filled polygon between the two circles
                        % that the user cannot interact with, just for
                        % reference
                        ROI{3} = drawpolygon(self.image_axes.Diffraction, ...
                                             "Position", [ROI{1}.Vertices;ROI{2}.Vertices], ...
                                             "InteractionsAllowed", "none", ...
                                             "EdgeAlpha", 0, ...
                                             "FaceSelectable", false);
                    
                    case "Wedge"
                        % give polygon temporary set of points, keep
                        % invisible. Points will be sorted in move_wedge()
                        if isempty(p2)
                            l = min(self.dataset_parameters.n_pixels)/3;
                            p1 = [l l];
                            p2 = [l 2*l];
                        end

                        % draw polygon wedge and a pair of points for user
                        % interaction
                        ROI{3} = drawpolygon(self.image_axes.Diffraction, ...
                                             "Position", [p1;p2;b0], ...
                                             "InteractionsAllowed", "none");
                        ROI{1} = drawpoint(self.image_axes.Diffraction, "Position",p1);
                        ROI{2} = drawpoint(self.image_axes.Diffraction, "Position",p2);
                    
                    case "Polygon"
                        if isempty(p1)
                            notification_dialog(self, ...
                                                "help", ...
                                                sprintf("Please draw a Polygon ROI on the Diffraction image!\n\n" ...
                                                        + "Press 'Esc' to cancel during drawing. Please refer to MATLAB's 'drawpolygon' for more tips."), ...
                                                "Draw Polygon ROI");
                            
                            % Disable UIs until polygon is drawn
                            enable_windows(self,false);
                            figure(self.figures.Diffraction);
                            self.figures.Diffraction.UserData.grayout.Visible = "off";
                            
                            % draw polygon and re-enable UIs
                            ROI{1} = drawpolygon(self.image_axes.Diffraction, ...
                                                 "Color", user_data.Color);
                            p1 = ROI{1}.Position;
                            enable_windows(self,true)
                            
                            % Early return if polygon is not drawn
                            if isempty(p1)
                                delete(ROI{1});
                                ROI = [];
                                return;
                            end

                        else
                            ROI{1} = drawpolygon(self.image_axes.Diffraction, ...
                                                 "Position",p1);
                        end

                        ROI{1}.FaceSelectable = false;
                        ROI{2} = drawpolygon(self.image_axes.Diffraction, ...
                                             "Position", p1, ...
                                             "EdgeAlpha", 0, ...
                                             "InteractionsAllowed", "none");
                    
                    case "File"
                        % Invisible ROI as placeholder
                        ROI{1} = drawrectangle(self.image_axes.Diffraction, ...
                                               "Position", [0 0 xmax+1 ymax+1], ...
                                               "InteractionsAllowed", "none", ...
                                               "EdgeAlpha", 0, ...
                                               "FaceAlpha",0);
                    
                    case "Math"
                        % Invisible ROI as placeholder
                        ROI{1} = drawrectangle(self.image_axes.Diffraction, ...
                                               "Position", [0 0 xmax+1 ymax+1], ...
                                               "InteractionsAllowed", "none", ...
                                               "EdgeAlpha", 0, ...
                                               "FaceAlpha",0);

                        % set defaults
                        self.MathFormula.Value = "1";
                        user_data.Math = "1";
                        
                        % Show and select Math Tab
                        figure(self.figures.Settings);
                        self.SettingsTabGroup.SelectedTab = self.MathTab;
                end
                
                % Try to set common properties for all ROI objects
                for i = 1:numel(ROI)
                    if ~any(ishandle(ROI{i}))
                        continue;
                    end

                    % set parameters
                    set(ROI{i}, ...
                        "Color", user_data.Color, ...
                        "Deletable", false, ...
                        "Tag", "Custom "+id, ...
                        "UserData", user_data)
                    
                    % add listeners
                    ROI{i}.UserData.Move = addlistener(ROI{i}, "ROIMoved", @move_custom_ROI);
                    addlistener(ROI{i}, "MovingROI", @move_custom_ROI);
                    addlistener(ROI{i},'ROIClicked', @move_custom_ROI);
                end
            end

            % Function for UI/ROI changes
            function move_custom_ROI(source, event)
                debug_time = tic;
                
                % Clear diffraction mask and real images if empty source; early return
                if isempty(source)
                    plot_custom_mask(event, []);
                    return;
                end

                % Retrieve ROIs of the current interacted-with
                ROI = self.annotations.Custom.(replace(source.Tag, "Custom ",""));
                user_data = ROI{1}.UserData;

                % Change selected mask based on the one the user is interacting with
                if self.CustomDetectorTable.Data.ID(self.CustomDetectorTable.Selection) ~= user_data.ID
                    self.CustomDetectorTable.Selection = find(self.CustomDetectorTable.Data.ID == user_data.ID);
                    update_custom_detector_UI();
                end

                % Get position etc from ROI
                p1 = [];
                r1 = [];
                p2 = [];
                r2 = [];
                p1t = [];
                p2t = [];

                if isprop(ROI{1}, "Position")
                    p1 = ROI{1}.Position;
                end

                if isprop(ROI{1}, "Radius")
                    p1 = ROI{1}.Center;
                    r1 = ROI{1}.Radius;
                end

                % Types with significant 2nd ROI
                if ismember(user_data.Type, ["Grid"; "GridNoCenter"; "Bandpass"; "Wedge"])
                    if isprop(ROI{2}, "Position")
                        p2 = ROI{2}.Position;
                    end

                    if isprop(ROI{2}, "Radius")
                        p2 = ROI{2}.Center;
                        r2 = ROI{2}.Radius;
                    end
                end

                % Update Detail Table with coordinate options, with maybe reduced calculation policy
                if is_static_event(self, event) || self.CalculationPolicy.Value == 2
                    if ~isempty(p1)
                        p1t = p1(:, 1:2);
                    end

                    if ~isempty(p2)
                        p2t = p2(:, 1:2);
                    end

                    xyt = ([p1t; p2t] - self.center_rel)*self.diff_scale;

                    if self.DetectorCoordinateSystem.Value == "Polar"
                        xyt = [sqrt(sum(xyt.^2, 2)), mod(atan2d(xyt(:, 2), xyt(:, 1)), 360)];
                    end

                    self.CustomDetectorDetailsTable.Data = [xyt, [r1;r2]*self.diff_scale];
                end

                % Diffraction image size limits
                xmin = 0;
                xmax = self.dataset_parameters.n_pixels(1)+1;
                ymin = 0;
                ymax = self.dataset_parameters.n_pixels(2)+1;

                switch user_data.Type
                    case "Circle"
                        % Make mask from current detector objects
                        mask = createMask(ROI{1}, self.image_displays.Diffraction)';

                        if user_data.Mirrored
                            % update circle{2} location
                            ROI{2}.Center = 2*b0 - p1;
                            ROI{2}.Radius = r1;

                            % Mask of mirrored circle
                            mask2 = createMask(ROI{2}, self.image_displays.Diffraction)';

                            switch user_data.IntraMask
                                case "Additive"
                                    mask = mask + mask2;

                                case "Union"
                                    mask = mask | mask2;

                                case "Intersection"
                                    mask = mask & mask2;
                            end
                        end

                    case {"Grid", "GridNoCenter"}
                        % Either from ROI{1} or ROI{2}
                        if isprop(event, "CurrentRadius")
                            r1 = event.CurrentRadius;
                        end

                        % Sync radii of both ROIs
                        ROI{1}.Radius = r1;
                        ROI{2}.Radius = r1;

                        
                        % max # of repeats (anything larger gets laggy)
                        nRep = 100;
                        
                        % Find position of all circles in the grid
                        [repsy, repsx] = meshgrid(-nRep:nRep);
                        reps = [reshape(repsx,[],1), reshape(repsy,[],1)];

                        % if "GridNoCenter" remove all even repeats to
                        % ignore transmitted beam and equivalents
                        if strcmp(user_data.Type, "GridNoCenter")
                            reps(all(mod(reps,2) == 0,2) | all(mod(reps,2) == 1,2),:) = [];
                        end
                        
                        % apply basis vectors to each circle
                        reps = reps*([p1; p2]-b0) + b0;
                        
                        % Remove duplicates within single precision
                        reps = uniquetol(reps,eps("single"),"ByRows",true);

                        % filter out any grid points outside the diffraction pattern
                        reps(reps(:,1) < -r1 | ...
                             reps(:,2) < -r1 | ...
                             reps(:,1) > xmax+r1 | ...
                             reps(:,2) > ymax+r1, :) = [];
                        
                        % Draw circles for grid
                        delete(ROI{3})
                        ROI{3} = viscircles(self.image_axes.Diffraction, ...
                                            reps, r1+reps(:,1)*0, ...
                                            "EnhanceVisibility", false, ...
                                            "Color", user_data.Color);

                        % Copy properties
                        ROI{3}.Tag = ROI{1}.Tag;
                        ROI{3}.Visible = ROI{1}.Visible;
                        
                        % Make mask from current detector grid
                        [ygrid,xgrid] = meshgrid(1:self.dataset_parameters.n_pixels(2), 1:self.dataset_parameters.n_pixels(1));
                        mask = reshape(sum(sqrt((xgrid(:)-reps(:,1)').^2+(ygrid(:)-reps(:,2)').^2) <= r1, 2), self.dataset_parameters.n_pixels);

                        switch user_data.IntraMask
                            case "Additive"

                            case "Union"
                                mask = logical(mask);

                            case "Intersection"
                                mask = mask > 1;
                        end

                    case "Bandpass"
                        % Sync centers if moved
                        if isprop(event, "CurrentCenter")
                            p1 = event.CurrentCenter;
                            set_external_source(self, event,[ROI{1}, ROI{2}],"Center",p1)
                        end

                        % Generate mask
                        pos = [ROI{2}.Vertices; ROI{1}.Vertices];
                        ROI{3}.Position = pos;
                        mask = createMask(ROI{3}, self.image_displays.Diffraction)';
                        
                        % Invert only ROI appearance here
                        if user_data.Inverted
                            ROI{3}.Position = [pos;
                                               [xmax, pos(end,2);
                                                xmax, ymax;
                                                xmin, ymax;
                                                xmin, ymin;
                                                xmax, ymin;
                                                xmax, pos(end,2)] ...
                                               ];
                        end

                    case "Wedge"
                        % Get polar degrees of the two Point ROIs in `dp`, and sort as `dp(1)` < `dp(2)`
                        dp = [p1;p2] - b0;
                        dp = sort(mod(atan2d(dp(:,2), dp(:,1)), 360));

                        % Make sure the in-between angle < 180
                        if dp(2)-dp(1) > 180
                            dp = [dp(2) dp(1)+360];
                        end

                        % `d1` & `d2` are for degrees of vertices of the two symmetric sectors, `dp` as initials
                        d1 = dp;
                        d2 = dp + 180;

                        % Extra logics for inverted/mirrored mask
                        if user_data.Inverted
                            d1 = [dp(2) dp(1)+360];
                        end

                        if user_data.Inverted && user_data.Mirrored
                            d1 = [dp(2) dp(1)+180];
                            d2 = [dp(2)+180 dp(1)+360];
                        end

                        % Insert diagonal degrees to cover the corners
                        cnr = 45:90:720;
                        d1 = [d1(1), cnr(cnr >= d1(1) & cnr <= d1(2)), d1(2)];
                        d2 = [d2(1), cnr(cnr >= d2(1) & cnr <= d2(2)), d2(2)];
                        
                        % Ignore `d2` for single-sided mask, then convert to
                        % X/Y and insert the center [0 0] as starting point
                        if user_data.Mirrored
                            d = [d1 fliplr(d2)]';
                        else
                            d = d1';
                        end

                        ROI{3}.Position = [0 0; 2*max(ymax,xmax).*[cosd(d) sind(d)]] + b0;
                        
                        % Generate mask
                        mask = createMask(ROI{3}, self.image_displays.Diffraction)';
                        
                        % Extra inversion, because it'll be inverted universally at the end
                        if user_data.Inverted
                            mask = 1 - mask;
                        end

                    case "Polygon"
                        % Invert only ROI appearance here
                        if user_data.Inverted
                            endPt = p1(end,:);
                            endPtAng = atan2d(endPt(2) - b0(2), endPt(1) - b0(1));
                            
                            if endPtAng < 135 && endPtAng >= 45
                                % top edge
                                corners = [endPt;endPt(1),ymax; xmax,ymax; xmax,ymin; xmin,ymin; xmin,ymax; endPt(1),ymax;endPt];
                            
                            elseif endPtAng < 45 && endPtAng >= -45
                                % right edge
                                corners = [endPt;xmax,endPt(2); xmax,ymax; xmin,ymax; xmin,ymin; xmax,ymin; xmax,endPt(2);endPt];
                            
                            elseif endPtAng < -45 && endPtAng >= -135
                                % bottom edge
                                corners = [endPt;endPt(1),ymin; xmin,ymin; xmin,ymax; xmax,ymax; xmax,ymin; endPt(1),ymin;endPt];
                            
                            else
                                % left edge
                                corners = [endPt;xmin,endPt(2); xmin,ymax; xmax,ymax; xmax,ymin; xmin,ymin; xmin,endPt(2);endPt];
                            end
                            pos2 = [corners;p1];
                            faceAlpha = 0;
                        else
                            pos2 = p1;
                            faceAlpha = 0.2;
                        end

                        % update poly2 points and faceAlpha for both. set max alpha to 0.2
                        ROI{1}.FaceAlpha = faceAlpha;
                        ROI{2}.FaceAlpha = 0.2 - faceAlpha;
                        ROI{2}.Position = pos2;
                        
                        % generate mask
                        mask = createMask(ROI{1}, self.image_displays.Diffraction)';

                    case "File"
                        % Only deal with visual here
                        mask = self.masks.Custom.(user_data.ID);
                        
                        % Invert only ROI appearance here
                        if user_data.Inverted
                            mask = max(mask,[], "all") - mask;
                        end
                        
                        delete(ROI{2})
                        
                        % Draw boundaries of imported file mask
                        try
                            visb = visboundaries(self.image_axes.Diffraction, ...
                                                 bwboundaries(mask'), ...
                                                 "Color", user_data.Color, ...
                                                 "EnhanceVisibility", 0);

                            % If some boundary is drawn, copy properties
                            if ~isempty(visb)
                                visb.Tag = ROI{1}.Tag;
                                visb.Visible = ROI{1}.Visible;
                                ROI{2} = visb;
                            end
                        catch
                        end

                        % Actual mask is already updated before
                        self.masks.Custom.(user_data.ID) = mask;

                    case "Math"
                        message = strings(0);
                        
                        % Get/Store formula
                        equ0 = string(strjoin(self.MathFormula.Value));
                        ROI{1}.UserData.Math = equ0;
                        
                        % Extract "A" "AB" etc
                        ms = unique(string(regexp(equ0, "\<[A-Z]+\>", "match")));

                        ids = string(fieldnames(self.annotations.Custom));
                        
                        % Existing IDs and Unknown IDs
                        unk = setdiff(ms,ids);
                        
                        % Check IDs
                        if numel(unk)
                            message(end + 1) = sprintf("Unknown IDs: %s !", strjoin(unk, ", "));
                        end
                        
                        if ismember(user_data.ID, ms)
                            message(end + 1) = sprintf("Self ID (%s) encountered!", user_data.ID);
                        end
                        
                        % Try to evaluate
                        if isempty(message)
                            equ = regexprep(equ0, "\<" + ms + "\>", "self.masks.Custom." + ms); 
                            mask_t = [];
                            try
                                mask_t = eval(equ);
                                mask = zeros(self.dataset_parameters.n_pixels) + mask_t;
                            catch ME
                                message(end + 1) = sprintf('%s\n%s\n%s', ME.identifier, ME.message, ME.Correction);
                                % Check result size
                                if ~isempty(mask_t)
                                    message(end + 1) = sprintf("Resulted mask size is %d×%d (X×Y).", size(mask_t));
                                end
                            end
                        end

                        % Check real/complex
                        if isempty(message) && ~isreal(mask)
                            message(end + 1) = sprintf("Resulted mask is a complex array!");
                        end
                        
                        % Early return if any error
                        if ~isempty(message)
                            notification_dialog(self, ...
                                                "warn", ...
                                                "Calculation failed!" + sprintf("\n%s",message), ...
                                                "Evaluation Failed");
                            return
                        end

                        delete(ROI{2})
                        
                        % Draw boundaries of calculated mask
                        try
                            visb = visboundaries(self.image_axes.Diffraction, ...
                                                 bwboundaries(mask'), ...
                                                 "Color", user_data.Color, ...
                                                 "EnhanceVisibility",0);

                            % If some boundary is drawn, copy properties
                            if ~isempty(visb)
                                visb.Tag = ROI{1}.Tag;
                                visb.Visible = ROI{1}.Visible;
                                ROI{2} = visb;
                            end
                        catch
                        end
                end

                % bring ROIs to the front
                for i_ROI = 3:-1:1
                    if ismethod(ROI{i_ROI},'bringToFront')
                        bringToFront(ROI{i_ROI});
                    end
                end
                
                % Assign the created ROIs back to the global handle
                self.annotations.Custom.(user_data.ID) = ROI;
                
                % Invert mask
                if user_data.Inverted
                    mask = max(mask,[], "all") - mask;
                end
                
                % Store mask
                self.masks.Custom.(user_data.ID) = mask;

                % Store color mix mask
                if strcmp(self.CustomDetectorInterMask.Value, "Color Mix")
                    self.masks.CustomColor.(user_data.ID) = mask.*reshape(self.annotations.Custom.(user_data.ID){1}.Color,[1 1 3]);
                end

                plot_custom_mask(event, user_data.ID)
                debug_toc(self, event, "", debug_time)
            end

            function plot_custom_mask(event, id)
                debug_time = tic;
                % Whether to update images
                if to_update_image(self, event)
                    % start with a clear mask
                    custom_mask = zeros(self.dataset_parameters.n_pixels, self.dataset_parameters.data_type);
                    
                    % Go through all enabled AND non-zero-weighting masks; add/intersect them accordingly
                    cds = self.CustomDetectorTable.Data(self.CustomDetectorTable.Data.Enable & self.CustomDetectorTable.Data.Weight, :);

                    % exit if there are no custom masks
                    if isempty(cds)
                        self.images.DiffractionMask = custom_mask;
                        self.images.Real = zeros(self.dataset_parameters.n_frames, self.dataset_parameters.data_type);
                        plot_all_patterns(self, event)
                        return
                    end

                    % split masks by color if in "Color Mix" mode
                    if strcmp(self.CustomDetectorInterMask.Value, "Color Mix")
                        color_masks = zeros([height(cds),prod(self.dataset_parameters.n_pixels)],self.dataset_parameters.data_type);
                        self.masks.CustomColorMix = zeros([prod(self.dataset_parameters.n_pixels) 3],self.dataset_parameters.data_type);
                        color_mix_list = zeros([3 height(cds)]);
                    end

                    for i = 1:height(cds)
                        selection = cds(i, :);
                        maski = self.masks.Custom.(selection.ID)*selection.Weight;
                        switch self.CustomDetectorInterMask.Value
                            case "Additive"
                                custom_mask = custom_mask + maski;

                            case "Current-only"
                                if selection.ID == id
                                    custom_mask = maski;
                                end

                            case "Intersection"
                                if i == 1
                                    custom_mask = maski;
                                else
                                    custom_mask = custom_mask & maski;
                                end

                            case "Union"
                                custom_mask = custom_mask | maski;

                            case "Color Mix"
                                color_masks(i,:) = maski(:);
                                color_mix_list(:,i) = self.annotations.Custom.(selection.ID){1}.UserData.Color;
                                custom_mask = custom_mask | maski;
                        end
                    end

                    % Update images if the mask actually changed OR not a changing event
                    if ~isequal(self.images.DiffractionMask, custom_mask) || is_static_event(self, event)
                        self.images.DiffractionMask = custom_mask;
                        self.images.Real = gather(reshape(reshape(custom_mask,1,[])*self.data, self.dataset_parameters.n_frames));
                        
                        if strcmp(self.CustomDetectorInterMask.Value, "Color Mix")
                            self.masks.CustomColorMix = permute(reshape((color_mix_list*color_masks)',[self.dataset_parameters.n_pixels 3]),[2 1 3]);
                            self.images.RealColorMix = gather(rescale(reshape((color_mix_list*color_masks*self.data)',[self.dataset_parameters.n_frames 3])));
                        end

                    end

                    plot_all_patterns(self, event)
                end
                debug_toc(self, event, "", debug_time)
            end

        end

        % Callback function: BandpassFilter, BandpassFilter, 
        % ...and 5 other components
        function first_moment(self, event)
            % Function called when the user applies a filter to iDPC/dDPC
            % or iCoM/dCoM images, or saves a vector field image
            % 
            % Parameters:
            %    self (Quant4D)
            %    event (event.EventData)
            %
            % Returns:
            %    None

            switch event.Source
                case self.SaveVecMenu
                    % save vector field as image and figure
                    save_vector_field(self);
                    
                case {self.BandpassFilterLow, self.BandpassFilterHigh}
                    % update self.BandpassFilter RangeSlider
                    self.BandpassFilter.Value = sort([self.BandpassFilterLow.Value,self.BandpassFilterHigh.Value]);
                    self.BandpassFilterLow.Value = min(self.BandpassFilter.Value);
                    self.BandpassFilterHigh.Value = max(self.BandpassFilter.Value);

                case self.BandpassFilter
                    % update self.BandpassFilterLow and
                    % self.BandpassFilterLow spinners
                    self.BandpassFilterLow.Value = event.Value(1);
                    self.BandpassFilterHigh.Value = event.Value(2);
            end

            % update images
            mock_UI_callbacks(self, self.UpdateImages)
        end

        % Button pushed function: ShowCoMMagnitudeWindow, 
        % ...and 17 other components
        function show_window(self, event)
            % Function called when the user presses any of the Show*Window
            % buttons
            % 
            % Parameters:
            %    self (Quant4D)
            %    event (event.EventData)
            %
            % Returns:
            %    None

            debug_time = tic;

            id = self.DisplayImage.Value;
            switch event.Source
                case self.ShowImageWindow
                    % Show selected image
                    figure(self.figures.(id));
                    %movegui(self.figures.(id))
                
                case self.ShowMaskWindow
                    % Show diffraction or Real `space` mask
                    % for the selected image
                    id = self.image_axes.(id).UserData.space + "Mask";
                    figure(self.figures.(id));
                    %movegui(self.figures.(id))
                
                otherwise
                    % All other `self.Show***Window`
                    id = event.Source.Tag;
                    figure(self.figures.(id))
                    %movegui(self.figures.(id))

                    % If `id` is one of the available images, select it
                    if ~self.DisplayLock.Value && ...
                       ~strcmp(self.DisplayImage.Value, id) && ...
                       ismember(id, self.DisplayImage.ItemsData)
                        mock_UI_callbacks(self, self.DisplayImage, id)
                    end
            end

            debug_toc(self, event, "", debug_time)
        end

        % Callback function: SetAllDiffractionWindows, SetAllRealWindows, 
        % ...and 6 other components
        function resize_window(self, event)
            % Function called when the user sets the size of one or more
            % windows from the `Window size and orientation` panel in the
            % `Windows` tab of the Settings UI. 
            % 
            % Parameters:
            %    self (Quant4D)
            %    event (event.EventData)
            %
            % Returns:
            %    None

            % `Diffraction` or `Real` space from source Tag
            space = event.Source.Tag;
            
            % user-defined window size from Settings UI window
            window_size = [self.("Set" + space + "WindowWidth").Value ...
                           self.("Set" + space + "WindowHeight").Value];

            % ensure window size is in range [1, screen_avail]
            window_size = clip(window_size, 1, self.sys_constants.screen_avail(3:4));

            switch event.Source
                case {self.SetDiffractionWindow, self.SetRealWindow}
                    % Only resize currently selected image window
                    id = self.DisplayImage.Value;

                    % If the selected image is not of that space (i.e.
                    % self.DisplayLock.Value = true), then resize the
                    % primary image window for that space instead
                    if self.image_axes.(id).UserData.space ~= space
                        id = space;
                    end

                    % get image axes position
                    pos = self.image_axes.(id).Position;

                    % set window size
                    self.figures.(id).Position(3:4) = window_size;
                    
                    % make sure figure window stays on the screen
                    off_screen = self.figures.(id).Position(1:2) + window_size > self.sys_constants.screen_avail(3:4);
                    if any(off_screen)
                        shift = (self.sys_constants.screen_size(3:4) - (self.figures.(id).Position(1:2) + window_size + [0, self.sys_constants.title_height])).*(off_screen);
                        self.figures.(id).Position(1:2) = self.figures.(id).Position(1:2) + shift;
                    end

                    % make sure image axes position remains unchanged after
                    % window size change
                    self.image_axes.(id).Position = pos;
                
                case {self.SetAllDiffractionWindows, self.SetAllRealWindows}
                    % Resize all image windows of the given space
                    for fig = self.ui_groups.image_figures(self.ui_groups.image_space == space)'
                        % get image axes and position
                        ax = fig.CurrentAxes;
                        pos = ax.Position;

                        % set window size
                        fig.Position(3:4) = window_size;
                        
                        % make sure figure window stays on the screen
                        off_screen = fig.Position(1:2) + window_size > self.sys_constants.screen_size(3:4);
                        if off_screen
                            shift = (self.sys_constants.screen_size(3:4) - (fig.Position(1:2) + window_size + [0, self.sys_constants.title_height])).*(off_screen);
                            fig.Position(1:2) = fig.Position(1:2) + shift;
                        end

                        % make sure image axes position remains unchanged after
                        % window size change
                        ax.Position = pos;
                    end
            end

            % always keep diffraction_dropdown in the upper right hand
            % corner of the diffraction figure
            self.diffraction_dropdown.Position = [0, self.figures.Diffraction.Position(4) - self.diffraction_dropdown.Position(4), 65, 22];
        end

        % Callback function: CalculationPolicy, UpdateImages
        function update_images(self, event)
            % Function called when the user changes the CalculationPolicy
            % (`Active`, `Reduced` or `Passive`) or explicitly refreshes
            % the images (can also be called programmatically). 
            % 
            % Parameters:
            %    self (Quant4D)
            %    event (event.EventData)
            %
            % Returns:
            %    None

            switch event.Source
                case self.CalculationPolicy
                    % Update once if not passive
                    if event.Value
                        mock_UI_callbacks(self, self.UpdateImages);
                    end

                case self.UpdateImages
                    % Calculate and update all images by triggering
                    % detector callbacks
                    switch self.Mode.Value
                        case "Preview"
                            preview_callbacks(self, event)

                        case "Alignment"
                            transmitted_beam_callbacks(self, event)
                        
                        case {'Annular' 'CoM' 'DPC'}
                            annular_detector_callbacks(self, event)
                        
                        case "Virtual"
                            virtual_aperture_callbacks(self, event)
                        
                        case "Custom"
                            custom_detector_callbacks(self, event)
                    end

                    % Trigger real-space ROI callbacks
                    if self.Mode.Value ~= "Preview"
                        realspace_ROI_callbacks(self, event)
                    end
            end
        end

        % Menu selected function: ResetQuant4DMenu
        function reset_Quant4D(self, event)
            % Function to revert all UI properties to their initial state
            % and unload all data from RAM and the GPU, if used.
            % 
            % Parameters:
            %    self (Quant4D)
            %    event (event.EventData)
            %
            % Returns:
            %    None

            % A state like just start-up without import
            unload_data(self)
            mock_UI_callbacks(self, self.Mode, "Preview")
        end

        % Menu selected function: EnableallUIsMenu
        function enable_all_UI(self, event)
            % Context menu item to re-enable all UI elements. Mostly used
            % for debugging. 
            % 
            % Parameters:
            %    self (Quant4D)
            %    event (event.EventData)
            %
            % Returns:
            %    None

            % Try to delete any progress window
            try delete(self.tmp_variables.progress_dialog); catch; end
            
            % Enable all windows
            enable_windows(self,true)
        end

        % Menu selected function: Test1Menu
        function test1(self, event)
            % User editable function for debugging. 
            % 
            % Parameters:
            %    self (Quant4D)
            %    event (event.EventData)
            %
            % Returns:
            %    None

            % places main window at top left of main screen, with settings, diffraction and real space windows immediately adjacent
            self.Quant4D_Fig.Position(1:2) = [1,self.sys_constants.screen_size(4) - self.Quant4D_Fig.Position(4)-self.sys_constants.title_height];
            for ii=1:2 % running it twice makes it work better for some reason
                self.figures.Settings.Position(1) = sum(self.Quant4D_Fig.Position([1,3])) + 1;
                self.figures.Diffraction.Position(1) = sum(self.figures.Settings.Position([1,3])) + 1;
                self.figures.Preview.Position(1) = sum(self.figures.Settings.Position([1,3])) + 1;
                self.figures.Real.Position(1) = sum(self.figures.Diffraction.Position([1,3])) + 1;
                self.figures.Import.Position(1) = sum(self.figures.Diffraction.Position([1,3])) + 1;
                self.figures.Settings.Position(2:4) = self.Quant4D_Fig.Position(2:4);
                self.figures.Diffraction.Position(2:4) = self.Quant4D_Fig.Position([2,4,4]);
                self.figures.Preview.Position(2:4) = self.Quant4D_Fig.Position([2,4,4]);
                self.figures.Real.Position(2:4) = self.Quant4D_Fig.Position([2,4,4]);
                self.figures.Import.Position(2) = self.figures.Preview.Position(2)+self.figures.Preview.Position(4)-self.figures.Import.Position(4);
            end
        end

        % Menu selected function: Test2Menu
        function test2(self, event)
            % User editable function for debugging. 
            % 
            % Parameters:
            %    self (Quant4D)
            %    event (event.EventData)
            %
            % Returns:
            %    None

            fprintf(""); % Can be used for debugging or interfacing with internal data.
            % Just right click on the "Import" button and select Test2
        end

        % Close request function: Quant4D_Fig
        function close_function(self, event)
            % Function called to ensure that all figure windows and any
            % progress dialogs are closed when the self exits.
            % 
            % Parameters:
            %    self (Quant4D)
            %    event (event.EventData)
            %
            % Returns:
            %    None

            % close the progress bar if its open
            try delete(self.tmp_variables.progress_dialog);catch;end

            % make sure all figures are closed after the self is closed

            try figs = self.ui_groups.image_figures; catch; figs =[]; end
            delete(self);
            
            for ii = 1:numel(figs)
                try close(figs(ii)); catch; end
            end
            clear figs;
        end

        % Callback function: ShowVariables, VariablesTree
        function variable_viewer(self, event)
            % Function used to display or hide the variable viewer treenode
            % in the Settings UI. 
            % 
            % Parameters:
            %    self (Quant4D)
            %    event (event.EventData)
            %
            % Returns:
            %    None

            switch self.ShowVariables.Value
                case true
                    self.VariablesTab.Parent = self.SettingsTabGroup;
                    self.ShowVariables.Text = "Hide all variables";
                    self.SettingsTabGroup.SelectedTab = self.VariablesTab;
                case false
                    self.VariablesTab.Parent = [];
                    self.ShowVariables.Text = "Show all variables";
            end
            % Get currently selected node
            selectedNode = self.VariablesTree.SelectedNodes;

            % Only show these variables/structures 
            group_names = {"dataset_parameters";
                           "common_parameters";
                           "sys_constants";
                           "figures";
                           "images";
                           "masks";
                           "image_axes";
                           "annotations";
                           "ui_groups"};

            % Refresh TreeNode as needed
            for i_group = 1:numel(group_names)
                group_name = group_names{i_group};
                
                % Add TreeNode if it doesn't already exist or is invalid
                if ~isfield(self.variable_nodes,group_name) || ...
                   ~isa(self.variable_nodes.(group_name),'matlab.ui.container.TreeNode') || ...
                    ~isvalid(self.variable_nodes.(group_name))

                    self.variable_nodes.(group_name) = uitreenode(self.VariablesTree, "Text", group_name);
                end
                
                % Populate the branches on the TreeNode
                get_fields(self, self.variable_nodes.(group_name), self.(group_name))
            end

            % If node is selected, show variable data in self.VariablesTable
            if ~isempty(selectedNode)
                % get parent
                parent = selectedNode.Parent;
                tree_path = selectedNode.Text;

                % Get all TreeNode parents above it
                while isa(parent,'matlab.ui.container.TreeNode')
                    tree_path = [parent.Text,'.',tree_path];
                    parent = parent.Parent;
                end

                % Absolute path 
                tree_path = ['self.', tree_path];

                % Get variable in a suitable way for displaying
                self.VariablesTable.Data = get_variable_display(tree_path);
            end            

            function value = get_variable_display(variable_path)
                value = [];

                % get the variable from the text string
                try
                    item = eval(variable_path);
                catch 
                    return
                end

                item_class = class(item);

                switch item_class
                    case 'char'
                        value = string(item);

                    case {'string' 'cell'}
                        if isscalar(item)
                            value = item;
                        elseif isrow(item)
                            value = item';
                        else
                            value = item;
                        end
                    
                    case {'images.roi.Circle', ...
                          'images.roi.Rectangle', ...
                          'images.roi.Line', ...
                          'images.roi.Point', ...
                          'images.roi.Polygon', ...
                          'matlab.graphics.shape.Rectangle', ...
                          'matlab.ui.control.Button'}
                        try
                            item_class = arrayfun(@(r) string(class(r)), item, 'UniformOutput', false);

                            if all(isprop(item,'Name'))
                                value = reshape({item.Name},[],1);
                            elseif all(isprop(item,'Tag'))
                                value = reshape({item.Tag},[],1);
                            else
                                error('');
                            end

                            if numel(item_class) == numel(value) && isequal(size(item_class),size(value))
                                value = table([value,item_class]);
                            end

                        catch
                            try
                                value = arrayfun(@(r) class(r), item, 'UniformOutput', false);
                            catch
                                value = item_class;
                            end
                        end

                    case 'struct'
                        try
                            value = [fieldnames(item), struct2cell(item)];
                        catch
                            value = fieldnames(item);
                        end

                        if ~iscolumn(value)
                            value = cell2table(value);
                        end

                    otherwise
                        if isnumeric(item)
                            if ~iscolumn(item) && ~isrow(item) && ndims(item)>=2
                                % print shape and class of array instead of
                                % the array itself
                                value = sprintf("[%s %s]",string(size(item)).join("×"),class(item));
                            else
                                % return the item itself
                                value = item;
                            end
                        
                        elseif islogical(item)
                            if isscalar(item)
                                value = string(item);
                            else
                                value = sprintf("[%s %s]",string(size(item)).join("×"),class(item));
                            end

                        elseif isgraphics(item)
                            if isscalar(item)
                                value = string(item_class);
                            else
                                try
                                    item_class = arrayfun(@(r) string(class(r)), item, 'UniformOutput', false);
                                    
                                    if all(isprop(item,'Name'))
                                        value = reshape({item.Name},[],1);
                                    elseif all(isprop(item,'Tag'))
                                        value = reshape({item.Tag},[],1);
                                    elseif all(isprop(item,'Text'))
                                        value = reshape({item.Text},[],1);
                                    else
                                        error('')
                                    end

                                    if numel(item_class) == numel(value) && isequal(size(item_class),size(value))
                                        value = table([value,item_class]);
                                    end
                                catch 
                                    try
                                        value = arrayfun(@(r) class(r), item, 'UniformOutput', false);
                                    catch
                                        value = item_class;
                                    end
                                end
                            end
                        else
                            value = "Unknown";
                        end
                end

                if ~isscalar(item) && isrow(item) || (isrow(value) && ~isstring(value)) && ~istable(value)
                    value = value';
                end

                if ischar(value)
                    value = string(value);
                end

                switch size(value,2)
                    case 2
                        self.VariablesTable.ColumnName = {"Name", "Value"};
                        self.VariablesTable.ColumnWidth = 'auto';
                    otherwise
                        self.VariablesTable.ColumnName = "Value";
                        self.VariablesTable.ColumnWidth = '1x';
                end
                
            end
        end
    end

    % Component initialization
    methods (Access = private)

        % Create UIFigure and components
        function createComponents(self)

            % Get the file path for locating images
            pathToMLAPP = fileparts(mfilename('fullpath'));

            % Create Quant4D_Fig and hide until all components are created
            self.Quant4D_Fig = uifigure('Visible', 'off');
            self.Quant4D_Fig.AutoResizeChildren = 'off';
            self.Quant4D_Fig.Position = [1 1 262 472];
            self.Quant4D_Fig.Name = 'Quant4D';
            self.Quant4D_Fig.Resize = 'off';
            self.Quant4D_Fig.CloseRequestFcn = createCallbackFcn(self, @close_function, true);

            % Create SavePanel
            self.SavePanel = uipanel(self.Quant4D_Fig);
            self.SavePanel.AutoResizeChildren = 'off';
            self.SavePanel.BorderType = 'none';
            self.SavePanel.FontWeight = 'bold';
            self.SavePanel.Position = [-697 -35 424 500];

            % Create SaveGrid
            self.SaveGrid = uigridlayout(self.SavePanel);
            self.SaveGrid.ColumnWidth = {'1x'};
            self.SaveGrid.RowHeight = {'fit', '1x', 'fit'};
            self.SaveGrid.ColumnSpacing = 4;
            self.SaveGrid.RowSpacing = 0;
            self.SaveGrid.Padding = [0 0 0 0];

            % Create SaveDirectoryGrid
            self.SaveDirectoryGrid = uigridlayout(self.SaveGrid);
            self.SaveDirectoryGrid.ColumnWidth = {'fit', '1x'};
            self.SaveDirectoryGrid.RowHeight = {24};
            self.SaveDirectoryGrid.ColumnSpacing = 4;
            self.SaveDirectoryGrid.RowSpacing = 4;
            self.SaveDirectoryGrid.Padding = [4 4 4 4];
            self.SaveDirectoryGrid.Layout.Row = 1;
            self.SaveDirectoryGrid.Layout.Column = 1;

            % Create SaveDirectoryButton
            self.SaveDirectoryButton = uibutton(self.SaveDirectoryGrid, 'push');
            self.SaveDirectoryButton.ButtonPushedFcn = createCallbackFcn(self, @save_callbacks, true);
            self.SaveDirectoryButton.BackgroundColor = [0.702 1 0.702];
            self.SaveDirectoryButton.FontName = 'arial';
            self.SaveDirectoryButton.FontWeight = 'bold';
            self.SaveDirectoryButton.Tooltip = {'Select saving/export directory'};
            self.SaveDirectoryButton.Layout.Row = 1;
            self.SaveDirectoryButton.Layout.Column = 1;
            self.SaveDirectoryButton.Text = 'Directory';

            % Create SaveDirectoryPath
            self.SaveDirectoryPath = uieditfield(self.SaveDirectoryGrid, 'text');
            self.SaveDirectoryPath.ValueChangedFcn = createCallbackFcn(self, @save_callbacks, true);
            self.SaveDirectoryPath.Tooltip = {'Saving/Export directory'};
            self.SaveDirectoryPath.Layout.Row = 1;
            self.SaveDirectoryPath.Layout.Column = 2;

            % Create SaveTabGroup
            self.SaveTabGroup = uitabgroup(self.SaveGrid);
            self.SaveTabGroup.AutoResizeChildren = 'off';
            self.SaveTabGroup.SelectionChangedFcn = createCallbackFcn(self, @export_callbacks, true);
            self.SaveTabGroup.Layout.Row = 2;
            self.SaveTabGroup.Layout.Column = 1;

            % Create SaveImagesTab
            self.SaveImagesTab = uitab(self.SaveTabGroup);
            self.SaveImagesTab.AutoResizeChildren = 'off';
            self.SaveImagesTab.Title = 'Save Images';

            % Create SaveImagesGrid
            self.SaveImagesGrid = uigridlayout(self.SaveImagesTab);
            self.SaveImagesGrid.ColumnWidth = {'1x'};
            self.SaveImagesGrid.RowHeight = {'fit', 'fit', '1x', 'fit'};
            self.SaveImagesGrid.ColumnSpacing = 4;
            self.SaveImagesGrid.RowSpacing = 4;
            self.SaveImagesGrid.Padding = [4 4 4 4];

            % Create SaveImagePrefixGrid
            self.SaveImagePrefixGrid = uigridlayout(self.SaveImagesGrid);
            self.SaveImagePrefixGrid.ColumnWidth = {'fit', '1x'};
            self.SaveImagePrefixGrid.RowHeight = {24};
            self.SaveImagePrefixGrid.ColumnSpacing = 4;
            self.SaveImagePrefixGrid.RowSpacing = 4;
            self.SaveImagePrefixGrid.Padding = [0 0 0 0];
            self.SaveImagePrefixGrid.Layout.Row = 1;
            self.SaveImagePrefixGrid.Layout.Column = 1;

            % Create FilenamePrefixLabel
            self.FilenamePrefixLabel = uilabel(self.SaveImagePrefixGrid);
            self.FilenamePrefixLabel.HorizontalAlignment = 'right';
            self.FilenamePrefixLabel.Layout.Row = 1;
            self.FilenamePrefixLabel.Layout.Column = 1;
            self.FilenamePrefixLabel.Text = 'Filename Prefix';

            % Create SaveImagePrefix
            self.SaveImagePrefix = uieditfield(self.SaveImagePrefixGrid, 'text');
            self.SaveImagePrefix.ValueChangedFcn = createCallbackFcn(self, @save_callbacks, true);
            self.SaveImagePrefix.Layout.Row = 1;
            self.SaveImagePrefix.Layout.Column = 2;

            % Create SavePrefixAngleGrid
            self.SavePrefixAngleGrid = uigridlayout(self.SaveImagesGrid);
            self.SavePrefixAngleGrid.ColumnWidth = {'fit', 'fit', 'fit', '1x'};
            self.SavePrefixAngleGrid.RowHeight = {'1x'};
            self.SavePrefixAngleGrid.ColumnSpacing = 6;
            self.SavePrefixAngleGrid.Padding = [0 0 0 0];
            self.SavePrefixAngleGrid.Layout.Row = 2;
            self.SavePrefixAngleGrid.Layout.Column = 1;

            % Create SavePrefixAngleLabel
            self.SavePrefixAngleLabel = uilabel(self.SavePrefixAngleGrid);
            self.SavePrefixAngleLabel.HorizontalAlignment = 'right';
            self.SavePrefixAngleLabel.Layout.Row = 1;
            self.SavePrefixAngleLabel.Layout.Column = 1;
            self.SavePrefixAngleLabel.Text = 'Include Annular Detector Angles in Filename';

            % Create SavePrefixAngleInner
            self.SavePrefixAngleInner = uicheckbox(self.SavePrefixAngleGrid);
            self.SavePrefixAngleInner.ValueChangedFcn = createCallbackFcn(self, @save_callbacks, true);
            self.SavePrefixAngleInner.Text = 'Inner';
            self.SavePrefixAngleInner.Layout.Row = 1;
            self.SavePrefixAngleInner.Layout.Column = 2;

            % Create SavePrefixAngleOuter
            self.SavePrefixAngleOuter = uicheckbox(self.SavePrefixAngleGrid);
            self.SavePrefixAngleOuter.ValueChangedFcn = createCallbackFcn(self, @save_callbacks, true);
            self.SavePrefixAngleOuter.Text = 'Outer';
            self.SavePrefixAngleOuter.Layout.Row = 1;
            self.SavePrefixAngleOuter.Layout.Column = 3;

            % Create SaveImageListGrid
            self.SaveImageListGrid = uigridlayout(self.SaveImagesGrid);
            self.SaveImageListGrid.ColumnWidth = {'1x', 'fit'};
            self.SaveImageListGrid.RowHeight = {'fit', '1x'};
            self.SaveImageListGrid.ColumnSpacing = 4;
            self.SaveImageListGrid.RowSpacing = 4;
            self.SaveImageListGrid.Padding = [0 0 0 0];
            self.SaveImageListGrid.Layout.Row = 3;
            self.SaveImageListGrid.Layout.Column = 1;

            % Create ImagestoSaveMultiselectwithCtrlShiftLabel
            self.ImagestoSaveMultiselectwithCtrlShiftLabel = uilabel(self.SaveImageListGrid);
            self.ImagestoSaveMultiselectwithCtrlShiftLabel.HorizontalAlignment = 'center';
            self.ImagestoSaveMultiselectwithCtrlShiftLabel.VerticalAlignment = 'bottom';
            self.ImagestoSaveMultiselectwithCtrlShiftLabel.FontName = 'Arial';
            self.ImagestoSaveMultiselectwithCtrlShiftLabel.FontWeight = 'bold';
            self.ImagestoSaveMultiselectwithCtrlShiftLabel.Layout.Row = 1;
            self.ImagestoSaveMultiselectwithCtrlShiftLabel.Layout.Column = [1 2];
            self.ImagestoSaveMultiselectwithCtrlShiftLabel.Text = 'Images to Save (Multi-select with Ctrl/Shift)';

            % Create SaveImageSelectAll
            self.SaveImageSelectAll = uicheckbox(self.SaveImageListGrid);
            self.SaveImageSelectAll.ValueChangedFcn = createCallbackFcn(self, @save_callbacks, true);
            self.SaveImageSelectAll.Text = 'Select All';
            self.SaveImageSelectAll.Layout.Row = 1;
            self.SaveImageSelectAll.Layout.Column = 2;

            % Create SaveImageList
            self.SaveImageList = uilistbox(self.SaveImageListGrid);
            self.SaveImageList.Items = {};
            self.SaveImageList.Multiselect = 'on';
            self.SaveImageList.ValueChangedFcn = createCallbackFcn(self, @save_callbacks, true);
            self.SaveImageList.FontName = 'Arial';
            self.SaveImageList.Layout.Row = 2;
            self.SaveImageList.Layout.Column = [1 2];
            self.SaveImageList.Value = {};

            % Create SaveImageFormatGrid
            self.SaveImageFormatGrid = uigridlayout(self.SaveImagesGrid);
            self.SaveImageFormatGrid.ColumnWidth = {'1x'};
            self.SaveImageFormatGrid.RowHeight = {20, 20};
            self.SaveImageFormatGrid.ColumnSpacing = 4;
            self.SaveImageFormatGrid.RowSpacing = 2;
            self.SaveImageFormatGrid.Padding = [0 0 0 0];
            self.SaveImageFormatGrid.Layout.Row = 4;
            self.SaveImageFormatGrid.Layout.Column = 1;

            % Create SaveImageTIFF
            self.SaveImageTIFF = uicheckbox(self.SaveImageFormatGrid);
            self.SaveImageTIFF.ValueChangedFcn = createCallbackFcn(self, @save_callbacks, true);
            self.SaveImageTIFF.Text = 'Raw data (single-precision), TIFF';
            self.SaveImageTIFF.Layout.Row = 1;
            self.SaveImageTIFF.Layout.Column = 1;
            self.SaveImageTIFF.Value = true;

            % Create SaveImagePNGGrid
            self.SaveImagePNGGrid = uigridlayout(self.SaveImageFormatGrid);
            self.SaveImagePNGGrid.ColumnWidth = {'fit', 'fit', 'fit', 40, '1x'};
            self.SaveImagePNGGrid.RowHeight = {'1x'};
            self.SaveImagePNGGrid.ColumnSpacing = 0;
            self.SaveImagePNGGrid.RowSpacing = 4;
            self.SaveImagePNGGrid.Padding = [0 0 0 0];
            self.SaveImagePNGGrid.Layout.Row = 2;
            self.SaveImagePNGGrid.Layout.Column = 1;

            % Create SaveImagePNG
            self.SaveImagePNG = uicheckbox(self.SaveImagePNGGrid);
            self.SaveImagePNG.ValueChangedFcn = createCallbackFcn(self, @save_callbacks, true);
            self.SaveImagePNG.Text = 'As-displayed, PNG; ';
            self.SaveImagePNG.Layout.Row = 1;
            self.SaveImagePNG.Layout.Column = 1;
            self.SaveImagePNG.Value = true;

            % Create SaveImageAnnotations
            self.SaveImageAnnotations = uicheckbox(self.SaveImagePNGGrid);
            self.SaveImageAnnotations.ValueChangedFcn = createCallbackFcn(self, @save_callbacks, true);
            self.SaveImageAnnotations.Text = 'with annotations, e.g. ROIs,';
            self.SaveImageAnnotations.Layout.Row = 1;
            self.SaveImageAnnotations.Layout.Column = 2;
            self.SaveImageAnnotations.Value = true;

            % Create SaveImgAnnotDPILabel
            self.SaveImgAnnotDPILabel = uilabel(self.SaveImagePNGGrid);
            self.SaveImgAnnotDPILabel.Layout.Row = 1;
            self.SaveImgAnnotDPILabel.Layout.Column = 3;
            self.SaveImgAnnotDPILabel.Text = 'DPI';

            % Create SaveImageDPI
            self.SaveImageDPI = uieditfield(self.SaveImagePNGGrid, 'numeric');
            self.SaveImageDPI.Limits = [1 Inf];
            self.SaveImageDPI.RoundFractionalValues = 'on';
            self.SaveImageDPI.ValueDisplayFormat = '%d';
            self.SaveImageDPI.ValueChangedFcn = createCallbackFcn(self, @save_callbacks, true);
            self.SaveImageDPI.Layout.Row = 1;
            self.SaveImageDPI.Layout.Column = 4;
            self.SaveImageDPI.Value = 72;

            % Create ExportDatasetTab
            self.ExportDatasetTab = uitab(self.SaveTabGroup);
            self.ExportDatasetTab.AutoResizeChildren = 'off';
            self.ExportDatasetTab.Title = 'Export Dataset';

            % Create ExportGrid
            self.ExportGrid = uigridlayout(self.ExportDatasetTab);
            self.ExportGrid.RowHeight = {'fit', 24, 'fit', 'fit', 'fit', '1x'};
            self.ExportGrid.ColumnSpacing = 6;
            self.ExportGrid.RowSpacing = 4;
            self.ExportGrid.Padding = [4 4 4 4];

            % Create ExportFileGrid
            self.ExportFileGrid = uigridlayout(self.ExportGrid);
            self.ExportFileGrid.ColumnWidth = {'fit', '1x', 'fit'};
            self.ExportFileGrid.RowHeight = {24};
            self.ExportFileGrid.ColumnSpacing = 4;
            self.ExportFileGrid.RowSpacing = 4;
            self.ExportFileGrid.Padding = [0 0 0 0];
            self.ExportFileGrid.Layout.Row = 1;
            self.ExportFileGrid.Layout.Column = [1 2];

            % Create FilenameLabel
            self.FilenameLabel = uilabel(self.ExportFileGrid);
            self.FilenameLabel.HorizontalAlignment = 'right';
            self.FilenameLabel.Layout.Row = 1;
            self.FilenameLabel.Layout.Column = 1;
            self.FilenameLabel.Text = 'Filename';

            % Create ExportFilename
            self.ExportFilename = uieditfield(self.ExportFileGrid, 'text');
            self.ExportFilename.ValueChangedFcn = createCallbackFcn(self, @export_callbacks, true);
            self.ExportFilename.Layout.Row = 1;
            self.ExportFilename.Layout.Column = 2;

            % Create ExportDimensionSuffix
            self.ExportDimensionSuffix = uicheckbox(self.ExportFileGrid);
            self.ExportDimensionSuffix.ValueChangedFcn = createCallbackFcn(self, @export_callbacks, true);
            self.ExportDimensionSuffix.Tooltip = {'To suffix the filename with image stack''s dimensions'};
            self.ExportDimensionSuffix.Text = 'Dimensions suffix';
            self.ExportDimensionSuffix.Layout.Row = 1;
            self.ExportDimensionSuffix.Layout.Column = 3;

            % Create ExportDataType
            self.ExportDataType = uidropdown(self.ExportGrid);
            self.ExportDataType.Items = {'HDF5 (*.h5)', 'Raw binary (*.raw)'};
            self.ExportDataType.ItemsData = {'h5', 'raw'};
            self.ExportDataType.ValueChangedFcn = createCallbackFcn(self, @export_callbacks, true);
            self.ExportDataType.Layout.Row = 2;
            self.ExportDataType.Layout.Column = 1;
            self.ExportDataType.Value = 'h5';

            % Create ExportByteOrder
            self.ExportByteOrder = uidropdown(self.ExportGrid);
            self.ExportByteOrder.Items = {'Little Endian', 'Big Endian'};
            self.ExportByteOrder.ItemsData = {'l', 'b'};
            self.ExportByteOrder.ValueChangedFcn = createCallbackFcn(self, @export_callbacks, true);
            self.ExportByteOrder.Layout.Row = 2;
            self.ExportByteOrder.Layout.Column = 2;
            self.ExportByteOrder.Value = 'l';

            % Create ExportPartialPixels
            self.ExportPartialPixels = uicheckbox(self.ExportGrid);
            self.ExportPartialPixels.ValueChangedFcn = createCallbackFcn(self, @export_callbacks, true);
            self.ExportPartialPixels.Tag = 'Export Diffraction';
            self.ExportPartialPixels.Text = '    Diffraction Partial Export';
            self.ExportPartialPixels.FontName = 'Arial';
            self.ExportPartialPixels.FontWeight = 'bold';
            self.ExportPartialPixels.Layout.Row = 3;
            self.ExportPartialPixels.Layout.Column = 1;

            % Create DiffractionPartialExportGrid
            self.DiffractionPartialExportGrid = uigridlayout(self.ExportGrid);
            self.DiffractionPartialExportGrid.ColumnWidth = {'1x', 80, '1x', 80};
            self.DiffractionPartialExportGrid.RowHeight = {24, 24, 24};
            self.DiffractionPartialExportGrid.ColumnSpacing = 4;
            self.DiffractionPartialExportGrid.RowSpacing = 2;
            self.DiffractionPartialExportGrid.Padding = [0 0 0 0];
            self.DiffractionPartialExportGrid.Layout.Row = 4;
            self.DiffractionPartialExportGrid.Layout.Column = 1;

            % Create BinningDistanceLabel_2
            self.BinningDistanceLabel_2 = uilabel(self.DiffractionPartialExportGrid);
            self.BinningDistanceLabel_2.HorizontalAlignment = 'right';
            self.BinningDistanceLabel_2.Layout.Row = 1;
            self.BinningDistanceLabel_2.Layout.Column = [1 3];
            self.BinningDistanceLabel_2.Text = 'Binning Distance';

            % Create DiffractionPartialExportPixelsDist
            self.DiffractionPartialExportPixelsDist = uispinner(self.DiffractionPartialExportGrid);
            self.DiffractionPartialExportPixelsDist.ValueChangingFcn = createCallbackFcn(self, @export_callbacks, true);
            self.DiffractionPartialExportPixelsDist.RoundFractionalValues = 'on';
            self.DiffractionPartialExportPixelsDist.ValueDisplayFormat = '%.0f';
            self.DiffractionPartialExportPixelsDist.ValueChangedFcn = createCallbackFcn(self, @export_callbacks, true);
            self.DiffractionPartialExportPixelsDist.Tag = 'Export Diffraction';
            self.DiffractionPartialExportPixelsDist.Tooltip = {'To bin n×n pixels into one (by averaging)'};
            self.DiffractionPartialExportPixelsDist.Layout.Row = 1;
            self.DiffractionPartialExportPixelsDist.Layout.Column = 4;
            self.DiffractionPartialExportPixelsDist.Value = 1;

            % Create xsub1Label_3
            self.xsub1Label_3 = uilabel(self.DiffractionPartialExportGrid);
            self.xsub1Label_3.HorizontalAlignment = 'right';
            self.xsub1Label_3.Layout.Row = 2;
            self.xsub1Label_3.Layout.Column = 1;
            self.xsub1Label_3.Interpreter = 'html';
            self.xsub1Label_3.Text = 'x<sub>1';

            % Create DiffractionPartialExportXStart
            self.DiffractionPartialExportXStart = uispinner(self.DiffractionPartialExportGrid);
            self.DiffractionPartialExportXStart.ValueChangingFcn = createCallbackFcn(self, @export_callbacks, true);
            self.DiffractionPartialExportXStart.RoundFractionalValues = 'on';
            self.DiffractionPartialExportXStart.ValueDisplayFormat = '%.0f';
            self.DiffractionPartialExportXStart.ValueChangedFcn = createCallbackFcn(self, @export_callbacks, true);
            self.DiffractionPartialExportXStart.Tag = 'Export Diffraction';
            self.DiffractionPartialExportXStart.Tooltip = {'Starting pixel on X (1st dimension of image stack) to import, in each frame'};
            self.DiffractionPartialExportXStart.Layout.Row = 2;
            self.DiffractionPartialExportXStart.Layout.Column = 2;
            self.DiffractionPartialExportXStart.Value = 1;

            % Create ysub1Label_3
            self.ysub1Label_3 = uilabel(self.DiffractionPartialExportGrid);
            self.ysub1Label_3.HorizontalAlignment = 'right';
            self.ysub1Label_3.Layout.Row = 2;
            self.ysub1Label_3.Layout.Column = 3;
            self.ysub1Label_3.Interpreter = 'html';
            self.ysub1Label_3.Text = 'y<sub>1';

            % Create DiffractionPartialExportYStart
            self.DiffractionPartialExportYStart = uispinner(self.DiffractionPartialExportGrid);
            self.DiffractionPartialExportYStart.ValueChangingFcn = createCallbackFcn(self, @export_callbacks, true);
            self.DiffractionPartialExportYStart.RoundFractionalValues = 'on';
            self.DiffractionPartialExportYStart.ValueDisplayFormat = '%.0f';
            self.DiffractionPartialExportYStart.ValueChangedFcn = createCallbackFcn(self, @export_callbacks, true);
            self.DiffractionPartialExportYStart.Tag = 'Export Diffraction';
            self.DiffractionPartialExportYStart.Tooltip = {'Starting pixel on Y (2nd dimension of image stack) to import, in each frame'};
            self.DiffractionPartialExportYStart.Layout.Row = 2;
            self.DiffractionPartialExportYStart.Layout.Column = 4;
            self.DiffractionPartialExportYStart.Value = 1;

            % Create ENPxXl
            self.ENPxXl = uilabel(self.DiffractionPartialExportGrid);
            self.ENPxXl.HorizontalAlignment = 'right';
            self.ENPxXl.Layout.Row = 3;
            self.ENPxXl.Layout.Column = 1;
            self.ENPxXl.Text = 'X';

            % Create DiffractionPartialExportX
            self.DiffractionPartialExportX = uispinner(self.DiffractionPartialExportGrid);
            self.DiffractionPartialExportX.ValueChangingFcn = createCallbackFcn(self, @export_callbacks, true);
            self.DiffractionPartialExportX.RoundFractionalValues = 'on';
            self.DiffractionPartialExportX.ValueDisplayFormat = '%.0f';
            self.DiffractionPartialExportX.ValueChangedFcn = createCallbackFcn(self, @export_callbacks, true);
            self.DiffractionPartialExportX.Tag = 'Export Diffraction';
            self.DiffractionPartialExportX.Tooltip = {'Total pixels after binning on X (1st dimension of image stack), in each frame'};
            self.DiffractionPartialExportX.Layout.Row = 3;
            self.DiffractionPartialExportX.Layout.Column = 2;
            self.DiffractionPartialExportX.Value = 1;

            % Create ENPxYl
            self.ENPxYl = uilabel(self.DiffractionPartialExportGrid);
            self.ENPxYl.HorizontalAlignment = 'right';
            self.ENPxYl.Layout.Row = 3;
            self.ENPxYl.Layout.Column = 3;
            self.ENPxYl.Text = 'Y';

            % Create DiffractionPartialExportY
            self.DiffractionPartialExportY = uispinner(self.DiffractionPartialExportGrid);
            self.DiffractionPartialExportY.ValueChangingFcn = createCallbackFcn(self, @export_callbacks, true);
            self.DiffractionPartialExportY.RoundFractionalValues = 'on';
            self.DiffractionPartialExportY.ValueDisplayFormat = '%.0f';
            self.DiffractionPartialExportY.ValueChangedFcn = createCallbackFcn(self, @export_callbacks, true);
            self.DiffractionPartialExportY.Tag = 'Export Diffraction';
            self.DiffractionPartialExportY.Tooltip = {'Total pixels after binning on Y (2nd dimension of image stack), in each frame'};
            self.DiffractionPartialExportY.Layout.Row = 3;
            self.DiffractionPartialExportY.Layout.Column = 4;
            self.DiffractionPartialExportY.Value = 1;

            % Create RealPartialExportGrid
            self.RealPartialExportGrid = uigridlayout(self.ExportGrid);
            self.RealPartialExportGrid.ColumnWidth = {'1x', 80, '1x', 80};
            self.RealPartialExportGrid.RowHeight = {24, 24, 24};
            self.RealPartialExportGrid.ColumnSpacing = 4;
            self.RealPartialExportGrid.RowSpacing = 2;
            self.RealPartialExportGrid.Padding = [0 0 0 0];
            self.RealPartialExportGrid.Layout.Row = 4;
            self.RealPartialExportGrid.Layout.Column = 2;

            % Create xsub1Label_4
            self.xsub1Label_4 = uilabel(self.RealPartialExportGrid);
            self.xsub1Label_4.HorizontalAlignment = 'right';
            self.xsub1Label_4.Layout.Row = 2;
            self.xsub1Label_4.Layout.Column = 1;
            self.xsub1Label_4.Interpreter = 'html';
            self.xsub1Label_4.Text = 'x<sub>1';

            % Create RealPartialExportXStart
            self.RealPartialExportXStart = uispinner(self.RealPartialExportGrid);
            self.RealPartialExportXStart.ValueChangingFcn = createCallbackFcn(self, @export_callbacks, true);
            self.RealPartialExportXStart.RoundFractionalValues = 'on';
            self.RealPartialExportXStart.ValueDisplayFormat = '%.0f';
            self.RealPartialExportXStart.ValueChangedFcn = createCallbackFcn(self, @export_callbacks, true);
            self.RealPartialExportXStart.Tag = 'Export Real';
            self.RealPartialExportXStart.Tooltip = {'Starting frame on X (3rd dimension of image stack) to import'};
            self.RealPartialExportXStart.Layout.Row = 2;
            self.RealPartialExportXStart.Layout.Column = 2;
            self.RealPartialExportXStart.Value = 1;

            % Create ysub1Label_4
            self.ysub1Label_4 = uilabel(self.RealPartialExportGrid);
            self.ysub1Label_4.HorizontalAlignment = 'right';
            self.ysub1Label_4.Layout.Row = 2;
            self.ysub1Label_4.Layout.Column = 3;
            self.ysub1Label_4.Interpreter = 'html';
            self.ysub1Label_4.Text = 'y<sub>1';

            % Create RealPartialExportYStart
            self.RealPartialExportYStart = uispinner(self.RealPartialExportGrid);
            self.RealPartialExportYStart.ValueChangingFcn = createCallbackFcn(self, @export_callbacks, true);
            self.RealPartialExportYStart.RoundFractionalValues = 'on';
            self.RealPartialExportYStart.ValueDisplayFormat = '%.0f';
            self.RealPartialExportYStart.ValueChangedFcn = createCallbackFcn(self, @export_callbacks, true);
            self.RealPartialExportYStart.Tag = 'Export Real';
            self.RealPartialExportYStart.Tooltip = {'Starting frame on Y (4th dimension of image stack) to import'};
            self.RealPartialExportYStart.Layout.Row = 2;
            self.RealPartialExportYStart.Layout.Column = 4;
            self.RealPartialExportYStart.Value = 1;

            % Create ENFrXl
            self.ENFrXl = uilabel(self.RealPartialExportGrid);
            self.ENFrXl.HorizontalAlignment = 'right';
            self.ENFrXl.Layout.Row = 3;
            self.ENFrXl.Layout.Column = 1;
            self.ENFrXl.Text = 'X';

            % Create RealPartialExportX
            self.RealPartialExportX = uispinner(self.RealPartialExportGrid);
            self.RealPartialExportX.ValueChangingFcn = createCallbackFcn(self, @export_callbacks, true);
            self.RealPartialExportX.RoundFractionalValues = 'on';
            self.RealPartialExportX.ValueDisplayFormat = '%.0f';
            self.RealPartialExportX.ValueChangedFcn = createCallbackFcn(self, @export_callbacks, true);
            self.RealPartialExportX.Tag = 'Export Real';
            self.RealPartialExportX.Tooltip = {'Total frames after sampling on X (3rd dimension of image stack)'};
            self.RealPartialExportX.Layout.Row = 3;
            self.RealPartialExportX.Layout.Column = 2;
            self.RealPartialExportX.Value = 1;

            % Create ENFrYl
            self.ENFrYl = uilabel(self.RealPartialExportGrid);
            self.ENFrYl.HorizontalAlignment = 'right';
            self.ENFrYl.Layout.Row = 3;
            self.ENFrYl.Layout.Column = 3;
            self.ENFrYl.Text = 'Y';

            % Create RealPartialExportY
            self.RealPartialExportY = uispinner(self.RealPartialExportGrid);
            self.RealPartialExportY.ValueChangingFcn = createCallbackFcn(self, @export_callbacks, true);
            self.RealPartialExportY.RoundFractionalValues = 'on';
            self.RealPartialExportY.ValueDisplayFormat = '%.0f';
            self.RealPartialExportY.ValueChangedFcn = createCallbackFcn(self, @export_callbacks, true);
            self.RealPartialExportY.Tag = 'Export Real';
            self.RealPartialExportY.Tooltip = {'Total frames after sampling on Y (4th dimension of image stack)'};
            self.RealPartialExportY.Layout.Row = 3;
            self.RealPartialExportY.Layout.Column = 4;
            self.RealPartialExportY.Value = 1;

            % Create SamplingIntervalLabel
            self.SamplingIntervalLabel = uilabel(self.RealPartialExportGrid);
            self.SamplingIntervalLabel.HorizontalAlignment = 'right';
            self.SamplingIntervalLabel.Layout.Row = 1;
            self.SamplingIntervalLabel.Layout.Column = [1 3];
            self.SamplingIntervalLabel.Text = 'Sampling Interval';

            % Create RealPartialExportFramesDist
            self.RealPartialExportFramesDist = uispinner(self.RealPartialExportGrid);
            self.RealPartialExportFramesDist.ValueChangingFcn = createCallbackFcn(self, @export_callbacks, true);
            self.RealPartialExportFramesDist.RoundFractionalValues = 'on';
            self.RealPartialExportFramesDist.ValueDisplayFormat = '%.0f';
            self.RealPartialExportFramesDist.ValueChangedFcn = createCallbackFcn(self, @export_callbacks, true);
            self.RealPartialExportFramesDist.Tag = 'Export Real';
            self.RealPartialExportFramesDist.Tooltip = {'Distance between sampling frames in both X & Y directions (neighboring frames have distance of 1)'};
            self.RealPartialExportFramesDist.Layout.Row = 1;
            self.RealPartialExportFramesDist.Layout.Column = 4;
            self.RealPartialExportFramesDist.Value = 1;

            % Create SummaryLabel
            self.SummaryLabel = uilabel(self.ExportGrid);
            self.SummaryLabel.HorizontalAlignment = 'center';
            self.SummaryLabel.VerticalAlignment = 'bottom';
            self.SummaryLabel.FontName = 'Arial';
            self.SummaryLabel.FontWeight = 'bold';
            self.SummaryLabel.Layout.Row = 5;
            self.SummaryLabel.Layout.Column = [1 2];
            self.SummaryLabel.Text = 'Summary';

            % Create ExportNotes
            self.ExportNotes = uitextarea(self.ExportGrid);
            self.ExportNotes.Editable = 'off';
            self.ExportNotes.FontName = 'Arial';
            self.ExportNotes.Layout.Row = 6;
            self.ExportNotes.Layout.Column = [1 2];

            % Create ExportPartialFrames
            self.ExportPartialFrames = uicheckbox(self.ExportGrid);
            self.ExportPartialFrames.ValueChangedFcn = createCallbackFcn(self, @export_callbacks, true);
            self.ExportPartialFrames.Tag = 'Export Real';
            self.ExportPartialFrames.Text = '    Real-space Partial Export';
            self.ExportPartialFrames.FontName = 'Arial';
            self.ExportPartialFrames.FontWeight = 'bold';
            self.ExportPartialFrames.Layout.Row = 3;
            self.ExportPartialFrames.Layout.Column = 2;

            % Create SaveExportButtonGrid
            self.SaveExportButtonGrid = uigridlayout(self.SaveGrid);
            self.SaveExportButtonGrid.ColumnWidth = {120, '1x', 120};
            self.SaveExportButtonGrid.RowHeight = {'1x'};
            self.SaveExportButtonGrid.ColumnSpacing = 8;
            self.SaveExportButtonGrid.Padding = [4 4 4 4];
            self.SaveExportButtonGrid.Layout.Row = 3;
            self.SaveExportButtonGrid.Layout.Column = 1;

            % Create SaveExport
            self.SaveExport = uibutton(self.SaveExportButtonGrid, 'push');
            self.SaveExport.ButtonPushedFcn = createCallbackFcn(self, @save_callbacks, true);
            self.SaveExport.FontName = 'Arial';
            self.SaveExport.FontWeight = 'bold';
            self.SaveExport.Layout.Row = 1;
            self.SaveExport.Layout.Column = 1;
            self.SaveExport.Text = 'Save Images';

            % Create SaveCloseButton
            self.SaveCloseButton = uibutton(self.SaveExportButtonGrid, 'push');
            self.SaveCloseButton.ButtonPushedFcn = createCallbackFcn(self, @export_callbacks, true);
            self.SaveCloseButton.FontName = 'Arial';
            self.SaveCloseButton.FontWeight = 'bold';
            self.SaveCloseButton.Layout.Row = 1;
            self.SaveCloseButton.Layout.Column = 3;
            self.SaveCloseButton.Text = 'Close';

            % Create ImportPanel
            self.ImportPanel = uipanel(self.Quant4D_Fig);
            self.ImportPanel.AutoResizeChildren = 'off';
            self.ImportPanel.BorderType = 'none';
            self.ImportPanel.FontWeight = 'bold';
            self.ImportPanel.Position = [548 -27 600 500];

            % Create ImportGrid
            self.ImportGrid = uigridlayout(self.ImportPanel);
            self.ImportGrid.ColumnWidth = {'1x', '1.8x'};
            self.ImportGrid.RowHeight = {24, '1x', 24};
            self.ImportGrid.ColumnSpacing = 8;
            self.ImportGrid.RowSpacing = 4;
            self.ImportGrid.Padding = [4 4 4 4];

            % Create ImportFileGrid
            self.ImportFileGrid = uigridlayout(self.ImportGrid);
            self.ImportFileGrid.ColumnWidth = {'fit', '1x'};
            self.ImportFileGrid.RowHeight = {'1x'};
            self.ImportFileGrid.ColumnSpacing = 4;
            self.ImportFileGrid.Padding = [0 0 0 0];
            self.ImportFileGrid.Layout.Row = 1;
            self.ImportFileGrid.Layout.Column = [1 2];

            % Create ImportFileSelect
            self.ImportFileSelect = uibutton(self.ImportFileGrid, 'push');
            self.ImportFileSelect.ButtonPushedFcn = createCallbackFcn(self, @import_select_file, true);
            self.ImportFileSelect.IconAlignment = 'center';
            self.ImportFileSelect.BackgroundColor = [0.702 1 0.702];
            self.ImportFileSelect.FontName = 'Arial';
            self.ImportFileSelect.FontWeight = 'bold';
            self.ImportFileSelect.Layout.Row = 1;
            self.ImportFileSelect.Layout.Column = 1;
            self.ImportFileSelect.Text = 'Select';

            % Create ImportFilePath
            self.ImportFilePath = uieditfield(self.ImportFileGrid, 'text');
            self.ImportFilePath.ValueChangedFcn = createCallbackFcn(self, @import_select_file, true);
            self.ImportFilePath.Layout.Row = 1;
            self.ImportFilePath.Layout.Column = 2;

            % Create ImportDatasetInfoPanel
            self.ImportDatasetInfoPanel = uipanel(self.ImportGrid);
            self.ImportDatasetInfoPanel.AutoResizeChildren = 'off';
            self.ImportDatasetInfoPanel.BorderType = 'none';
            self.ImportDatasetInfoPanel.TitlePosition = 'centertop';
            self.ImportDatasetInfoPanel.Title = 'Dataset Info';
            self.ImportDatasetInfoPanel.Layout.Row = [2 3];
            self.ImportDatasetInfoPanel.Layout.Column = 1;
            self.ImportDatasetInfoPanel.FontName = 'Arial';
            self.ImportDatasetInfoPanel.FontWeight = 'bold';
            self.ImportDatasetInfoPanel.FontSize = 14;

            % Create ImportDatasetInfoGrid
            self.ImportDatasetInfoGrid = uigridlayout(self.ImportDatasetInfoPanel);
            self.ImportDatasetInfoGrid.ColumnWidth = {'1x'};
            self.ImportDatasetInfoGrid.RowHeight = {48, 'fit', 'fit', 'fit', 'fit', '1x'};
            self.ImportDatasetInfoGrid.ColumnSpacing = 4;
            self.ImportDatasetInfoGrid.RowSpacing = 4;
            self.ImportDatasetInfoGrid.Padding = [0 0 0 4];

            % Create FileTypeButtonGroup
            self.FileTypeButtonGroup = uibuttongroup(self.ImportDatasetInfoGrid);
            self.FileTypeButtonGroup.AutoResizeChildren = 'off';
            self.FileTypeButtonGroup.SelectionChangedFcn = createCallbackFcn(self, @import_file_type, true);
            self.FileTypeButtonGroup.Tooltip = {'EMPAD'; '128x128 pixels'; 'Header: 0 bytes'; 'Footer: 1024 bytes'; '32-bit Real, Little endian'; ''; 'MEDIPIX'; '256x256 pixels'; 'Header: 384 bytes'; 'Footer: 0 bytes'; 'Unsigned integer, Big endian'; ''; 'MRC'; 'variable # of pixels'; 'Header: 1024 bytes'; 'Footer: 0 bytes'; 'Signed integer, Little endian'};
            self.FileTypeButtonGroup.BorderType = 'none';
            self.FileTypeButtonGroup.TitlePosition = 'centertop';
            self.FileTypeButtonGroup.Layout.Row = 1;
            self.FileTypeButtonGroup.Layout.Column = 1;
            self.FileTypeButtonGroup.FontWeight = 'bold';

            % Create EMPAD
            self.EMPAD = uitogglebutton(self.FileTypeButtonGroup);
            self.EMPAD.Tooltip = {'*.raw'; '128x128 pixels'; 'Data Offset: 0 bytes'; 'Frame Header: 0 bytes'; 'Frame Footer: 1024 bytes'; '32-bit Real, Little Endian'};
            self.EMPAD.Text = 'EMPAD';
            self.EMPAD.Position = [3 27 68 22];
            self.EMPAD.Value = true;

            % Create Medipix
            self.Medipix = uitogglebutton(self.FileTypeButtonGroup);
            self.Medipix.Tooltip = {'*.mib'; '256x256 pixels'; 'Data Offset: 0 bytes'; 'Frame Header: 384 bytes'; 'Frame Footer: 0 bytes'; 'Unsigned integer, Big Endian'};
            self.Medipix.Text = 'Medipix';
            self.Medipix.Position = [71 27 68 22];

            % Create MRC
            self.MRC = uitogglebutton(self.FileTypeButtonGroup);
            self.MRC.Tooltip = {'*.mrc'; 'Data Offset: 1024 bytes'; 'Frame Header: 0 bytes'; 'Frame Footer: 0 bytes'; 'Signed integer, Little Endian'};
            self.MRC.Text = 'MRC';
            self.MRC.Position = [139 27 68 22];

            % Create DM34
            self.DM34 = uitogglebutton(self.FileTypeButtonGroup);
            self.DM34.Tooltip = {'Gatan *.dm3/*.dm4'};
            self.DM34.Text = 'DM3/4';
            self.DM34.Position = [3 5 68 22];

            % Create HDF5
            self.HDF5 = uitogglebutton(self.FileTypeButtonGroup);
            self.HDF5.Tooltip = {'*.h5/*.hdf5'};
            self.HDF5.Text = 'HDF5';
            self.HDF5.Position = [71 5 68 22];

            % Create Custom
            self.Custom = uitogglebutton(self.FileTypeButtonGroup);
            self.Custom.Tooltip = {'E.g. simulated/raw data'};
            self.Custom.Text = 'Custom';
            self.Custom.Position = [139 5 68 22];

            % Create ImportDatasetStructureGrid
            self.ImportDatasetStructureGrid = uigridlayout(self.ImportDatasetInfoGrid);
            self.ImportDatasetStructureGrid.ColumnWidth = {'fit', '1x'};
            self.ImportDatasetStructureGrid.RowHeight = {24, 24, 24, 24, 24, 24};
            self.ImportDatasetStructureGrid.ColumnSpacing = 4;
            self.ImportDatasetStructureGrid.RowSpacing = 2;
            self.ImportDatasetStructureGrid.Padding = [0 0 0 0];
            self.ImportDatasetStructureGrid.Layout.Row = 2;
            self.ImportDatasetStructureGrid.Layout.Column = 1;

            % Create SubdatasetDropDownLabel
            self.SubdatasetDropDownLabel = uilabel(self.ImportDatasetStructureGrid);
            self.SubdatasetDropDownLabel.HorizontalAlignment = 'right';
            self.SubdatasetDropDownLabel.Layout.Row = 1;
            self.SubdatasetDropDownLabel.Layout.Column = 1;
            self.SubdatasetDropDownLabel.Text = 'Sub-dataset';

            % Create SubDataset
            self.SubDataset = uidropdown(self.ImportDatasetStructureGrid);
            self.SubDataset.Items = {};
            self.SubDataset.ValueChangedFcn = createCallbackFcn(self, @import_file_type, true);
            self.SubDataset.Tooltip = {'Some file formats (e.g. DM3, DM4 or HDF5) can contain multiple image-stacks in one file'};
            self.SubDataset.Layout.Row = 1;
            self.SubDataset.Layout.Column = 2;
            self.SubDataset.Value = {};

            % Create DataOffsetLabel
            self.DataOffsetLabel = uilabel(self.ImportDatasetStructureGrid);
            self.DataOffsetLabel.HorizontalAlignment = 'right';
            self.DataOffsetLabel.Layout.Row = 2;
            self.DataOffsetLabel.Layout.Column = 1;
            self.DataOffsetLabel.Text = 'Data Offset';

            % Create DataOffset
            self.DataOffset = uieditfield(self.ImportDatasetStructureGrid, 'numeric');
            self.DataOffset.Limits = [0 Inf];
            self.DataOffset.ValueDisplayFormat = '%d bytes';
            self.DataOffset.ValueChangedFcn = createCallbackFcn(self, @import_box_input, true);
            self.DataOffset.Tooltip = {'Number of bytes before the image stack in file (e.g. for metadata)'};
            self.DataOffset.Layout.Row = 2;
            self.DataOffset.Layout.Column = 2;

            % Create FrameHeaderLabel
            self.FrameHeaderLabel = uilabel(self.ImportDatasetStructureGrid);
            self.FrameHeaderLabel.HorizontalAlignment = 'right';
            self.FrameHeaderLabel.Layout.Row = 3;
            self.FrameHeaderLabel.Layout.Column = 1;
            self.FrameHeaderLabel.Text = 'Frame Header';

            % Create FrameHeader
            self.FrameHeader = uieditfield(self.ImportDatasetStructureGrid, 'numeric');
            self.FrameHeader.Limits = [0 Inf];
            self.FrameHeader.ValueDisplayFormat = '%d bytes';
            self.FrameHeader.ValueChangedFcn = createCallbackFcn(self, @import_box_input, true);
            self.FrameHeader.Tooltip = {'Number of bytes before the actual pattern in each frame (e.g. for metadata)'};
            self.FrameHeader.Layout.Row = 3;
            self.FrameHeader.Layout.Column = 2;

            % Create FrameFooterLabel
            self.FrameFooterLabel = uilabel(self.ImportDatasetStructureGrid);
            self.FrameFooterLabel.HorizontalAlignment = 'right';
            self.FrameFooterLabel.Layout.Row = 4;
            self.FrameFooterLabel.Layout.Column = 1;
            self.FrameFooterLabel.Text = 'Frame Footer';

            % Create FrameFooter
            self.FrameFooter = uieditfield(self.ImportDatasetStructureGrid, 'numeric');
            self.FrameFooter.Limits = [0 Inf];
            self.FrameFooter.ValueDisplayFormat = '%d bytes';
            self.FrameFooter.ValueChangedFcn = createCallbackFcn(self, @import_box_input, true);
            self.FrameFooter.Tooltip = {'Number of bytes after the actual pattern in each frame (e.g. for metadata)'};
            self.FrameFooter.Layout.Row = 4;
            self.FrameFooter.Layout.Column = 2;

            % Create DataTypeLabel
            self.DataTypeLabel = uilabel(self.ImportDatasetStructureGrid);
            self.DataTypeLabel.HorizontalAlignment = 'right';
            self.DataTypeLabel.Layout.Row = 5;
            self.DataTypeLabel.Layout.Column = 1;
            self.DataTypeLabel.Text = 'Data Type';

            % Create ImportDataType
            self.ImportDataType = uidropdown(self.ImportDatasetStructureGrid);
            self.ImportDataType.Items = {};
            self.ImportDataType.ValueChangedFcn = createCallbackFcn(self, @import_box_input, true);
            self.ImportDataType.Layout.Row = 5;
            self.ImportDataType.Layout.Column = 2;
            self.ImportDataType.Value = {};

            % Create ByteOrderDropDownLabel
            self.ByteOrderDropDownLabel = uilabel(self.ImportDatasetStructureGrid);
            self.ByteOrderDropDownLabel.HorizontalAlignment = 'right';
            self.ByteOrderDropDownLabel.Layout.Row = 6;
            self.ByteOrderDropDownLabel.Layout.Column = 1;
            self.ByteOrderDropDownLabel.Text = 'Byte Order';

            % Create ImportByteOrder
            self.ImportByteOrder = uidropdown(self.ImportDatasetStructureGrid);
            self.ImportByteOrder.Items = {'Little Endian', 'Big Endian'};
            self.ImportByteOrder.ItemsData = {'l', 'b'};
            self.ImportByteOrder.ValueChangedFcn = createCallbackFcn(self, @import_box_input, true);
            self.ImportByteOrder.Layout.Row = 6;
            self.ImportByteOrder.Layout.Column = 2;
            self.ImportByteOrder.Value = 'l';

            % Create ImportDimensionGrid
            self.ImportDimensionGrid = uigridlayout(self.ImportDatasetInfoGrid);
            self.ImportDimensionGrid.ColumnWidth = {'fit', 'fit', '1x', 'fit', '1x'};
            self.ImportDimensionGrid.RowHeight = {24, 24};
            self.ImportDimensionGrid.ColumnSpacing = 4;
            self.ImportDimensionGrid.RowSpacing = 4;
            self.ImportDimensionGrid.Padding = [0 0 0 0];
            self.ImportDimensionGrid.Layout.Row = 3;
            self.ImportDimensionGrid.Layout.Column = 1;

            % Create ImportPixelsLabel
            self.ImportPixelsLabel = uilabel(self.ImportDimensionGrid);
            self.ImportPixelsLabel.HorizontalAlignment = 'center';
            self.ImportPixelsLabel.FontName = 'Arial';
            self.ImportPixelsLabel.FontWeight = 'bold';
            self.ImportPixelsLabel.Layout.Row = 1;
            self.ImportPixelsLabel.Layout.Column = 1;
            self.ImportPixelsLabel.Text = 'Pixels';

            % Create XLabel_2
            self.XLabel_2 = uilabel(self.ImportDimensionGrid);
            self.XLabel_2.HorizontalAlignment = 'right';
            self.XLabel_2.Layout.Row = 1;
            self.XLabel_2.Layout.Column = 2;
            self.XLabel_2.Text = 'X';

            % Create ImportPixelsX
            self.ImportPixelsX = uieditfield(self.ImportDimensionGrid, 'numeric');
            self.ImportPixelsX.Limits = [1 Inf];
            self.ImportPixelsX.RoundFractionalValues = 'on';
            self.ImportPixelsX.ValueDisplayFormat = '%d';
            self.ImportPixelsX.ValueChangedFcn = createCallbackFcn(self, @import_box_input, true);
            self.ImportPixelsX.Tag = 'Import Diffraction';
            self.ImportPixelsX.HorizontalAlignment = 'center';
            self.ImportPixelsX.Tooltip = {'Number of pixels on X axis in each frame (1st dimension of image stack)'};
            self.ImportPixelsX.Layout.Row = 1;
            self.ImportPixelsX.Layout.Column = 3;
            self.ImportPixelsX.Value = 1;

            % Create YLabel_2
            self.YLabel_2 = uilabel(self.ImportDimensionGrid);
            self.YLabel_2.HorizontalAlignment = 'right';
            self.YLabel_2.Layout.Row = 1;
            self.YLabel_2.Layout.Column = 4;
            self.YLabel_2.Text = ' Y';

            % Create ImportPixelsY
            self.ImportPixelsY = uieditfield(self.ImportDimensionGrid, 'numeric');
            self.ImportPixelsY.Limits = [1 Inf];
            self.ImportPixelsY.RoundFractionalValues = 'on';
            self.ImportPixelsY.ValueDisplayFormat = '%d';
            self.ImportPixelsY.ValueChangedFcn = createCallbackFcn(self, @import_box_input, true);
            self.ImportPixelsY.Tag = 'Import Diffraction';
            self.ImportPixelsY.HorizontalAlignment = 'center';
            self.ImportPixelsY.Tooltip = {'Number of pixels on Y axis in each frame (2nd dimension of image stack)'};
            self.ImportPixelsY.Layout.Row = 1;
            self.ImportPixelsY.Layout.Column = 5;
            self.ImportPixelsY.Value = 1;

            % Create ImportFramesLabel
            self.ImportFramesLabel = uilabel(self.ImportDimensionGrid);
            self.ImportFramesLabel.HorizontalAlignment = 'center';
            self.ImportFramesLabel.FontName = 'Arial';
            self.ImportFramesLabel.FontWeight = 'bold';
            self.ImportFramesLabel.Layout.Row = 2;
            self.ImportFramesLabel.Layout.Column = 1;
            self.ImportFramesLabel.Text = 'Frames';

            % Create XLabel
            self.XLabel = uilabel(self.ImportDimensionGrid);
            self.XLabel.HorizontalAlignment = 'right';
            self.XLabel.Layout.Row = 2;
            self.XLabel.Layout.Column = 2;
            self.XLabel.Text = 'X';

            % Create ImportFramesX
            self.ImportFramesX = uieditfield(self.ImportDimensionGrid, 'numeric');
            self.ImportFramesX.Limits = [1 Inf];
            self.ImportFramesX.RoundFractionalValues = 'on';
            self.ImportFramesX.ValueDisplayFormat = '%d';
            self.ImportFramesX.ValueChangedFcn = createCallbackFcn(self, @import_box_input, true);
            self.ImportFramesX.Tag = 'Import Real';
            self.ImportFramesX.HorizontalAlignment = 'center';
            self.ImportFramesX.Tooltip = {'Number of frames on X axis (3rd dimension of image stack)'};
            self.ImportFramesX.Layout.Row = 2;
            self.ImportFramesX.Layout.Column = 3;
            self.ImportFramesX.Value = 1;

            % Create YLabel
            self.YLabel = uilabel(self.ImportDimensionGrid);
            self.YLabel.HorizontalAlignment = 'right';
            self.YLabel.Layout.Row = 2;
            self.YLabel.Layout.Column = 4;
            self.YLabel.Text = ' Y';

            % Create ImportFramesY
            self.ImportFramesY = uieditfield(self.ImportDimensionGrid, 'numeric');
            self.ImportFramesY.Limits = [1 Inf];
            self.ImportFramesY.RoundFractionalValues = 'on';
            self.ImportFramesY.ValueDisplayFormat = '%d';
            self.ImportFramesY.ValueChangedFcn = createCallbackFcn(self, @import_box_input, true);
            self.ImportFramesY.Tag = 'Import Real';
            self.ImportFramesY.HorizontalAlignment = 'center';
            self.ImportFramesY.Tooltip = {'Number of frames on Y axis (4th dimension of image stack)'};
            self.ImportFramesY.Layout.Row = 2;
            self.ImportFramesY.Layout.Column = 5;
            self.ImportFramesY.Value = 1;

            % Create ImportFileSizeGrid
            self.ImportFileSizeGrid = uigridlayout(self.ImportDatasetInfoGrid);
            self.ImportFileSizeGrid.ColumnWidth = {'fit', '1x'};
            self.ImportFileSizeGrid.RowHeight = {'fit', 'fit'};
            self.ImportFileSizeGrid.ColumnSpacing = 4;
            self.ImportFileSizeGrid.RowSpacing = 2;
            self.ImportFileSizeGrid.Padding = [0 0 0 0];
            self.ImportFileSizeGrid.Layout.Row = 4;
            self.ImportFileSizeGrid.Layout.Column = 1;

            % Create ImportActualFilesizeLabel
            self.ImportActualFilesizeLabel = uilabel(self.ImportFileSizeGrid);
            self.ImportActualFilesizeLabel.HorizontalAlignment = 'right';
            self.ImportActualFilesizeLabel.Layout.Row = 1;
            self.ImportActualFilesizeLabel.Layout.Column = 1;
            self.ImportActualFilesizeLabel.Text = 'Size:';

            % Create ImportActualFilesize
            self.ImportActualFilesize = uilabel(self.ImportFileSizeGrid);
            self.ImportActualFilesize.HorizontalAlignment = 'center';
            self.ImportActualFilesize.Tooltip = {'Actual physical file size'};
            self.ImportActualFilesize.Layout.Row = 1;
            self.ImportActualFilesize.Layout.Column = 2;
            self.ImportActualFilesize.Text = '';

            % Create ImportEstimatedFilesizeLabel
            self.ImportEstimatedFilesizeLabel = uilabel(self.ImportFileSizeGrid);
            self.ImportEstimatedFilesizeLabel.HorizontalAlignment = 'right';
            self.ImportEstimatedFilesizeLabel.Layout.Row = 2;
            self.ImportEstimatedFilesizeLabel.Layout.Column = 1;
            self.ImportEstimatedFilesizeLabel.Text = 'Est.:';

            % Create ImportEstimatedFilesize
            self.ImportEstimatedFilesize = uilabel(self.ImportFileSizeGrid);
            self.ImportEstimatedFilesize.HorizontalAlignment = 'center';
            self.ImportEstimatedFilesize.Tooltip = {'File size calculated from info above. Size after the image stack (the "data tail") is implicit, thus may not be accurate'};
            self.ImportEstimatedFilesize.Layout.Row = 2;
            self.ImportEstimatedFilesize.Layout.Column = 2;
            self.ImportEstimatedFilesize.Text = '';

            % Create DatasetInfofromMetadataLabel
            self.DatasetInfofromMetadataLabel = uilabel(self.ImportDatasetInfoGrid);
            self.DatasetInfofromMetadataLabel.HorizontalAlignment = 'center';
            self.DatasetInfofromMetadataLabel.VerticalAlignment = 'bottom';
            self.DatasetInfofromMetadataLabel.FontName = 'Arial';
            self.DatasetInfofromMetadataLabel.FontWeight = 'bold';
            self.DatasetInfofromMetadataLabel.Layout.Row = 5;
            self.DatasetInfofromMetadataLabel.Layout.Column = 1;
            self.DatasetInfofromMetadataLabel.Text = 'Dataset Info from Metadata';

            % Create ImportFileMetadata
            self.ImportFileMetadata = uitextarea(self.ImportDatasetInfoGrid);
            self.ImportFileMetadata.Editable = 'off';
            self.ImportFileMetadata.FontName = 'Arial';
            self.ImportFileMetadata.Layout.Row = 6;
            self.ImportFileMetadata.Layout.Column = 1;

            % Create ImportOptionsPanel
            self.ImportOptionsPanel = uipanel(self.ImportGrid);
            self.ImportOptionsPanel.AutoResizeChildren = 'off';
            self.ImportOptionsPanel.BorderType = 'none';
            self.ImportOptionsPanel.TitlePosition = 'centertop';
            self.ImportOptionsPanel.Title = 'Import Options';
            self.ImportOptionsPanel.Layout.Row = 2;
            self.ImportOptionsPanel.Layout.Column = 2;
            self.ImportOptionsPanel.FontName = 'Arial';
            self.ImportOptionsPanel.FontWeight = 'bold';
            self.ImportOptionsPanel.FontSize = 14;

            % Create ImportOptionsGrid
            self.ImportOptionsGrid = uigridlayout(self.ImportOptionsPanel);
            self.ImportOptionsGrid.RowHeight = {24, 'fit', 'fit', 'fit', '1x'};
            self.ImportOptionsGrid.ColumnSpacing = 6;
            self.ImportOptionsGrid.RowSpacing = 6;
            self.ImportOptionsGrid.Padding = [0 0 0 4];

            % Create MemoryGrid
            self.MemoryGrid = uigridlayout(self.ImportOptionsGrid);
            self.MemoryGrid.ColumnWidth = {'fit', '1x'};
            self.MemoryGrid.RowHeight = {'1x'};
            self.MemoryGrid.ColumnSpacing = 8;
            self.MemoryGrid.RowSpacing = 4;
            self.MemoryGrid.Padding = [0 0 0 0];
            self.MemoryGrid.Layout.Row = 1;
            self.MemoryGrid.Layout.Column = [1 2];

            % Create MemoryType
            self.MemoryType = uidropdown(self.MemoryGrid);
            self.MemoryType.Items = {'Physical Memory', 'Virtual Mapping'};
            self.MemoryType.Tooltip = {'VIRTUAL MEMORY is best for most large datasets as it does not physically load the dataset into RAM. This can be significantly faster depending on drive speed and file size. HOWEVER - it is currently only beneficial for datasets with no header of footer.'; ''; 'Virtual mapping to the GPU is not recommended at this point. It is extremely fast to load, but still requires significant GPU memory resources.'};
            self.MemoryType.Layout.Row = 1;
            self.MemoryType.Layout.Column = 1;
            self.MemoryType.Value = 'Physical Memory';

            % Create GPU
            self.GPU = uidropdown(self.MemoryGrid);
            self.GPU.Items = {'GPU off'};
            self.GPU.ValueChangedFcn = createCallbackFcn(self, @import_box_input, true);
            self.GPU.Tooltip = {'GPU acceleration'};
            self.GPU.Layout.Row = 1;
            self.GPU.Layout.Column = 2;
            self.GPU.Value = 'GPU off';

            % Create ImportPartialPixels
            self.ImportPartialPixels = uicheckbox(self.ImportOptionsGrid);
            self.ImportPartialPixels.ValueChangedFcn = createCallbackFcn(self, @import_box_input, true);
            self.ImportPartialPixels.Tag = 'Import Diffraction';
            self.ImportPartialPixels.Text = '    Diffraction Partial Import';
            self.ImportPartialPixels.FontName = 'Arial';
            self.ImportPartialPixels.FontWeight = 'bold';
            self.ImportPartialPixels.Layout.Row = 2;
            self.ImportPartialPixels.Layout.Column = 1;

            % Create ImportPartialFrames
            self.ImportPartialFrames = uicheckbox(self.ImportOptionsGrid);
            self.ImportPartialFrames.ValueChangedFcn = createCallbackFcn(self, @import_box_input, true);
            self.ImportPartialFrames.Tag = 'Import Real';
            self.ImportPartialFrames.Text = '    Real-space Partial Import';
            self.ImportPartialFrames.FontName = 'Arial';
            self.ImportPartialFrames.FontWeight = 'bold';
            self.ImportPartialFrames.Layout.Row = 2;
            self.ImportPartialFrames.Layout.Column = 2;

            % Create DiffractionPartialImportGrid
            self.DiffractionPartialImportGrid = uigridlayout(self.ImportOptionsGrid);
            self.DiffractionPartialImportGrid.ColumnWidth = {'fit', '1x', 'fit', '1x'};
            self.DiffractionPartialImportGrid.RowHeight = {24, 24, 24};
            self.DiffractionPartialImportGrid.ColumnSpacing = 4;
            self.DiffractionPartialImportGrid.RowSpacing = 2;
            self.DiffractionPartialImportGrid.Padding = [0 0 0 0];
            self.DiffractionPartialImportGrid.Layout.Row = 3;
            self.DiffractionPartialImportGrid.Layout.Column = 1;

            % Create BinningDistanceLabel
            self.BinningDistanceLabel = uilabel(self.DiffractionPartialImportGrid);
            self.BinningDistanceLabel.HorizontalAlignment = 'right';
            self.BinningDistanceLabel.Enable = 'off';
            self.BinningDistanceLabel.Layout.Row = 1;
            self.BinningDistanceLabel.Layout.Column = [1 3];
            self.BinningDistanceLabel.Text = 'Binning Distance';

            % Create DiffractionPartialImportPixelsDist
            self.DiffractionPartialImportPixelsDist = uispinner(self.DiffractionPartialImportGrid);
            self.DiffractionPartialImportPixelsDist.RoundFractionalValues = 'on';
            self.DiffractionPartialImportPixelsDist.ValueDisplayFormat = '%.0f';
            self.DiffractionPartialImportPixelsDist.ValueChangedFcn = createCallbackFcn(self, @import_box_input, true);
            self.DiffractionPartialImportPixelsDist.Tag = 'Import Diffraction';
            self.DiffractionPartialImportPixelsDist.Enable = 'off';
            self.DiffractionPartialImportPixelsDist.Tooltip = {'To bin n×n pixels into one (by averaging)'};
            self.DiffractionPartialImportPixelsDist.Layout.Row = 1;
            self.DiffractionPartialImportPixelsDist.Layout.Column = 4;
            self.DiffractionPartialImportPixelsDist.Value = 1;

            % Create xsub1Label_5
            self.xsub1Label_5 = uilabel(self.DiffractionPartialImportGrid);
            self.xsub1Label_5.HorizontalAlignment = 'right';
            self.xsub1Label_5.Enable = 'off';
            self.xsub1Label_5.Layout.Row = 2;
            self.xsub1Label_5.Layout.Column = 1;
            self.xsub1Label_5.Interpreter = 'html';
            self.xsub1Label_5.Text = 'x<sub>1';

            % Create DiffractionPartialImportXStart
            self.DiffractionPartialImportXStart = uispinner(self.DiffractionPartialImportGrid);
            self.DiffractionPartialImportXStart.RoundFractionalValues = 'on';
            self.DiffractionPartialImportXStart.ValueDisplayFormat = '%.0f';
            self.DiffractionPartialImportXStart.ValueChangedFcn = createCallbackFcn(self, @import_box_input, true);
            self.DiffractionPartialImportXStart.Tag = 'Import Diffraction';
            self.DiffractionPartialImportXStart.Enable = 'off';
            self.DiffractionPartialImportXStart.Tooltip = {'Starting pixel on X (1st dimension of image stack) to import, in each frame'};
            self.DiffractionPartialImportXStart.Layout.Row = 2;
            self.DiffractionPartialImportXStart.Layout.Column = 2;
            self.DiffractionPartialImportXStart.Value = 1;

            % Create ysub1Label_5
            self.ysub1Label_5 = uilabel(self.DiffractionPartialImportGrid);
            self.ysub1Label_5.HorizontalAlignment = 'right';
            self.ysub1Label_5.Enable = 'off';
            self.ysub1Label_5.Layout.Row = 2;
            self.ysub1Label_5.Layout.Column = 3;
            self.ysub1Label_5.Interpreter = 'html';
            self.ysub1Label_5.Text = 'y<sub>1';

            % Create DiffractionPartialImportYStart
            self.DiffractionPartialImportYStart = uispinner(self.DiffractionPartialImportGrid);
            self.DiffractionPartialImportYStart.RoundFractionalValues = 'on';
            self.DiffractionPartialImportYStart.ValueDisplayFormat = '%.0f';
            self.DiffractionPartialImportYStart.ValueChangedFcn = createCallbackFcn(self, @import_box_input, true);
            self.DiffractionPartialImportYStart.Tag = 'Import Diffraction';
            self.DiffractionPartialImportYStart.Enable = 'off';
            self.DiffractionPartialImportYStart.Tooltip = {'Starting pixel on Y (2nd dimension of image stack) to import, in each frame'};
            self.DiffractionPartialImportYStart.Layout.Row = 2;
            self.DiffractionPartialImportYStart.Layout.Column = 4;
            self.DiffractionPartialImportYStart.Value = 1;

            % Create XLabel_3
            self.XLabel_3 = uilabel(self.DiffractionPartialImportGrid);
            self.XLabel_3.HorizontalAlignment = 'right';
            self.XLabel_3.Enable = 'off';
            self.XLabel_3.Layout.Row = 3;
            self.XLabel_3.Layout.Column = 1;
            self.XLabel_3.Text = 'X';

            % Create DiffractionPartialImportX
            self.DiffractionPartialImportX = uispinner(self.DiffractionPartialImportGrid);
            self.DiffractionPartialImportX.RoundFractionalValues = 'on';
            self.DiffractionPartialImportX.ValueDisplayFormat = '%.0f';
            self.DiffractionPartialImportX.ValueChangedFcn = createCallbackFcn(self, @import_box_input, true);
            self.DiffractionPartialImportX.Tag = 'Import Diffraction';
            self.DiffractionPartialImportX.Enable = 'off';
            self.DiffractionPartialImportX.Tooltip = {'Total pixels after binning on X (1st dimension of image stack), in each frame'};
            self.DiffractionPartialImportX.Layout.Row = 3;
            self.DiffractionPartialImportX.Layout.Column = 2;
            self.DiffractionPartialImportX.Value = 1;

            % Create YLabel_3
            self.YLabel_3 = uilabel(self.DiffractionPartialImportGrid);
            self.YLabel_3.HorizontalAlignment = 'right';
            self.YLabel_3.Enable = 'off';
            self.YLabel_3.Layout.Row = 3;
            self.YLabel_3.Layout.Column = 3;
            self.YLabel_3.Text = 'Y';

            % Create DiffractionPartialImportY
            self.DiffractionPartialImportY = uispinner(self.DiffractionPartialImportGrid);
            self.DiffractionPartialImportY.RoundFractionalValues = 'on';
            self.DiffractionPartialImportY.ValueDisplayFormat = '%.0f';
            self.DiffractionPartialImportY.ValueChangedFcn = createCallbackFcn(self, @import_box_input, true);
            self.DiffractionPartialImportY.Tag = 'Import Diffraction';
            self.DiffractionPartialImportY.Enable = 'off';
            self.DiffractionPartialImportY.Tooltip = {'Total pixels after binning on Y (2nd dimension of image stack), in each frame'};
            self.DiffractionPartialImportY.Layout.Row = 3;
            self.DiffractionPartialImportY.Layout.Column = 4;
            self.DiffractionPartialImportY.Value = 1;

            % Create RealPartialImportGrid
            self.RealPartialImportGrid = uigridlayout(self.ImportOptionsGrid);
            self.RealPartialImportGrid.ColumnWidth = {'fit', '1x', 'fit', '1x'};
            self.RealPartialImportGrid.RowHeight = {24, 24, 24};
            self.RealPartialImportGrid.ColumnSpacing = 4;
            self.RealPartialImportGrid.RowSpacing = 2;
            self.RealPartialImportGrid.Padding = [0 0 0 0];
            self.RealPartialImportGrid.Layout.Row = 3;
            self.RealPartialImportGrid.Layout.Column = 2;

            % Create SamplingIntervalLabel_2
            self.SamplingIntervalLabel_2 = uilabel(self.RealPartialImportGrid);
            self.SamplingIntervalLabel_2.HorizontalAlignment = 'right';
            self.SamplingIntervalLabel_2.Enable = 'off';
            self.SamplingIntervalLabel_2.Layout.Row = 1;
            self.SamplingIntervalLabel_2.Layout.Column = [1 3];
            self.SamplingIntervalLabel_2.Text = 'Sampling Interval';

            % Create RealPartialImportFramesDist
            self.RealPartialImportFramesDist = uispinner(self.RealPartialImportGrid);
            self.RealPartialImportFramesDist.RoundFractionalValues = 'on';
            self.RealPartialImportFramesDist.ValueDisplayFormat = '%.0f';
            self.RealPartialImportFramesDist.ValueChangedFcn = createCallbackFcn(self, @import_box_input, true);
            self.RealPartialImportFramesDist.Tag = 'Import Real';
            self.RealPartialImportFramesDist.Enable = 'off';
            self.RealPartialImportFramesDist.Tooltip = {'Distance between sampling frames in both X & Y directions (neighboring frames have distance of 1)'};
            self.RealPartialImportFramesDist.Layout.Row = 1;
            self.RealPartialImportFramesDist.Layout.Column = 4;
            self.RealPartialImportFramesDist.Value = 1;

            % Create xsub1Label_6
            self.xsub1Label_6 = uilabel(self.RealPartialImportGrid);
            self.xsub1Label_6.HorizontalAlignment = 'right';
            self.xsub1Label_6.Enable = 'off';
            self.xsub1Label_6.Layout.Row = 2;
            self.xsub1Label_6.Layout.Column = 1;
            self.xsub1Label_6.Interpreter = 'html';
            self.xsub1Label_6.Text = 'x<sub>1';

            % Create RealPartialImportXStart
            self.RealPartialImportXStart = uispinner(self.RealPartialImportGrid);
            self.RealPartialImportXStart.RoundFractionalValues = 'on';
            self.RealPartialImportXStart.ValueDisplayFormat = '%.0f';
            self.RealPartialImportXStart.ValueChangedFcn = createCallbackFcn(self, @import_box_input, true);
            self.RealPartialImportXStart.Tag = 'Import Real';
            self.RealPartialImportXStart.Enable = 'off';
            self.RealPartialImportXStart.Tooltip = {'Starting frame on X (3rd dimension of image stack) to import'};
            self.RealPartialImportXStart.Layout.Row = 2;
            self.RealPartialImportXStart.Layout.Column = 2;
            self.RealPartialImportXStart.Value = 1;

            % Create ysub1Label_6
            self.ysub1Label_6 = uilabel(self.RealPartialImportGrid);
            self.ysub1Label_6.HorizontalAlignment = 'right';
            self.ysub1Label_6.Enable = 'off';
            self.ysub1Label_6.Layout.Row = 2;
            self.ysub1Label_6.Layout.Column = 3;
            self.ysub1Label_6.Interpreter = 'html';
            self.ysub1Label_6.Text = 'y<sub>1';

            % Create RealPartialImportYStart
            self.RealPartialImportYStart = uispinner(self.RealPartialImportGrid);
            self.RealPartialImportYStart.RoundFractionalValues = 'on';
            self.RealPartialImportYStart.ValueDisplayFormat = '%.0f';
            self.RealPartialImportYStart.ValueChangedFcn = createCallbackFcn(self, @import_box_input, true);
            self.RealPartialImportYStart.Tag = 'Import Real';
            self.RealPartialImportYStart.Enable = 'off';
            self.RealPartialImportYStart.Tooltip = {'Starting frame on Y (4th dimension of image stack) to import'};
            self.RealPartialImportYStart.Layout.Row = 2;
            self.RealPartialImportYStart.Layout.Column = 4;
            self.RealPartialImportYStart.Value = 1;

            % Create INFrXl
            self.INFrXl = uilabel(self.RealPartialImportGrid);
            self.INFrXl.HorizontalAlignment = 'right';
            self.INFrXl.Enable = 'off';
            self.INFrXl.Layout.Row = 3;
            self.INFrXl.Layout.Column = 1;
            self.INFrXl.Text = 'X';

            % Create RealPartialImportX
            self.RealPartialImportX = uispinner(self.RealPartialImportGrid);
            self.RealPartialImportX.RoundFractionalValues = 'on';
            self.RealPartialImportX.ValueDisplayFormat = '%.0f';
            self.RealPartialImportX.ValueChangedFcn = createCallbackFcn(self, @import_box_input, true);
            self.RealPartialImportX.Tag = 'Import Real';
            self.RealPartialImportX.Enable = 'off';
            self.RealPartialImportX.Tooltip = {'Total frames after sampling on X (3rd dimension of image stack)'};
            self.RealPartialImportX.Layout.Row = 3;
            self.RealPartialImportX.Layout.Column = 2;
            self.RealPartialImportX.Value = 1;

            % Create INFrYl
            self.INFrYl = uilabel(self.RealPartialImportGrid);
            self.INFrYl.HorizontalAlignment = 'right';
            self.INFrYl.Enable = 'off';
            self.INFrYl.Layout.Row = 3;
            self.INFrYl.Layout.Column = 3;
            self.INFrYl.Text = 'Y';

            % Create RealPartialImportY
            self.RealPartialImportY = uispinner(self.RealPartialImportGrid);
            self.RealPartialImportY.RoundFractionalValues = 'on';
            self.RealPartialImportY.ValueDisplayFormat = '%.0f';
            self.RealPartialImportY.ValueChangedFcn = createCallbackFcn(self, @import_box_input, true);
            self.RealPartialImportY.Tag = 'Import Real';
            self.RealPartialImportY.Enable = 'off';
            self.RealPartialImportY.Tooltip = {'Total frames after sampling on Y (4th dimension of image stack)'};
            self.RealPartialImportY.Layout.Row = 3;
            self.RealPartialImportY.Layout.Column = 4;
            self.RealPartialImportY.Value = 1;

            % Create ImportSummaryLabel
            self.ImportSummaryLabel = uilabel(self.ImportOptionsGrid);
            self.ImportSummaryLabel.HorizontalAlignment = 'center';
            self.ImportSummaryLabel.VerticalAlignment = 'bottom';
            self.ImportSummaryLabel.FontName = 'Arial';
            self.ImportSummaryLabel.FontWeight = 'bold';
            self.ImportSummaryLabel.Layout.Row = 4;
            self.ImportSummaryLabel.Layout.Column = [1 2];
            self.ImportSummaryLabel.Text = 'Import Summary';

            % Create ImportSummary
            self.ImportSummary = uitextarea(self.ImportOptionsGrid);
            self.ImportSummary.Editable = 'off';
            self.ImportSummary.FontName = 'Arial';
            self.ImportSummary.Layout.Row = 5;
            self.ImportSummary.Layout.Column = [1 2];

            % Create ImportButtonGrid
            self.ImportButtonGrid = uigridlayout(self.ImportGrid);
            self.ImportButtonGrid.ColumnWidth = {'1x', '1x', '1x'};
            self.ImportButtonGrid.RowHeight = {24};
            self.ImportButtonGrid.ColumnSpacing = 4;
            self.ImportButtonGrid.RowSpacing = 4;
            self.ImportButtonGrid.Padding = [0 0 0 0];
            self.ImportButtonGrid.Layout.Row = 3;
            self.ImportButtonGrid.Layout.Column = 2;

            % Create ImportData
            self.ImportData = uibutton(self.ImportButtonGrid, 'push');
            self.ImportData.ButtonPushedFcn = createCallbackFcn(self, @import_callbacks, true);
            self.ImportData.FontName = 'Arial';
            self.ImportData.FontWeight = 'bold';
            self.ImportData.Layout.Row = 1;
            self.ImportData.Layout.Column = 1;
            self.ImportData.Text = 'Import Data';

            % Create SwapDataset
            self.SwapDataset = uicheckbox(self.ImportButtonGrid);
            self.SwapDataset.ValueChangedFcn = createCallbackFcn(self, @import_box_input, true);
            self.SwapDataset.Tooltip = {'Keep all current parameters/alignments/setups, and swap the already-imported dataset with another with exact (import) dimensions/datatype'};
            self.SwapDataset.Text = 'Swap Dataset';
            self.SwapDataset.Layout.Row = 1;
            self.SwapDataset.Layout.Column = 2;

            % Create CancelImport
            self.CancelImport = uibutton(self.ImportButtonGrid, 'push');
            self.CancelImport.ButtonPushedFcn = createCallbackFcn(self, @import_callbacks, true);
            self.CancelImport.FontName = 'Arial';
            self.CancelImport.FontWeight = 'bold';
            self.CancelImport.Layout.Row = 1;
            self.CancelImport.Layout.Column = 3;
            self.CancelImport.Text = 'Cancel';

            % Create SettingsPanel
            self.SettingsPanel = uipanel(self.Quant4D_Fig);
            self.SettingsPanel.AutoResizeChildren = 'off';
            self.SettingsPanel.BorderType = 'none';
            self.SettingsPanel.TitlePosition = 'centertop';
            self.SettingsPanel.FontWeight = 'bold';
            self.SettingsPanel.Position = [280 1 260 470];

            % Create SettingsGrid
            self.SettingsGrid = uigridlayout(self.SettingsPanel);
            self.SettingsGrid.ColumnWidth = {'1x'};
            self.SettingsGrid.RowHeight = {'1x'};
            self.SettingsGrid.ColumnSpacing = 4;
            self.SettingsGrid.RowSpacing = 4;
            self.SettingsGrid.Padding = [0 0 0 0];

            % Create SettingsTabGroup
            self.SettingsTabGroup = uitabgroup(self.SettingsGrid);
            self.SettingsTabGroup.AutoResizeChildren = 'off';
            self.SettingsTabGroup.Layout.Row = 1;
            self.SettingsTabGroup.Layout.Column = 1;

            % Create DisplayTab
            self.DisplayTab = uitab(self.SettingsTabGroup);
            self.DisplayTab.Title = 'Display';

            % Create DisplayGrid
            self.DisplayGrid = uigridlayout(self.DisplayTab);
            self.DisplayGrid.ColumnWidth = {'1x'};
            self.DisplayGrid.RowHeight = {'fit', 46, '1x', 'fit'};
            self.DisplayGrid.ColumnSpacing = 4;
            self.DisplayGrid.RowSpacing = 4;
            self.DisplayGrid.Padding = [4 4 4 4];

            % Create DisplayDropDownGrid
            self.DisplayDropDownGrid = uigridlayout(self.DisplayGrid);
            self.DisplayDropDownGrid.ColumnWidth = {24, 'fit', '1x', 24};
            self.DisplayDropDownGrid.RowHeight = {24, 24};
            self.DisplayDropDownGrid.ColumnSpacing = 4;
            self.DisplayDropDownGrid.RowSpacing = 4;
            self.DisplayDropDownGrid.Padding = [0 0 0 0];
            self.DisplayDropDownGrid.Layout.Row = 1;
            self.DisplayDropDownGrid.Layout.Column = 1;

            % Create ShowImageWindow
            self.ShowImageWindow = uibutton(self.DisplayDropDownGrid, 'push');
            self.ShowImageWindow.ButtonPushedFcn = createCallbackFcn(self, @show_window, true);
            self.ShowImageWindow.Icon = 'frontWindow.png';
            self.ShowImageWindow.FontWeight = 'bold';
            self.ShowImageWindow.Tooltip = {'Bring selected image to front'};
            self.ShowImageWindow.Layout.Row = 1;
            self.ShowImageWindow.Layout.Column = 1;
            self.ShowImageWindow.Text = '';

            % Create ImageLabel
            self.ImageLabel = uilabel(self.DisplayDropDownGrid);
            self.ImageLabel.HorizontalAlignment = 'right';
            self.ImageLabel.FontName = 'Arial';
            self.ImageLabel.FontWeight = 'bold';
            self.ImageLabel.Layout.Row = 1;
            self.ImageLabel.Layout.Column = 2;
            self.ImageLabel.Text = 'Image';

            % Create DisplayImage
            self.DisplayImage = uidropdown(self.DisplayDropDownGrid);
            self.DisplayImage.Items = {};
            self.DisplayImage.ValueChangedFcn = createCallbackFcn(self, @display_callbacks, true);
            self.DisplayImage.FontName = 'Arial';
            self.DisplayImage.Layout.Row = 1;
            self.DisplayImage.Layout.Column = 3;
            self.DisplayImage.Value = {};

            % Create DisplayLock
            self.DisplayLock = uibutton(self.DisplayDropDownGrid, 'state');
            self.DisplayLock.ValueChangedFcn = createCallbackFcn(self, @display_callbacks, true);
            self.DisplayLock.Tooltip = {'Stop changing the selected image when clicking on a new image'};
            self.DisplayLock.Icon = 'link.png';
            self.DisplayLock.Text = '';
            self.DisplayLock.Layout.Row = 1;
            self.DisplayLock.Layout.Column = 4;

            % Create ColormapLabel
            self.ColormapLabel = uilabel(self.DisplayDropDownGrid);
            self.ColormapLabel.HorizontalAlignment = 'right';
            self.ColormapLabel.Layout.Row = 2;
            self.ColormapLabel.Layout.Column = [1 2];
            self.ColormapLabel.Text = 'Colormap';

            % Create DispColorMap
            self.DispColorMap = uidropdown(self.DisplayDropDownGrid);
            self.DispColorMap.Items = {'gray', 'hsv', 'jet', 'parula', 'hot', 'cool', 'spring', 'summer', 'autumn', 'winter', 'bone', 'copper', 'pink'};
            self.DispColorMap.ValueChangedFcn = createCallbackFcn(self, @display_callbacks, true);
            self.DispColorMap.Layout.Row = 2;
            self.DispColorMap.Layout.Column = 3;
            self.DispColorMap.Value = 'gray';

            % Create DispColorMapInvert
            self.DispColorMapInvert = uibutton(self.DisplayDropDownGrid, 'state');
            self.DispColorMapInvert.ValueChangedFcn = createCallbackFcn(self, @display_callbacks, true);
            self.DispColorMapInvert.Tooltip = {'Invert colormap'};
            self.DispColorMapInvert.Icon = 'invertColors.png';
            self.DispColorMapInvert.Text = '';
            self.DispColorMapInvert.Layout.Row = 2;
            self.DispColorMapInvert.Layout.Column = 4;

            % Create ImageStatistics
            self.ImageStatistics = uitextarea(self.DisplayGrid);
            self.ImageStatistics.Editable = 'off';
            self.ImageStatistics.FontName = 'Monospaced';
            self.ImageStatistics.FontSize = 11;
            self.ImageStatistics.FontWeight = 'bold';
            self.ImageStatistics.Layout.Row = 2;
            self.ImageStatistics.Layout.Column = 1;

            % Create HistogramGrid
            self.HistogramGrid = uigridlayout(self.DisplayGrid);
            self.HistogramGrid.ColumnWidth = {'1x', 'fit', 6};
            self.HistogramGrid.RowHeight = {6, 'fit', '1x'};
            self.HistogramGrid.ColumnSpacing = 4;
            self.HistogramGrid.RowSpacing = 4;
            self.HistogramGrid.Padding = [0 0 0 0];
            self.HistogramGrid.Layout.Row = 3;
            self.HistogramGrid.Layout.Column = 1;

            % Create HistogramAxes
            self.HistogramAxes = uiaxes(self.HistogramGrid);
            self.HistogramAxes.Toolbar.Visible = 'off';
            self.HistogramAxes.XTick = [];
            self.HistogramAxes.YTick = [];
            self.HistogramAxes.ZTick = [];
            self.HistogramAxes.Box = 'on';
            self.HistogramAxes.NextPlot = 'add';
            self.HistogramAxes.Layout.Row = [1 3];
            self.HistogramAxes.Layout.Column = [1 3];

            % Create HistogramLog
            self.HistogramLog = uibutton(self.HistogramGrid, 'state');
            self.HistogramLog.ValueChangedFcn = createCallbackFcn(self, @display_callbacks, true);
            self.HistogramLog.Text = 'log';
            self.HistogramLog.FontName = 'Arial';
            self.HistogramLog.FontWeight = 'bold';
            self.HistogramLog.Layout.Row = 2;
            self.HistogramLog.Layout.Column = 2;

            % Create DispContrastsGrid
            self.DispContrastsGrid = uigridlayout(self.DisplayGrid);
            self.DispContrastsGrid.ColumnWidth = {24, '1x', 72};
            self.DispContrastsGrid.RowHeight = {24, 24, 24, 24};
            self.DispContrastsGrid.ColumnSpacing = 4;
            self.DispContrastsGrid.RowSpacing = 4;
            self.DispContrastsGrid.Padding = [0 0 0 0];
            self.DispContrastsGrid.Layout.Row = 4;
            self.DispContrastsGrid.Layout.Column = 1;

            % Create DisplayBrightnessReset
            self.DisplayBrightnessReset = uibutton(self.DispContrastsGrid, 'push');
            self.DisplayBrightnessReset.ButtonPushedFcn = createCallbackFcn(self, @display_callbacks, true);
            self.DisplayBrightnessReset.Icon = 'brightness.png';
            self.DisplayBrightnessReset.FontWeight = 'bold';
            self.DisplayBrightnessReset.Tooltip = {'Reset Brightness'};
            self.DisplayBrightnessReset.Layout.Row = 1;
            self.DisplayBrightnessReset.Layout.Column = 1;
            self.DisplayBrightnessReset.Text = '';

            % Create DisplayBrightness
            self.DisplayBrightness = uislider(self.DispContrastsGrid);
            self.DisplayBrightness.MajorTicks = [];
            self.DisplayBrightness.MajorTickLabels = {};
            self.DisplayBrightness.ValueChangedFcn = createCallbackFcn(self, @display_callbacks, true);
            self.DisplayBrightness.ValueChangingFcn = createCallbackFcn(self, @display_callbacks, true);
            self.DisplayBrightness.Layout.Row = 1;
            self.DisplayBrightness.Layout.Column = 2;
            self.DisplayBrightness.Value = 50;

            % Create DisplayBrightnessSpinner
            self.DisplayBrightnessSpinner = uispinner(self.DispContrastsGrid);
            self.DisplayBrightnessSpinner.ValueChangingFcn = createCallbackFcn(self, @display_callbacks, true);
            self.DisplayBrightnessSpinner.Limits = [0 100];
            self.DisplayBrightnessSpinner.ValueDisplayFormat = '%.4g%%';
            self.DisplayBrightnessSpinner.ValueChangedFcn = createCallbackFcn(self, @display_callbacks, true);
            self.DisplayBrightnessSpinner.Layout.Row = 1;
            self.DisplayBrightnessSpinner.Layout.Column = 3;
            self.DisplayBrightnessSpinner.Value = 50;

            % Create DisplayContrastReset
            self.DisplayContrastReset = uibutton(self.DispContrastsGrid, 'push');
            self.DisplayContrastReset.ButtonPushedFcn = createCallbackFcn(self, @display_callbacks, true);
            self.DisplayContrastReset.Icon = 'contrast.png';
            self.DisplayContrastReset.FontWeight = 'bold';
            self.DisplayContrastReset.Tooltip = {'Reset Contrast'};
            self.DisplayContrastReset.Layout.Row = 2;
            self.DisplayContrastReset.Layout.Column = 1;
            self.DisplayContrastReset.Text = '';

            % Create DisplayContrast
            self.DisplayContrast = uislider(self.DispContrastsGrid);
            self.DisplayContrast.MajorTicks = [];
            self.DisplayContrast.MajorTickLabels = {};
            self.DisplayContrast.ValueChangedFcn = createCallbackFcn(self, @display_callbacks, true);
            self.DisplayContrast.ValueChangingFcn = createCallbackFcn(self, @display_callbacks, true);
            self.DisplayContrast.Layout.Row = 2;
            self.DisplayContrast.Layout.Column = 2;
            self.DisplayContrast.Value = 50;

            % Create DisplayContrastSpinner
            self.DisplayContrastSpinner = uispinner(self.DispContrastsGrid);
            self.DisplayContrastSpinner.ValueChangingFcn = createCallbackFcn(self, @display_callbacks, true);
            self.DisplayContrastSpinner.Limits = [0 100];
            self.DisplayContrastSpinner.ValueDisplayFormat = '%.4g%%';
            self.DisplayContrastSpinner.ValueChangedFcn = createCallbackFcn(self, @display_callbacks, true);
            self.DisplayContrastSpinner.Layout.Row = 2;
            self.DisplayContrastSpinner.Layout.Column = 3;
            self.DisplayContrastSpinner.Value = 50;

            % Create DisplayGammaReset
            self.DisplayGammaReset = uibutton(self.DispContrastsGrid, 'push');
            self.DisplayGammaReset.ButtonPushedFcn = createCallbackFcn(self, @display_callbacks, true);
            self.DisplayGammaReset.Icon = 'gamma.png';
            self.DisplayGammaReset.FontWeight = 'bold';
            self.DisplayGammaReset.Tooltip = {'Reset Gamma'};
            self.DisplayGammaReset.Layout.Row = 3;
            self.DisplayGammaReset.Layout.Column = 1;
            self.DisplayGammaReset.Text = '';

            % Create DisplayGamma
            self.DisplayGamma = uislider(self.DispContrastsGrid);
            self.DisplayGamma.Limits = [0 2];
            self.DisplayGamma.MajorTicks = [];
            self.DisplayGamma.MajorTickLabels = {};
            self.DisplayGamma.ValueChangedFcn = createCallbackFcn(self, @display_callbacks, true);
            self.DisplayGamma.ValueChangingFcn = createCallbackFcn(self, @display_callbacks, true);
            self.DisplayGamma.Layout.Row = 3;
            self.DisplayGamma.Layout.Column = 2;
            self.DisplayGamma.Value = 1;

            % Create DisplayGammaSpinner
            self.DisplayGammaSpinner = uispinner(self.DispContrastsGrid);
            self.DisplayGammaSpinner.Step = 0.01;
            self.DisplayGammaSpinner.ValueChangingFcn = createCallbackFcn(self, @display_callbacks, true);
            self.DisplayGammaSpinner.Limits = [0 2];
            self.DisplayGammaSpinner.ValueDisplayFormat = '%.5g';
            self.DisplayGammaSpinner.ValueChangedFcn = createCallbackFcn(self, @display_callbacks, true);
            self.DisplayGammaSpinner.Layout.Row = 3;
            self.DisplayGammaSpinner.Layout.Column = 3;
            self.DisplayGammaSpinner.Value = 1;

            % Create ShowMaskWindow
            self.ShowMaskWindow = uibutton(self.DispContrastsGrid, 'push');
            self.ShowMaskWindow.ButtonPushedFcn = createCallbackFcn(self, @show_window, true);
            self.ShowMaskWindow.Icon = 'Aperture.png';
            self.ShowMaskWindow.Tooltip = {'Show Mask Image'};
            self.ShowMaskWindow.Layout.Row = 4;
            self.ShowMaskWindow.Layout.Column = 1;
            self.ShowMaskWindow.Text = '';

            % Create DisplayMaskOpacitySlider
            self.DisplayMaskOpacitySlider = uislider(self.DispContrastsGrid);
            self.DisplayMaskOpacitySlider.MajorTicks = [];
            self.DisplayMaskOpacitySlider.ValueChangedFcn = createCallbackFcn(self, @display_callbacks, true);
            self.DisplayMaskOpacitySlider.ValueChangingFcn = createCallbackFcn(self, @display_callbacks, true);
            self.DisplayMaskOpacitySlider.Tooltip = {'Mask opacity displayed on pattern'};
            self.DisplayMaskOpacitySlider.Layout.Row = 4;
            self.DisplayMaskOpacitySlider.Layout.Column = 2;

            % Create DisplayMaskOpacitySpinner
            self.DisplayMaskOpacitySpinner = uispinner(self.DispContrastsGrid);
            self.DisplayMaskOpacitySpinner.ValueChangingFcn = createCallbackFcn(self, @display_callbacks, true);
            self.DisplayMaskOpacitySpinner.Limits = [0 100];
            self.DisplayMaskOpacitySpinner.ValueDisplayFormat = '%.4g%%';
            self.DisplayMaskOpacitySpinner.ValueChangedFcn = createCallbackFcn(self, @display_callbacks, true);
            self.DisplayMaskOpacitySpinner.Layout.Row = 4;
            self.DisplayMaskOpacitySpinner.Layout.Column = 3;

            % Create WindowsTab
            self.WindowsTab = uitab(self.SettingsTabGroup);
            self.WindowsTab.Title = 'Windows';

            % Create WindowsTabGrid
            self.WindowsTabGrid = uigridlayout(self.WindowsTab);
            self.WindowsTabGrid.ColumnWidth = {'1x'};
            self.WindowsTabGrid.RowHeight = {'2.5x', '1x', 108};
            self.WindowsTabGrid.ColumnSpacing = 4;
            self.WindowsTabGrid.RowSpacing = 4;
            self.WindowsTabGrid.Padding = [4 4 4 4];

            % Create BandpassFilterPanel
            self.BandpassFilterPanel = uipanel(self.WindowsTabGrid);
            self.BandpassFilterPanel.AutoResizeChildren = 'off';
            self.BandpassFilterPanel.Tooltip = {'Apply a bandpass, lowpass, or highpass filter. Units are in pixels applied in fourier space.'};
            self.BandpassFilterPanel.BorderType = 'none';
            self.BandpassFilterPanel.TitlePosition = 'centertop';
            self.BandpassFilterPanel.Title = 'iCoM / dCoM Bandpass Filter';
            self.BandpassFilterPanel.Layout.Row = 2;
            self.BandpassFilterPanel.Layout.Column = 1;
            self.BandpassFilterPanel.FontWeight = 'bold';

            % Create BandpassFilterGrid
            self.BandpassFilterGrid = uigridlayout(self.BandpassFilterPanel);
            self.BandpassFilterGrid.RowHeight = {'fit', 24};
            self.BandpassFilterGrid.ColumnSpacing = 4;
            self.BandpassFilterGrid.RowSpacing = 4;
            self.BandpassFilterGrid.Padding = [0 0 0 4];

            % Create BandpassFilter
            self.BandpassFilter = uislider(self.BandpassFilterGrid, 'range');
            self.BandpassFilter.MajorTicks = [];
            self.BandpassFilter.ValueChangedFcn = createCallbackFcn(self, @first_moment, true);
            self.BandpassFilter.ValueChangingFcn = createCallbackFcn(self, @first_moment, true);
            self.BandpassFilter.Layout.Row = 1;
            self.BandpassFilter.Layout.Column = [1 2];

            % Create BandpassFilterHigh
            self.BandpassFilterHigh = uispinner(self.BandpassFilterGrid);
            self.BandpassFilterHigh.ValueChangingFcn = createCallbackFcn(self, @first_moment, true);
            self.BandpassFilterHigh.Limits = [0 100];
            self.BandpassFilterHigh.RoundFractionalValues = 'on';
            self.BandpassFilterHigh.ValueDisplayFormat = '%d px';
            self.BandpassFilterHigh.ValueChangedFcn = createCallbackFcn(self, @first_moment, true);
            self.BandpassFilterHigh.Layout.Row = 2;
            self.BandpassFilterHigh.Layout.Column = 2;
            self.BandpassFilterHigh.Value = 100;

            % Create BandpassFilterLow
            self.BandpassFilterLow = uispinner(self.BandpassFilterGrid);
            self.BandpassFilterLow.ValueChangingFcn = createCallbackFcn(self, @first_moment, true);
            self.BandpassFilterLow.Limits = [0 100];
            self.BandpassFilterLow.RoundFractionalValues = 'on';
            self.BandpassFilterLow.ValueDisplayFormat = '%d px';
            self.BandpassFilterLow.ValueChangedFcn = createCallbackFcn(self, @first_moment, true);
            self.BandpassFilterLow.Layout.Row = 2;
            self.BandpassFilterLow.Layout.Column = 1;

            % Create ShowImageWindowsPanel
            self.ShowImageWindowsPanel = uipanel(self.WindowsTabGrid);
            self.ShowImageWindowsPanel.AutoResizeChildren = 'off';
            self.ShowImageWindowsPanel.BorderType = 'none';
            self.ShowImageWindowsPanel.TitlePosition = 'centertop';
            self.ShowImageWindowsPanel.Title = 'Show Image Windows';
            self.ShowImageWindowsPanel.Layout.Row = 1;
            self.ShowImageWindowsPanel.Layout.Column = 1;
            self.ShowImageWindowsPanel.FontName = 'Arial';
            self.ShowImageWindowsPanel.FontWeight = 'bold';

            % Create ShowImageWindowsGrid
            self.ShowImageWindowsGrid = uigridlayout(self.ShowImageWindowsPanel);
            self.ShowImageWindowsGrid.RowHeight = {24, 24, 24, 24, 24, 24, 'fit'};
            self.ShowImageWindowsGrid.ColumnSpacing = 0;
            self.ShowImageWindowsGrid.RowSpacing = 0;
            self.ShowImageWindowsGrid.Padding = [0 0 0 4];

            % Create ShowDiffractionWindow
            self.ShowDiffractionWindow = uibutton(self.ShowImageWindowsGrid, 'push');
            self.ShowDiffractionWindow.ButtonPushedFcn = createCallbackFcn(self, @show_window, true);
            self.ShowDiffractionWindow.Tag = 'Diffraction';
            self.ShowDiffractionWindow.Tooltip = {'Show Diffraction Pattern'};
            self.ShowDiffractionWindow.Layout.Row = 1;
            self.ShowDiffractionWindow.Layout.Column = 1;
            self.ShowDiffractionWindow.Text = 'Diffraction';

            % Create ShowDiffractionMaskWindow2
            self.ShowDiffractionMaskWindow2 = uibutton(self.ShowImageWindowsGrid, 'push');
            self.ShowDiffractionMaskWindow2.ButtonPushedFcn = createCallbackFcn(self, @show_window, true);
            self.ShowDiffractionMaskWindow2.Tag = 'DiffractionMask';
            self.ShowDiffractionMaskWindow2.Icon = 'Aperture.png';
            self.ShowDiffractionMaskWindow2.Tooltip = {'Show Diffraction Mask'};
            self.ShowDiffractionMaskWindow2.Layout.Row = 1;
            self.ShowDiffractionMaskWindow2.Layout.Column = 2;
            self.ShowDiffractionMaskWindow2.Text = 'Diff. Mask';

            % Create ShowRealWindow
            self.ShowRealWindow = uibutton(self.ShowImageWindowsGrid, 'push');
            self.ShowRealWindow.ButtonPushedFcn = createCallbackFcn(self, @show_window, true);
            self.ShowRealWindow.Tag = 'Real';
            self.ShowRealWindow.Tooltip = {'Show Real-space Image'};
            self.ShowRealWindow.Layout.Row = 2;
            self.ShowRealWindow.Layout.Column = 1;
            self.ShowRealWindow.Text = 'BF/DF';

            % Create ShowRealMaskWindow2
            self.ShowRealMaskWindow2 = uibutton(self.ShowImageWindowsGrid, 'push');
            self.ShowRealMaskWindow2.ButtonPushedFcn = createCallbackFcn(self, @show_window, true);
            self.ShowRealMaskWindow2.Tag = 'RealMask';
            self.ShowRealMaskWindow2.Icon = 'Aperture.png';
            self.ShowRealMaskWindow2.FontSize = 10;
            self.ShowRealMaskWindow2.Tooltip = {'Show Real-space Mask'};
            self.ShowRealMaskWindow2.Layout.Row = 2;
            self.ShowRealMaskWindow2.Layout.Column = 2;
            self.ShowRealMaskWindow2.Text = 'BF/DF Mask';

            % Create ShowColorWheelWindow2
            self.ShowColorWheelWindow2 = uibutton(self.ShowImageWindowsGrid, 'push');
            self.ShowColorWheelWindow2.ButtonPushedFcn = createCallbackFcn(self, @show_window, true);
            self.ShowColorWheelWindow2.Tag = 'ColorWheel';
            self.ShowColorWheelWindow2.Icon = 'colorwheel.png';
            self.ShowColorWheelWindow2.Tooltip = {'Show Color Wheel for Phase Vector Field Direction'};
            self.ShowColorWheelWindow2.Layout.Row = 5;
            self.ShowColorWheelWindow2.Layout.Column = 1;
            self.ShowColorWheelWindow2.Text = 'φ';

            % Create ShowCoMPhaseMagnitudeWindow
            self.ShowCoMPhaseMagnitudeWindow = uibutton(self.ShowImageWindowsGrid, 'push');
            self.ShowCoMPhaseMagnitudeWindow.ButtonPushedFcn = createCallbackFcn(self, @show_window, true);
            self.ShowCoMPhaseMagnitudeWindow.Tag = 'CoMPhMag';
            self.ShowCoMPhaseMagnitudeWindow.Tooltip = {'Show CoM/DPC Phase (Magnitude-shaded) Image'};
            self.ShowCoMPhaseMagnitudeWindow.Layout.Row = 5;
            self.ShowCoMPhaseMagnitudeWindow.Layout.Column = 2;
            self.ShowCoMPhaseMagnitudeWindow.Text = '|CoM| φ';

            % Create ShowCoMPhaseWindow
            self.ShowCoMPhaseWindow = uibutton(self.ShowImageWindowsGrid, 'push');
            self.ShowCoMPhaseWindow.ButtonPushedFcn = createCallbackFcn(self, @show_window, true);
            self.ShowCoMPhaseWindow.Tag = 'CoMPh';
            self.ShowCoMPhaseWindow.Tooltip = {'Show CoM/DPC Phase Image'};
            self.ShowCoMPhaseWindow.Layout.Row = 4;
            self.ShowCoMPhaseWindow.Layout.Column = 2;
            self.ShowCoMPhaseWindow.Text = 'CoM φ';

            % Create ShowCoMMagnitudeWindow
            self.ShowCoMMagnitudeWindow = uibutton(self.ShowImageWindowsGrid, 'push');
            self.ShowCoMMagnitudeWindow.ButtonPushedFcn = createCallbackFcn(self, @show_window, true);
            self.ShowCoMMagnitudeWindow.Tag = 'CoMMag';
            self.ShowCoMMagnitudeWindow.Tooltip = {'Show CoM/DPC Magnitude Image'};
            self.ShowCoMMagnitudeWindow.Layout.Row = 4;
            self.ShowCoMMagnitudeWindow.Layout.Column = 1;
            self.ShowCoMMagnitudeWindow.Text = '|CoM|';

            % Create ShowCoMXWindow
            self.ShowCoMXWindow = uibutton(self.ShowImageWindowsGrid, 'push');
            self.ShowCoMXWindow.ButtonPushedFcn = createCallbackFcn(self, @show_window, true);
            self.ShowCoMXWindow.Tag = 'CoMX';
            self.ShowCoMXWindow.Tooltip = {'Show CoM/DPC X Image'};
            self.ShowCoMXWindow.Layout.Row = 3;
            self.ShowCoMXWindow.Layout.Column = 1;
            self.ShowCoMXWindow.Text = 'CoM X';

            % Create ShowCoMYWindow
            self.ShowCoMYWindow = uibutton(self.ShowImageWindowsGrid, 'push');
            self.ShowCoMYWindow.ButtonPushedFcn = createCallbackFcn(self, @show_window, true);
            self.ShowCoMYWindow.Tag = 'CoMY';
            self.ShowCoMYWindow.Tooltip = {'Show CoM/DPC Y Image'};
            self.ShowCoMYWindow.Layout.Row = 3;
            self.ShowCoMYWindow.Layout.Column = 2;
            self.ShowCoMYWindow.Text = 'CoM Y';

            % Create ShowdCoMWindow
            self.ShowdCoMWindow = uibutton(self.ShowImageWindowsGrid, 'push');
            self.ShowdCoMWindow.ButtonPushedFcn = createCallbackFcn(self, @show_window, true);
            self.ShowdCoMWindow.Tag = 'dCoM';
            self.ShowdCoMWindow.Tooltip = {'Show dCoM/dDPC Image'};
            self.ShowdCoMWindow.Layout.Row = 6;
            self.ShowdCoMWindow.Layout.Column = 1;
            self.ShowdCoMWindow.Text = 'dCoM';

            % Create ShowiCoMWindow
            self.ShowiCoMWindow = uibutton(self.ShowImageWindowsGrid, 'push');
            self.ShowiCoMWindow.ButtonPushedFcn = createCallbackFcn(self, @show_window, true);
            self.ShowiCoMWindow.Tag = 'iCoM';
            self.ShowiCoMWindow.Tooltip = {'Show iCoM/iDPC Image'};
            self.ShowiCoMWindow.Layout.Row = 6;
            self.ShowiCoMWindow.Layout.Column = 2;
            self.ShowiCoMWindow.Text = 'iCoM';

            % Create VectorSamplingGrid
            self.VectorSamplingGrid = uigridlayout(self.ShowImageWindowsGrid);
            self.VectorSamplingGrid.ColumnWidth = {'fit', '1x', 24, 24};
            self.VectorSamplingGrid.RowHeight = {24};
            self.VectorSamplingGrid.ColumnSpacing = 4;
            self.VectorSamplingGrid.RowSpacing = 4;
            self.VectorSamplingGrid.Padding = [4 4 4 4];
            self.VectorSamplingGrid.Layout.Row = 7;
            self.VectorSamplingGrid.Layout.Column = [1 2];

            % Create DispVecFieldLabel
            self.DispVecFieldLabel = uilabel(self.VectorSamplingGrid);
            self.DispVecFieldLabel.HorizontalAlignment = 'right';
            self.DispVecFieldLabel.Layout.Row = 1;
            self.DispVecFieldLabel.Layout.Column = 1;
            self.DispVecFieldLabel.Text = 'Vector Sampling:';

            % Create DisplayVectorField
            self.DisplayVectorField = uidropdown(self.VectorSamplingGrid);
            self.DisplayVectorField.Items = {'None', '1:1', '1:2', '1:4', '1:8', '1:16'};
            self.DisplayVectorField.ItemsData = [0 1 2 4 8 16];
            self.DisplayVectorField.ValueChangedFcn = createCallbackFcn(self, @display_callbacks, true);
            self.DisplayVectorField.Tooltip = {'Plot vector field on the current selected Real-space image'};
            self.DisplayVectorField.Layout.Row = 1;
            self.DisplayVectorField.Layout.Column = 2;
            self.DisplayVectorField.Value = 0;

            % Create DisplayVectorColor
            self.DisplayVectorColor = uibutton(self.VectorSamplingGrid, 'push');
            self.DisplayVectorColor.ButtonPushedFcn = createCallbackFcn(self, @display_callbacks, true);
            self.DisplayVectorColor.Icon = 'colorPicker.png';
            self.DisplayVectorColor.Tooltip = {'Change Vector Field color'};
            self.DisplayVectorColor.Layout.Row = 1;
            self.DisplayVectorColor.Layout.Column = 3;
            self.DisplayVectorColor.Text = '';

            % Create ShowColorWheelWindow
            self.ShowColorWheelWindow = uibutton(self.VectorSamplingGrid, 'push');
            self.ShowColorWheelWindow.ButtonPushedFcn = createCallbackFcn(self, @show_window, true);
            self.ShowColorWheelWindow.Tag = 'ColorWheel';
            self.ShowColorWheelWindow.Icon = 'colorwheel.png';
            self.ShowColorWheelWindow.Tooltip = {'Show Color Wheel for Phase Vector Field Direction'};
            self.ShowColorWheelWindow.Layout.Row = 1;
            self.ShowColorWheelWindow.Layout.Column = 4;
            self.ShowColorWheelWindow.Text = '';

            % Create WindowResizePanel
            self.WindowResizePanel = uipanel(self.WindowsTabGrid);
            self.WindowResizePanel.BorderType = 'none';
            self.WindowResizePanel.TitlePosition = 'centertop';
            self.WindowResizePanel.Title = 'Window size and orientation';
            self.WindowResizePanel.Layout.Row = 3;
            self.WindowResizePanel.Layout.Column = 1;
            self.WindowResizePanel.FontWeight = 'bold';

            % Create WindowResizeGrid
            self.WindowResizeGrid = uigridlayout(self.WindowResizePanel);
            self.WindowResizeGrid.ColumnWidth = {'1x'};
            self.WindowResizeGrid.RowHeight = {'1x'};
            self.WindowResizeGrid.ColumnSpacing = 0;
            self.WindowResizeGrid.RowSpacing = 0;
            self.WindowResizeGrid.Padding = [0 0 0 0];

            % Create WindowResizeTabGroup
            self.WindowResizeTabGroup = uitabgroup(self.WindowResizeGrid);
            self.WindowResizeTabGroup.Layout.Row = 1;
            self.WindowResizeTabGroup.Layout.Column = 1;

            % Create DiffractionTab
            self.DiffractionTab = uitab(self.WindowResizeTabGroup);
            self.DiffractionTab.Title = 'Diffraction';

            % Create DiffractionTabGrid
            self.DiffractionTabGrid = uigridlayout(self.DiffractionTab);
            self.DiffractionTabGrid.ColumnWidth = {'1x'};
            self.DiffractionTabGrid.RowHeight = {'1x'};
            self.DiffractionTabGrid.ColumnSpacing = 4;
            self.DiffractionTabGrid.RowSpacing = 4;
            self.DiffractionTabGrid.Padding = [4 4 4 4];

            % Create DiffractionWindowPanel
            self.DiffractionWindowPanel = uipanel(self.DiffractionTabGrid);
            self.DiffractionWindowPanel.AutoResizeChildren = 'off';
            self.DiffractionWindowPanel.BorderType = 'none';
            self.DiffractionWindowPanel.TitlePosition = 'centertop';
            self.DiffractionWindowPanel.Layout.Row = 1;
            self.DiffractionWindowPanel.Layout.Column = 1;
            self.DiffractionWindowPanel.FontName = 'Arial';
            self.DiffractionWindowPanel.FontWeight = 'bold';

            % Create DiffractionWindowGrid
            self.DiffractionWindowGrid = uigridlayout(self.DiffractionWindowPanel);
            self.DiffractionWindowGrid.ColumnWidth = {12, 60, 12, 60, '1x', 'fit', 'fit'};
            self.DiffractionWindowGrid.RowHeight = {24, 24};
            self.DiffractionWindowGrid.ColumnSpacing = 4;
            self.DiffractionWindowGrid.RowSpacing = 4;
            self.DiffractionWindowGrid.Padding = [0 0 0 4];

            % Create DiffractionAxesGrid
            self.DiffractionAxesGrid = uigridlayout(self.DiffractionWindowGrid);
            self.DiffractionAxesGrid.ColumnWidth = {'1x', 24, 24, 24, '1x', 20, 'fit', '1x'};
            self.DiffractionAxesGrid.RowHeight = {24};
            self.DiffractionAxesGrid.ColumnSpacing = 4;
            self.DiffractionAxesGrid.RowSpacing = 4;
            self.DiffractionAxesGrid.Padding = [0 0 0 0];
            self.DiffractionAxesGrid.Layout.Row = 1;
            self.DiffractionAxesGrid.Layout.Column = [1 7];

            % Create ShowDiffractionAxes
            self.ShowDiffractionAxes = uibutton(self.DiffractionAxesGrid, 'state');
            self.ShowDiffractionAxes.ValueChangedFcn = createCallbackFcn(self, @axis_direction_callbacks, true);
            self.ShowDiffractionAxes.Tag = 'Diffraction';
            self.ShowDiffractionAxes.Tooltip = {'Show Axis Directions on Images'};
            self.ShowDiffractionAxes.Icon = 'axes.png';
            self.ShowDiffractionAxes.Text = '';
            self.ShowDiffractionAxes.Layout.Row = 1;
            self.ShowDiffractionAxes.Layout.Column = 2;
            self.ShowDiffractionAxes.Value = true;

            % Create ReverseDiffractionX
            self.ReverseDiffractionX = uibutton(self.DiffractionAxesGrid, 'state');
            self.ReverseDiffractionX.ValueChangedFcn = createCallbackFcn(self, @axis_direction_callbacks, true);
            self.ReverseDiffractionX.Tag = 'Diffraction';
            self.ReverseDiffractionX.Tooltip = {'Reverse X-axis Direction'};
            self.ReverseDiffractionX.Icon = 'axis-x.png';
            self.ReverseDiffractionX.Text = '';
            self.ReverseDiffractionX.FontWeight = 'bold';
            self.ReverseDiffractionX.Layout.Row = 1;
            self.ReverseDiffractionX.Layout.Column = 3;

            % Create ReverseDiffractionY
            self.ReverseDiffractionY = uibutton(self.DiffractionAxesGrid, 'state');
            self.ReverseDiffractionY.ValueChangedFcn = createCallbackFcn(self, @axis_direction_callbacks, true);
            self.ReverseDiffractionY.Tag = 'Diffraction';
            self.ReverseDiffractionY.Tooltip = {'Reverse Y-axis Direction'};
            self.ReverseDiffractionY.Icon = 'axis-y.png';
            self.ReverseDiffractionY.Text = '';
            self.ReverseDiffractionY.FontWeight = 'bold';
            self.ReverseDiffractionY.Layout.Row = 1;
            self.ReverseDiffractionY.Layout.Column = 4;
            self.ReverseDiffractionY.Value = true;

            % Create RotateDiffractionIcon
            self.RotateDiffractionIcon = uiimage(self.DiffractionAxesGrid);
            self.RotateDiffractionIcon.Tooltip = {'Rotate View'};
            self.RotateDiffractionIcon.Layout.Row = 1;
            self.RotateDiffractionIcon.Layout.Column = 6;
            self.RotateDiffractionIcon.ImageSource = 'right_rotate.png';

            % Create RotateDiffraction
            self.RotateDiffraction = uidropdown(self.DiffractionAxesGrid);
            self.RotateDiffraction.Items = {'0°', '90°', '180°', '-90°'};
            self.RotateDiffraction.ItemsData = [0 90 180 -90];
            self.RotateDiffraction.ValueChangedFcn = createCallbackFcn(self, @axis_direction_callbacks, true);
            self.RotateDiffraction.Tag = 'Diffraction';
            self.RotateDiffraction.Tooltip = {'Rotate Image Display'};
            self.RotateDiffraction.Layout.Row = 1;
            self.RotateDiffraction.Layout.Column = 7;
            self.RotateDiffraction.Value = 0;

            % Create WEditFieldLabel
            self.WEditFieldLabel = uilabel(self.DiffractionWindowGrid);
            self.WEditFieldLabel.HorizontalAlignment = 'right';
            self.WEditFieldLabel.Layout.Row = 2;
            self.WEditFieldLabel.Layout.Column = 1;
            self.WEditFieldLabel.Text = 'W';

            % Create SetDiffractionWindowWidth
            self.SetDiffractionWindowWidth = uieditfield(self.DiffractionWindowGrid, 'numeric');
            self.SetDiffractionWindowWidth.Limits = [1 Inf];
            self.SetDiffractionWindowWidth.RoundFractionalValues = 'on';
            self.SetDiffractionWindowWidth.ValueDisplayFormat = '%.0f';
            self.SetDiffractionWindowWidth.ValueChangedFcn = createCallbackFcn(self, @resize_window, true);
            self.SetDiffractionWindowWidth.Tag = 'Diffraction';
            self.SetDiffractionWindowWidth.Layout.Row = 2;
            self.SetDiffractionWindowWidth.Layout.Column = 2;
            self.SetDiffractionWindowWidth.Value = 400;

            % Create HEditFieldLabel
            self.HEditFieldLabel = uilabel(self.DiffractionWindowGrid);
            self.HEditFieldLabel.HorizontalAlignment = 'right';
            self.HEditFieldLabel.Layout.Row = 2;
            self.HEditFieldLabel.Layout.Column = 3;
            self.HEditFieldLabel.Text = 'H';

            % Create SetDiffractionWindowHeight
            self.SetDiffractionWindowHeight = uieditfield(self.DiffractionWindowGrid, 'numeric');
            self.SetDiffractionWindowHeight.Limits = [1 Inf];
            self.SetDiffractionWindowHeight.RoundFractionalValues = 'on';
            self.SetDiffractionWindowHeight.ValueDisplayFormat = '%.0f';
            self.SetDiffractionWindowHeight.ValueChangedFcn = createCallbackFcn(self, @resize_window, true);
            self.SetDiffractionWindowHeight.Tag = 'Diffraction';
            self.SetDiffractionWindowHeight.Layout.Row = 2;
            self.SetDiffractionWindowHeight.Layout.Column = 4;
            self.SetDiffractionWindowHeight.Value = 400;

            % Create SetDiffractionWindow
            self.SetDiffractionWindow = uibutton(self.DiffractionWindowGrid, 'push');
            self.SetDiffractionWindow.ButtonPushedFcn = createCallbackFcn(self, @resize_window, true);
            self.SetDiffractionWindow.Tag = 'Diffraction';
            self.SetDiffractionWindow.Layout.Row = 2;
            self.SetDiffractionWindow.Layout.Column = 6;
            self.SetDiffractionWindow.Text = 'Set';

            % Create SetAllDiffractionWindows
            self.SetAllDiffractionWindows = uibutton(self.DiffractionWindowGrid, 'push');
            self.SetAllDiffractionWindows.ButtonPushedFcn = createCallbackFcn(self, @resize_window, true);
            self.SetAllDiffractionWindows.Tag = 'Diffraction';
            self.SetAllDiffractionWindows.Layout.Row = 2;
            self.SetAllDiffractionWindows.Layout.Column = 7;
            self.SetAllDiffractionWindows.Text = 'Set All';

            % Create RealspaceTab
            self.RealspaceTab = uitab(self.WindowResizeTabGroup);
            self.RealspaceTab.Title = 'Real-space';

            % Create RealspaceTabGrid
            self.RealspaceTabGrid = uigridlayout(self.RealspaceTab);
            self.RealspaceTabGrid.ColumnWidth = {'1x'};
            self.RealspaceTabGrid.RowHeight = {'fit'};
            self.RealspaceTabGrid.ColumnSpacing = 4;
            self.RealspaceTabGrid.RowSpacing = 4;
            self.RealspaceTabGrid.Padding = [4 4 4 4];

            % Create RealWindowPanel
            self.RealWindowPanel = uipanel(self.RealspaceTabGrid);
            self.RealWindowPanel.AutoResizeChildren = 'off';
            self.RealWindowPanel.BorderType = 'none';
            self.RealWindowPanel.TitlePosition = 'centertop';
            self.RealWindowPanel.Layout.Row = 1;
            self.RealWindowPanel.Layout.Column = 1;
            self.RealWindowPanel.FontName = 'Arial';
            self.RealWindowPanel.FontWeight = 'bold';

            % Create RealWindowGrid
            self.RealWindowGrid = uigridlayout(self.RealWindowPanel);
            self.RealWindowGrid.ColumnWidth = {12, 60, 12, 60, '1x', 'fit', 'fit'};
            self.RealWindowGrid.RowHeight = {24, 24};
            self.RealWindowGrid.ColumnSpacing = 4;
            self.RealWindowGrid.RowSpacing = 4;
            self.RealWindowGrid.Padding = [0 0 0 4];

            % Create RealAxesGrid
            self.RealAxesGrid = uigridlayout(self.RealWindowGrid);
            self.RealAxesGrid.ColumnWidth = {'1x', 24, 24, 24, '1x', 20, 'fit', '1x'};
            self.RealAxesGrid.RowHeight = {24};
            self.RealAxesGrid.ColumnSpacing = 4;
            self.RealAxesGrid.RowSpacing = 4;
            self.RealAxesGrid.Padding = [0 0 0 0];
            self.RealAxesGrid.Layout.Row = 1;
            self.RealAxesGrid.Layout.Column = [1 7];

            % Create ShowRealAxes
            self.ShowRealAxes = uibutton(self.RealAxesGrid, 'state');
            self.ShowRealAxes.ValueChangedFcn = createCallbackFcn(self, @axis_direction_callbacks, true);
            self.ShowRealAxes.Tag = 'Real';
            self.ShowRealAxes.Tooltip = {'Show Axis Directions on Images'};
            self.ShowRealAxes.Icon = 'axes.png';
            self.ShowRealAxes.Text = '';
            self.ShowRealAxes.Layout.Row = 1;
            self.ShowRealAxes.Layout.Column = 2;
            self.ShowRealAxes.Value = true;

            % Create ReverseRealX
            self.ReverseRealX = uibutton(self.RealAxesGrid, 'state');
            self.ReverseRealX.ValueChangedFcn = createCallbackFcn(self, @axis_direction_callbacks, true);
            self.ReverseRealX.Tag = 'Real';
            self.ReverseRealX.Tooltip = {'Reverse X-axis Direction'};
            self.ReverseRealX.Icon = 'axis-x.png';
            self.ReverseRealX.Text = '';
            self.ReverseRealX.FontWeight = 'bold';
            self.ReverseRealX.Layout.Row = 1;
            self.ReverseRealX.Layout.Column = 3;

            % Create ReverseRealY
            self.ReverseRealY = uibutton(self.RealAxesGrid, 'state');
            self.ReverseRealY.ValueChangedFcn = createCallbackFcn(self, @axis_direction_callbacks, true);
            self.ReverseRealY.Tag = 'Real';
            self.ReverseRealY.Tooltip = {'Reverse Y-axis Direction'};
            self.ReverseRealY.Icon = 'axis-y.png';
            self.ReverseRealY.Text = '';
            self.ReverseRealY.FontWeight = 'bold';
            self.ReverseRealY.Layout.Row = 1;
            self.ReverseRealY.Layout.Column = 4;
            self.ReverseRealY.Value = true;

            % Create RotateRealIcon
            self.RotateRealIcon = uiimage(self.RealAxesGrid);
            self.RotateRealIcon.Tooltip = {'Rotate View'};
            self.RotateRealIcon.Layout.Row = 1;
            self.RotateRealIcon.Layout.Column = 6;
            self.RotateRealIcon.ImageSource = 'right_rotate.png';

            % Create RotateReal
            self.RotateReal = uidropdown(self.RealAxesGrid);
            self.RotateReal.Items = {'0°', '90°', '180°', '-90°'};
            self.RotateReal.ItemsData = [0 90 180 -90];
            self.RotateReal.ValueChangedFcn = createCallbackFcn(self, @axis_direction_callbacks, true);
            self.RotateReal.Tag = 'Real';
            self.RotateReal.Tooltip = {'Rotate Image Display'};
            self.RotateReal.Layout.Row = 1;
            self.RotateReal.Layout.Column = 7;
            self.RotateReal.Value = 0;

            % Create HEditField_2Label
            self.HEditField_2Label = uilabel(self.RealWindowGrid);
            self.HEditField_2Label.HorizontalAlignment = 'right';
            self.HEditField_2Label.Layout.Row = 2;
            self.HEditField_2Label.Layout.Column = 3;
            self.HEditField_2Label.Text = 'H';

            % Create SetRealWindowHeight
            self.SetRealWindowHeight = uieditfield(self.RealWindowGrid, 'numeric');
            self.SetRealWindowHeight.Limits = [1 Inf];
            self.SetRealWindowHeight.RoundFractionalValues = 'on';
            self.SetRealWindowHeight.ValueDisplayFormat = '%.0f';
            self.SetRealWindowHeight.ValueChangedFcn = createCallbackFcn(self, @resize_window, true);
            self.SetRealWindowHeight.Tag = 'Real';
            self.SetRealWindowHeight.Layout.Row = 2;
            self.SetRealWindowHeight.Layout.Column = 4;
            self.SetRealWindowHeight.Value = 400;

            % Create SetRealWindow
            self.SetRealWindow = uibutton(self.RealWindowGrid, 'push');
            self.SetRealWindow.ButtonPushedFcn = createCallbackFcn(self, @resize_window, true);
            self.SetRealWindow.Tag = 'Real';
            self.SetRealWindow.Layout.Row = 2;
            self.SetRealWindow.Layout.Column = 6;
            self.SetRealWindow.Text = 'Set';

            % Create SetAllRealWindows
            self.SetAllRealWindows = uibutton(self.RealWindowGrid, 'push');
            self.SetAllRealWindows.ButtonPushedFcn = createCallbackFcn(self, @resize_window, true);
            self.SetAllRealWindows.Tag = 'Real';
            self.SetAllRealWindows.Layout.Row = 2;
            self.SetAllRealWindows.Layout.Column = 7;
            self.SetAllRealWindows.Text = 'Set All';

            % Create WEditField_2Label
            self.WEditField_2Label = uilabel(self.RealWindowGrid);
            self.WEditField_2Label.HorizontalAlignment = 'right';
            self.WEditField_2Label.Layout.Row = 2;
            self.WEditField_2Label.Layout.Column = 1;
            self.WEditField_2Label.Text = 'W';

            % Create SetRealWindowWidth
            self.SetRealWindowWidth = uieditfield(self.RealWindowGrid, 'numeric');
            self.SetRealWindowWidth.Limits = [1 Inf];
            self.SetRealWindowWidth.RoundFractionalValues = 'on';
            self.SetRealWindowWidth.ValueDisplayFormat = '%.0f';
            self.SetRealWindowWidth.ValueChangedFcn = createCallbackFcn(self, @resize_window, true);
            self.SetRealWindowWidth.Tag = 'Real';
            self.SetRealWindowWidth.Layout.Row = 2;
            self.SetRealWindowWidth.Layout.Column = 2;
            self.SetRealWindowWidth.Value = 400;

            % Create MiscTab
            self.MiscTab = uitab(self.SettingsTabGroup);
            self.MiscTab.AutoResizeChildren = 'off';
            self.MiscTab.Title = 'Misc';

            % Create MiscGrid
            self.MiscGrid = uigridlayout(self.MiscTab);
            self.MiscGrid.ColumnWidth = {'1x'};
            self.MiscGrid.RowHeight = {24, 24, 'fit', 'fit'};
            self.MiscGrid.ColumnSpacing = 4;
            self.MiscGrid.Padding = [4 4 4 4];

            % Create LiveUpdateImagesGrid
            self.LiveUpdateImagesGrid = uigridlayout(self.MiscGrid);
            self.LiveUpdateImagesGrid.ColumnWidth = {'1x', 18, 'fit', 'fit', '1x'};
            self.LiveUpdateImagesGrid.RowHeight = {20};
            self.LiveUpdateImagesGrid.ColumnSpacing = 4;
            self.LiveUpdateImagesGrid.RowSpacing = 4;
            self.LiveUpdateImagesGrid.Padding = [0 0 0 0];
            self.LiveUpdateImagesGrid.Layout.Row = 1;
            self.LiveUpdateImagesGrid.Layout.Column = 1;

            % Create CalculationPolicyIcon
            self.CalculationPolicyIcon = uiimage(self.LiveUpdateImagesGrid);
            self.CalculationPolicyIcon.Tooltip = {''};
            self.CalculationPolicyIcon.Layout.Row = 1;
            self.CalculationPolicyIcon.Layout.Column = 2;
            self.CalculationPolicyIcon.ImageSource = 'refresh.png';

            % Create CalculationPolicyDropDownLabel
            self.CalculationPolicyDropDownLabel = uilabel(self.LiveUpdateImagesGrid);
            self.CalculationPolicyDropDownLabel.HorizontalAlignment = 'right';
            self.CalculationPolicyDropDownLabel.FontName = 'Arial';
            self.CalculationPolicyDropDownLabel.FontWeight = 'bold';
            self.CalculationPolicyDropDownLabel.Tooltip = {''};
            self.CalculationPolicyDropDownLabel.Layout.Row = 1;
            self.CalculationPolicyDropDownLabel.Layout.Column = 3;
            self.CalculationPolicyDropDownLabel.Text = 'Calculation Policy';

            % Create CalculationPolicy
            self.CalculationPolicy = uidropdown(self.LiveUpdateImagesGrid);
            self.CalculationPolicy.Items = {'Active', 'Reduced', 'Passive'};
            self.CalculationPolicy.ItemsData = [2 1 0];
            self.CalculationPolicy.ValueChangedFcn = createCallbackFcn(self, @update_images, true);
            self.CalculationPolicy.Tooltip = {'Policy to calculate/update images:'; '  1) Active - update in real-time.'; '  2) Reduced - update when interactions finish.'; '  3) Passive - update only when the "Update Images" Button (or F5) is pressed or "Diffraction Detector Mode" changes.'};
            self.CalculationPolicy.Layout.Row = 1;
            self.CalculationPolicy.Layout.Column = 4;
            self.CalculationPolicy.Value = 2;

            % Create DetectorCoordinatePanel
            self.DetectorCoordinatePanel = uipanel(self.MiscGrid);
            self.DetectorCoordinatePanel.AutoResizeChildren = 'off';
            self.DetectorCoordinatePanel.BorderType = 'none';
            self.DetectorCoordinatePanel.TitlePosition = 'centertop';
            self.DetectorCoordinatePanel.Title = 'Detector Coordinate Options';
            self.DetectorCoordinatePanel.Layout.Row = 3;
            self.DetectorCoordinatePanel.Layout.Column = 1;
            self.DetectorCoordinatePanel.FontName = 'Arial';
            self.DetectorCoordinatePanel.FontWeight = 'bold';

            % Create DetectorCoordinateGrid
            self.DetectorCoordinateGrid = uigridlayout(self.DetectorCoordinatePanel);
            self.DetectorCoordinateGrid.ColumnWidth = {'1x', 'fit', '1x', 'fit', '1x', 'fit', '1x'};
            self.DetectorCoordinateGrid.RowHeight = {24};
            self.DetectorCoordinateGrid.ColumnSpacing = 4;
            self.DetectorCoordinateGrid.RowSpacing = 4;
            self.DetectorCoordinateGrid.Padding = [0 0 0 4];

            % Create DetectorCoordinateSystem
            self.DetectorCoordinateSystem = uidropdown(self.DetectorCoordinateGrid);
            self.DetectorCoordinateSystem.Items = {'Polar', 'Cartesian'};
            self.DetectorCoordinateSystem.ValueChangedFcn = createCallbackFcn(self, @detector_coordinates_callbacks, true);
            self.DetectorCoordinateSystem.Tooltip = {'Display diffraction coordinates with a Cartesian or polar system'};
            self.DetectorCoordinateSystem.Layout.Row = 1;
            self.DetectorCoordinateSystem.Layout.Column = 2;
            self.DetectorCoordinateSystem.Value = 'Polar';

            % Create DetectorCoordinatePosition
            self.DetectorCoordinatePosition = uidropdown(self.DetectorCoordinateGrid);
            self.DetectorCoordinatePosition.Items = {'Relative', 'Absolute'};
            self.DetectorCoordinatePosition.ValueChangedFcn = createCallbackFcn(self, @detector_coordinates_callbacks, true);
            self.DetectorCoordinatePosition.Tooltip = {'Display diffraction coordinates as absolute positions or relative to the transmitted beam'};
            self.DetectorCoordinatePosition.Layout.Row = 1;
            self.DetectorCoordinatePosition.Layout.Column = 4;
            self.DetectorCoordinatePosition.Value = 'Relative';

            % Create DetectorCoordinateUnit
            self.DetectorCoordinateUnit = uidropdown(self.DetectorCoordinateGrid);
            self.DetectorCoordinateUnit.Items = {'mrad', 'pixels'};
            self.DetectorCoordinateUnit.ItemsData = {'mrad', 'px'};
            self.DetectorCoordinateUnit.ValueChangedFcn = createCallbackFcn(self, @detector_coordinates_callbacks, true);
            self.DetectorCoordinateUnit.Tooltip = {'Display diffraction coordinates in mrad or pixel'};
            self.DetectorCoordinateUnit.Layout.Row = 1;
            self.DetectorCoordinateUnit.Layout.Column = 6;
            self.DetectorCoordinateUnit.Value = 'mrad';

            % Create DatasetOptionPanel
            self.DatasetOptionPanel = uipanel(self.MiscGrid);
            self.DatasetOptionPanel.BorderType = 'none';
            self.DatasetOptionPanel.TitlePosition = 'centertop';
            self.DatasetOptionPanel.Title = 'Swap Dataset Byte Order and Dimensions';
            self.DatasetOptionPanel.Layout.Row = 4;
            self.DatasetOptionPanel.Layout.Column = 1;
            self.DatasetOptionPanel.FontName = 'Arial';
            self.DatasetOptionPanel.FontWeight = 'bold';

            % Create DatasetOptionGrid
            self.DatasetOptionGrid = uigridlayout(self.DatasetOptionPanel);
            self.DatasetOptionGrid.ColumnWidth = {'1x', 'fit', '1x'};
            self.DatasetOptionGrid.RowHeight = {10, 10, 10, 10};
            self.DatasetOptionGrid.ColumnSpacing = 2;
            self.DatasetOptionGrid.RowSpacing = 4;
            self.DatasetOptionGrid.Padding = [0 0 0 4];

            % Create SwapByteOrder
            self.SwapByteOrder = uibutton(self.DatasetOptionGrid, 'push');
            self.SwapByteOrder.ButtonPushedFcn = createCallbackFcn(self, @dataset_options_callbacks, true);
            self.SwapByteOrder.Tooltip = {'Swap the X/Y dimension sizes of the diffraction images, without re-importing'};
            self.SwapByteOrder.Layout.Row = [2 3];
            self.SwapByteOrder.Layout.Column = 1;
            self.SwapByteOrder.Text = 'Swap Byte Order';

            % Create SwapDiffractionXY
            self.SwapDiffractionXY = uibutton(self.DatasetOptionGrid, 'push');
            self.SwapDiffractionXY.ButtonPushedFcn = createCallbackFcn(self, @dataset_options_callbacks, true);
            self.SwapDiffractionXY.Tag = 'Diffraction';
            self.SwapDiffractionXY.Tooltip = {'Swap the X/Y dimension sizes of the diffraction images, without re-importing'};
            self.SwapDiffractionXY.Layout.Row = [1 2];
            self.SwapDiffractionXY.Layout.Column = [2 3];
            self.SwapDiffractionXY.Text = 'Swap Diffraction X/Y';

            % Create SwapRealXY
            self.SwapRealXY = uibutton(self.DatasetOptionGrid, 'push');
            self.SwapRealXY.ButtonPushedFcn = createCallbackFcn(self, @dataset_options_callbacks, true);
            self.SwapRealXY.Tag = 'Real';
            self.SwapRealXY.Tooltip = {'Swap the X/Y dimension sizes of the real-space images, without re-importing'};
            self.SwapRealXY.Layout.Row = [3 4];
            self.SwapRealXY.Layout.Column = [2 3];
            self.SwapRealXY.Text = 'Swap Real-space X/Y';

            % Create InfoTab
            self.InfoTab = uitab(self.SettingsTabGroup);
            self.InfoTab.AutoResizeChildren = 'off';
            self.InfoTab.Title = 'Info';

            % Create InfoGrid
            self.InfoGrid = uigridlayout(self.InfoTab);
            self.InfoGrid.ColumnWidth = {'1x'};
            self.InfoGrid.RowHeight = {'fit', '1x', 'fit'};
            self.InfoGrid.ColumnSpacing = 4;
            self.InfoGrid.RowSpacing = 4;
            self.InfoGrid.Padding = [4 4 4 4];

            % Create DatasetInfoTextAreaLabel
            self.DatasetInfoTextAreaLabel = uilabel(self.InfoGrid);
            self.DatasetInfoTextAreaLabel.HorizontalAlignment = 'center';
            self.DatasetInfoTextAreaLabel.VerticalAlignment = 'bottom';
            self.DatasetInfoTextAreaLabel.FontName = 'Arial';
            self.DatasetInfoTextAreaLabel.FontWeight = 'bold';
            self.DatasetInfoTextAreaLabel.Layout.Row = 1;
            self.DatasetInfoTextAreaLabel.Layout.Column = 1;
            self.DatasetInfoTextAreaLabel.Text = 'Dataset Info';

            % Create DatasetInfo
            self.DatasetInfo = uitextarea(self.InfoGrid);
            self.DatasetInfo.Editable = 'off';
            self.DatasetInfo.FontName = 'Arial';
            self.DatasetInfo.Layout.Row = 2;
            self.DatasetInfo.Layout.Column = 1;

            % Create ShowVariables
            self.ShowVariables = uibutton(self.InfoGrid, 'state');
            self.ShowVariables.ValueChangedFcn = createCallbackFcn(self, @variable_viewer, true);
            self.ShowVariables.Text = 'Show all variables';
            self.ShowVariables.FontWeight = 'bold';
            self.ShowVariables.Layout.Row = 3;
            self.ShowVariables.Layout.Column = 1;

            % Create MathTab
            self.MathTab = uitab(self.SettingsTabGroup);
            self.MathTab.Title = 'Math';

            % Create MathGrid
            self.MathGrid = uigridlayout(self.MathTab);
            self.MathGrid.ColumnWidth = {'1x'};
            self.MathGrid.RowHeight = {'fit', 'fit', '1x', 24};
            self.MathGrid.ColumnSpacing = 4;
            self.MathGrid.RowSpacing = 4;
            self.MathGrid.Padding = [4 4 4 4];

            % Create MathExampleGrid
            self.MathExampleGrid = uigridlayout(self.MathGrid);
            self.MathExampleGrid.ColumnWidth = {'1x', 18};
            self.MathExampleGrid.RowHeight = {18, '1x'};
            self.MathExampleGrid.ColumnSpacing = 4;
            self.MathExampleGrid.RowSpacing = 2;
            self.MathExampleGrid.Padding = [0 0 0 0];
            self.MathExampleGrid.Layout.Row = 1;
            self.MathExampleGrid.Layout.Column = 1;

            % Create MathExample
            self.MathExample = uilabel(self.MathExampleGrid);
            self.MathExample.FontName = 'Arial';
            self.MathExample.Layout.Row = [1 2];
            self.MathExample.Layout.Column = [1 2];
            self.MathExample.Interpreter = 'html';
            self.MathExample.Text = {'<center><b>Syntax Examples</b></center>• Union of B and C, then intersects with A:'; '<b style="font-family:''Consolas''">  A & (B | C)</b>'; '• A squared plus B times C (element-wisely), then transposed:'; '<b style="font-family:''Consolas''">  (A.^2 + B .* C)''</b>'; '• Concatenates (on X-dimension) A''s Rows 1-3  to B''s Rows 4-to-last:'; '<b style="font-family:''Consolas''">  [A(1:3,:) ; B(4:end,:)]</b>'};

            % Create MathHelpIcon
            self.MathHelpIcon = uiimage(self.MathExampleGrid);
            self.MathHelpIcon.Tooltip = {'• MATLAB syntax/functions are used.'; '• The X/Y dimensions (in images) are corresponding to the 1st/2nd dimensions (Rows/Columns) of arrays, respectively.'};
            self.MathHelpIcon.Layout.Row = 1;
            self.MathHelpIcon.Layout.Column = 2;
            self.MathHelpIcon.ImageSource = 'help.png';

            % Create FormulaLabel
            self.FormulaLabel = uilabel(self.MathGrid);
            self.FormulaLabel.HorizontalAlignment = 'center';
            self.FormulaLabel.FontName = 'Arial';
            self.FormulaLabel.FontWeight = 'bold';
            self.FormulaLabel.Layout.Row = 2;
            self.FormulaLabel.Layout.Column = 1;
            self.FormulaLabel.Text = 'Formula';

            % Create MathFormula
            self.MathFormula = uitextarea(self.MathGrid);
            self.MathFormula.FontName = 'Arial';
            self.MathFormula.Layout.Row = 3;
            self.MathFormula.Layout.Column = 1;

            % Create EvaluateGrid
            self.EvaluateGrid = uigridlayout(self.MathGrid);
            self.EvaluateGrid.ColumnWidth = {18, '1x', 'fit', '1x', 18};
            self.EvaluateGrid.RowHeight = {'1x'};
            self.EvaluateGrid.ColumnSpacing = 4;
            self.EvaluateGrid.RowSpacing = 4;
            self.EvaluateGrid.Padding = [0 0 0 0];
            self.EvaluateGrid.Layout.Row = 4;
            self.EvaluateGrid.Layout.Column = 1;

            % Create Evaluate
            self.Evaluate = uibutton(self.EvaluateGrid, 'push');
            self.Evaluate.ButtonPushedFcn = createCallbackFcn(self, @custom_detector_callbacks, true);
            self.Evaluate.FontName = 'Arial';
            self.Evaluate.Layout.Row = 1;
            self.Evaluate.Layout.Column = 3;
            self.Evaluate.Text = 'Evaluate';

            % Create VariablesTab
            self.VariablesTab = uitab(self.SettingsTabGroup);
            self.VariablesTab.Title = 'Variables';

            % Create VariablesGrid
            self.VariablesGrid = uigridlayout(self.VariablesTab);
            self.VariablesGrid.ColumnWidth = {'1x'};

            % Create VariablesTable
            self.VariablesTable = uitable(self.VariablesGrid);
            self.VariablesTable.ColumnName = {'Value'};
            self.VariablesTable.ColumnWidth = {'1x'};
            self.VariablesTable.RowName = {};
            self.VariablesTable.Layout.Row = 2;
            self.VariablesTable.Layout.Column = 1;

            % Create VariablesTree
            self.VariablesTree = uitree(self.VariablesGrid);
            self.VariablesTree.SelectionChangedFcn = createCallbackFcn(self, @variable_viewer, true);
            self.VariablesTree.Layout.Row = 1;
            self.VariablesTree.Layout.Column = 1;

            % Create ModeTabGroup
            self.ModeTabGroup = uitabgroup(self.Quant4D_Fig);
            self.ModeTabGroup.TabLocation = 'bottom';
            self.ModeTabGroup.Position = [-266 85 260 328];

            % Create PreviewTab
            self.PreviewTab = uitab(self.ModeTabGroup);
            self.PreviewTab.Title = 'Pv';

            % Create PreviewGrid
            self.PreviewGrid = uigridlayout(self.PreviewTab);
            self.PreviewGrid.ColumnWidth = {'1x'};
            self.PreviewGrid.RowHeight = {'1x'};
            self.PreviewGrid.ColumnSpacing = 4;
            self.PreviewGrid.RowSpacing = 4;
            self.PreviewGrid.Padding = [4 4 4 4];

            % Create PreviewFramePanel
            self.PreviewFramePanel = uipanel(self.PreviewGrid);
            self.PreviewFramePanel.BorderType = 'none';
            self.PreviewFramePanel.TitlePosition = 'centertop';
            self.PreviewFramePanel.Title = 'Preview Frame';
            self.PreviewFramePanel.Layout.Row = 1;
            self.PreviewFramePanel.Layout.Column = 1;
            self.PreviewFramePanel.FontName = 'Arial';
            self.PreviewFramePanel.FontWeight = 'bold';

            % Create PreviewButtonGrid
            self.PreviewButtonGrid = uigridlayout(self.PreviewFramePanel);
            self.PreviewButtonGrid.ColumnWidth = {'1x', '1x', '1x'};
            self.PreviewButtonGrid.RowHeight = {24, 24, 24, '1x'};
            self.PreviewButtonGrid.ColumnSpacing = 2;
            self.PreviewButtonGrid.RowSpacing = 2;
            self.PreviewButtonGrid.Padding = [0 0 0 4];

            % Create PreviewFrame_1_1
            self.PreviewFrame_1_1 = uibutton(self.PreviewButtonGrid, 'push');
            self.PreviewFrame_1_1.ButtonPushedFcn = createCallbackFcn(self, @preview_callbacks, true);
            self.PreviewFrame_1_1.FontName = 'Consolas';
            self.PreviewFrame_1_1.Layout.Row = 1;
            self.PreviewFrame_1_1.Layout.Column = 1;
            self.PreviewFrame_1_1.Text = '[1,1]';

            % Create PreviewFrame_X2_1
            self.PreviewFrame_X2_1 = uibutton(self.PreviewButtonGrid, 'push');
            self.PreviewFrame_X2_1.ButtonPushedFcn = createCallbackFcn(self, @preview_callbacks, true);
            self.PreviewFrame_X2_1.FontName = 'Consolas';
            self.PreviewFrame_X2_1.Layout.Row = 1;
            self.PreviewFrame_X2_1.Layout.Column = 2;
            self.PreviewFrame_X2_1.Text = '[X/2,1]';

            % Create PreviewFrame_X_1
            self.PreviewFrame_X_1 = uibutton(self.PreviewButtonGrid, 'push');
            self.PreviewFrame_X_1.ButtonPushedFcn = createCallbackFcn(self, @preview_callbacks, true);
            self.PreviewFrame_X_1.FontName = 'Consolas';
            self.PreviewFrame_X_1.Layout.Row = 1;
            self.PreviewFrame_X_1.Layout.Column = 3;
            self.PreviewFrame_X_1.Text = '[X,1]';

            % Create PreviewFrame_1_Y2
            self.PreviewFrame_1_Y2 = uibutton(self.PreviewButtonGrid, 'push');
            self.PreviewFrame_1_Y2.ButtonPushedFcn = createCallbackFcn(self, @preview_callbacks, true);
            self.PreviewFrame_1_Y2.FontName = 'Consolas';
            self.PreviewFrame_1_Y2.Layout.Row = 2;
            self.PreviewFrame_1_Y2.Layout.Column = 1;
            self.PreviewFrame_1_Y2.Text = '[1,Y/2]';

            % Create PreviewFrame_X2_Y2
            self.PreviewFrame_X2_Y2 = uibutton(self.PreviewButtonGrid, 'push');
            self.PreviewFrame_X2_Y2.ButtonPushedFcn = createCallbackFcn(self, @preview_callbacks, true);
            self.PreviewFrame_X2_Y2.FontName = 'Consolas';
            self.PreviewFrame_X2_Y2.Layout.Row = 2;
            self.PreviewFrame_X2_Y2.Layout.Column = 2;
            self.PreviewFrame_X2_Y2.Text = '[X/2,Y/2]';

            % Create PreviewFrame_X_Y2
            self.PreviewFrame_X_Y2 = uibutton(self.PreviewButtonGrid, 'push');
            self.PreviewFrame_X_Y2.ButtonPushedFcn = createCallbackFcn(self, @preview_callbacks, true);
            self.PreviewFrame_X_Y2.FontName = 'Consolas';
            self.PreviewFrame_X_Y2.Layout.Row = 2;
            self.PreviewFrame_X_Y2.Layout.Column = 3;
            self.PreviewFrame_X_Y2.Text = '[X,Y/2]';

            % Create PreviewFrame_1_Y
            self.PreviewFrame_1_Y = uibutton(self.PreviewButtonGrid, 'push');
            self.PreviewFrame_1_Y.ButtonPushedFcn = createCallbackFcn(self, @preview_callbacks, true);
            self.PreviewFrame_1_Y.FontName = 'Consolas';
            self.PreviewFrame_1_Y.Layout.Row = 3;
            self.PreviewFrame_1_Y.Layout.Column = 1;
            self.PreviewFrame_1_Y.Text = '[1,Y]';

            % Create PreviewFrame_X2_Y
            self.PreviewFrame_X2_Y = uibutton(self.PreviewButtonGrid, 'push');
            self.PreviewFrame_X2_Y.ButtonPushedFcn = createCallbackFcn(self, @preview_callbacks, true);
            self.PreviewFrame_X2_Y.FontName = 'Consolas';
            self.PreviewFrame_X2_Y.Layout.Row = 3;
            self.PreviewFrame_X2_Y.Layout.Column = 2;
            self.PreviewFrame_X2_Y.Text = '[X/2,Y]';

            % Create PreviewFrame_X_Y
            self.PreviewFrame_X_Y = uibutton(self.PreviewButtonGrid, 'push');
            self.PreviewFrame_X_Y.ButtonPushedFcn = createCallbackFcn(self, @preview_callbacks, true);
            self.PreviewFrame_X_Y.FontName = 'Consolas';
            self.PreviewFrame_X_Y.Layout.Row = 3;
            self.PreviewFrame_X_Y.Layout.Column = 3;
            self.PreviewFrame_X_Y.Text = '[X,Y]';

            % Create PreviewFrameGrid
            self.PreviewFrameGrid = uigridlayout(self.PreviewButtonGrid);
            self.PreviewFrameGrid.ColumnWidth = {'1x', 'fit', '1x', 'fit', '1x'};
            self.PreviewFrameGrid.RowHeight = {24};
            self.PreviewFrameGrid.ColumnSpacing = 4;
            self.PreviewFrameGrid.RowSpacing = 4;
            self.PreviewFrameGrid.Padding = [0 0 0 4];
            self.PreviewFrameGrid.Layout.Row = 4;
            self.PreviewFrameGrid.Layout.Column = [1 3];

            % Create PreviewButton
            self.PreviewButton = uibutton(self.PreviewFrameGrid, 'push');
            self.PreviewButton.ButtonPushedFcn = createCallbackFcn(self, @preview_callbacks, true);
            self.PreviewButton.FontName = 'Arial';
            self.PreviewButton.FontWeight = 'bold';
            self.PreviewButton.Layout.Row = 1;
            self.PreviewButton.Layout.Column = 1;
            self.PreviewButton.Text = 'Preview';

            % Create PvFrXLabel
            self.PvFrXLabel = uilabel(self.PreviewFrameGrid);
            self.PvFrXLabel.HorizontalAlignment = 'right';
            self.PvFrXLabel.Layout.Row = 1;
            self.PvFrXLabel.Layout.Column = 2;
            self.PvFrXLabel.Text = 'X';

            % Create PreviewFrameX
            self.PreviewFrameX = uispinner(self.PreviewFrameGrid);
            self.PreviewFrameX.RoundFractionalValues = 'on';
            self.PreviewFrameX.ValueDisplayFormat = '%.0f';
            self.PreviewFrameX.ValueChangedFcn = createCallbackFcn(self, @preview_callbacks, true);
            self.PreviewFrameX.Layout.Row = 1;
            self.PreviewFrameX.Layout.Column = 3;
            self.PreviewFrameX.Value = 1;

            % Create PvFrYLabel
            self.PvFrYLabel = uilabel(self.PreviewFrameGrid);
            self.PvFrYLabel.HorizontalAlignment = 'right';
            self.PvFrYLabel.Layout.Row = 1;
            self.PvFrYLabel.Layout.Column = 4;
            self.PvFrYLabel.Text = 'Y';

            % Create PreviewFrameY
            self.PreviewFrameY = uispinner(self.PreviewFrameGrid);
            self.PreviewFrameY.RoundFractionalValues = 'on';
            self.PreviewFrameY.ValueDisplayFormat = '%.0f';
            self.PreviewFrameY.ValueChangedFcn = createCallbackFcn(self, @preview_callbacks, true);
            self.PreviewFrameY.Layout.Row = 1;
            self.PreviewFrameY.Layout.Column = 5;
            self.PreviewFrameY.Value = 1;

            % Create AlignmentTab
            self.AlignmentTab = uitab(self.ModeTabGroup);
            self.AlignmentTab.Title = 'Align';
            self.AlignmentTab.BackgroundColor = [0.9412 0.9412 0.9412];

            % Create AlignmentGrid
            self.AlignmentGrid = uigridlayout(self.AlignmentTab);
            self.AlignmentGrid.ColumnWidth = {'1x'};
            self.AlignmentGrid.RowHeight = {'fit', 'fit', 18};
            self.AlignmentGrid.ColumnSpacing = 4;
            self.AlignmentGrid.RowSpacing = 4;
            self.AlignmentGrid.Padding = [4 4 4 4];

            % Create DiffractionCalibrationPanel
            self.DiffractionCalibrationPanel = uipanel(self.AlignmentGrid);
            self.DiffractionCalibrationPanel.BorderType = 'none';
            self.DiffractionCalibrationPanel.TitlePosition = 'centertop';
            self.DiffractionCalibrationPanel.Title = 'Diffraction Calibration';
            self.DiffractionCalibrationPanel.Layout.Row = 1;
            self.DiffractionCalibrationPanel.Layout.Column = 1;
            self.DiffractionCalibrationPanel.FontName = 'Arial';
            self.DiffractionCalibrationPanel.FontWeight = 'bold';

            % Create DiffractionCalibrationGrid
            self.DiffractionCalibrationGrid = uigridlayout(self.DiffractionCalibrationPanel);
            self.DiffractionCalibrationGrid.ColumnWidth = {'1x', 58, 58, '1x'};
            self.DiffractionCalibrationGrid.RowHeight = {24, 24};
            self.DiffractionCalibrationGrid.ColumnSpacing = 4;
            self.DiffractionCalibrationGrid.RowSpacing = 4;
            self.DiffractionCalibrationGrid.Padding = [0 0 0 4];

            % Create ConvergenceAngleLabel
            self.ConvergenceAngleLabel = uilabel(self.DiffractionCalibrationGrid);
            self.ConvergenceAngleLabel.HorizontalAlignment = 'right';
            self.ConvergenceAngleLabel.Layout.Row = 1;
            self.ConvergenceAngleLabel.Layout.Column = [1 2];
            self.ConvergenceAngleLabel.Text = 'Convergence Angle';

            % Create Alpha
            self.Alpha = uieditfield(self.DiffractionCalibrationGrid, 'numeric');
            self.Alpha.Limits = [0 Inf];
            self.Alpha.ValueDisplayFormat = '%.2f';
            self.Alpha.ValueChangedFcn = createCallbackFcn(self, @transmitted_beam_callbacks, true);
            self.Alpha.Layout.Row = 1;
            self.Alpha.Layout.Column = 3;
            self.Alpha.Value = 12;

            % Create AlphaLabel
            self.AlphaLabel = uilabel(self.DiffractionCalibrationGrid);
            self.AlphaLabel.Layout.Row = 1;
            self.AlphaLabel.Layout.Column = 4;
            self.AlphaLabel.Text = 'mrad';

            % Create DiffractionScaleLabel
            self.DiffractionScaleLabel = uilabel(self.DiffractionCalibrationGrid);
            self.DiffractionScaleLabel.HorizontalAlignment = 'right';
            self.DiffractionScaleLabel.Layout.Row = 2;
            self.DiffractionScaleLabel.Layout.Column = [1 2];
            self.DiffractionScaleLabel.Text = 'Diffraction Scale';

            % Create mradPx
            self.mradPx = uieditfield(self.DiffractionCalibrationGrid, 'numeric');
            self.mradPx.Limits = [0 Inf];
            self.mradPx.ValueDisplayFormat = '%.4g';
            self.mradPx.ValueChangedFcn = createCallbackFcn(self, @transmitted_beam_callbacks, true);
            self.mradPx.Layout.Row = 2;
            self.mradPx.Layout.Column = 3;
            self.mradPx.Value = 1;

            % Create mradPxLabel
            self.mradPxLabel = uilabel(self.DiffractionCalibrationGrid);
            self.mradPxLabel.Layout.Row = 2;
            self.mradPxLabel.Layout.Column = 4;
            self.mradPxLabel.Text = 'mrad/px';

            % Create TransBeamAlignPanel
            self.TransBeamAlignPanel = uipanel(self.AlignmentGrid);
            self.TransBeamAlignPanel.BorderType = 'none';
            self.TransBeamAlignPanel.TitlePosition = 'centertop';
            self.TransBeamAlignPanel.Title = 'Transmitted Beam Position Alignment';
            self.TransBeamAlignPanel.Layout.Row = 2;
            self.TransBeamAlignPanel.Layout.Column = 1;
            self.TransBeamAlignPanel.FontName = 'Arial';
            self.TransBeamAlignPanel.FontWeight = 'bold';

            % Create TransBeamAlignGrid
            self.TransBeamAlignGrid = uigridlayout(self.TransBeamAlignPanel);
            self.TransBeamAlignGrid.ColumnWidth = {'1x', 80, 80, '1x'};
            self.TransBeamAlignGrid.RowHeight = {24, 2, 24, 'fit', 2, 24, 'fit', 2, 24, 'fit'};
            self.TransBeamAlignGrid.ColumnSpacing = 4;
            self.TransBeamAlignGrid.RowSpacing = 2;
            self.TransBeamAlignGrid.Padding = [0 0 0 4];

            % Create TBAutoAlign
            self.TBAutoAlign = uibutton(self.TransBeamAlignGrid, 'push');
            self.TBAutoAlign.ButtonPushedFcn = createCallbackFcn(self, @transmitted_beam_callbacks, true);
            self.TBAutoAlign.Layout.Row = 1;
            self.TBAutoAlign.Layout.Column = [2 3];
            self.TBAutoAlign.Text = 'Auto Align';

            % Create TBCrossAlign
            self.TBCrossAlign = uibutton(self.TransBeamAlignGrid, 'push');
            self.TBCrossAlign.ButtonPushedFcn = createCallbackFcn(self, @transmitted_beam_callbacks, true);
            self.TBCrossAlign.Tooltip = {'Align transmitted beam location as the crossing point of two lines'};
            self.TBCrossAlign.Layout.Row = 1;
            self.TBCrossAlign.Layout.Column = 4;
            self.TBCrossAlign.Text = 'X';

            % Create TBRLabel
            self.TBRLabel = uilabel(self.TransBeamAlignGrid);
            self.TBRLabel.HorizontalAlignment = 'right';
            self.TBRLabel.Layout.Row = 3;
            self.TBRLabel.Layout.Column = 2;
            self.TBRLabel.Text = 'Radius';

            % Create TransBeamRSpinner
            self.TransBeamRSpinner = uispinner(self.TransBeamAlignGrid);
            self.TransBeamRSpinner.Step = 0.25;
            self.TransBeamRSpinner.ValueChangingFcn = createCallbackFcn(self, @transmitted_beam_callbacks, true);
            self.TransBeamRSpinner.ValueDisplayFormat = '%.2f';
            self.TransBeamRSpinner.ValueChangedFcn = createCallbackFcn(self, @transmitted_beam_callbacks, true);
            self.TransBeamRSpinner.Layout.Row = 3;
            self.TransBeamRSpinner.Layout.Column = 3;

            % Create TBR_NFLabel
            self.TBR_NFLabel = uilabel(self.TransBeamAlignGrid);
            self.TBR_NFLabel.Layout.Row = 3;
            self.TBR_NFLabel.Layout.Column = 4;
            self.TBR_NFLabel.Text = 'px';

            % Create TransBeamR
            self.TransBeamR = uislider(self.TransBeamAlignGrid);
            self.TransBeamR.MajorTicks = [];
            self.TransBeamR.ValueChangedFcn = createCallbackFcn(self, @transmitted_beam_callbacks, true);
            self.TransBeamR.ValueChangingFcn = createCallbackFcn(self, @transmitted_beam_callbacks, true);
            self.TransBeamR.Layout.Row = 4;
            self.TransBeamR.Layout.Column = [1 4];

            % Create TBXLabel
            self.TBXLabel = uilabel(self.TransBeamAlignGrid);
            self.TBXLabel.HorizontalAlignment = 'right';
            self.TBXLabel.Layout.Row = 6;
            self.TBXLabel.Layout.Column = 2;
            self.TBXLabel.Text = 'X';

            % Create TransBeamXSpinner
            self.TransBeamXSpinner = uispinner(self.TransBeamAlignGrid);
            self.TransBeamXSpinner.Step = 0.25;
            self.TransBeamXSpinner.ValueChangingFcn = createCallbackFcn(self, @transmitted_beam_callbacks, true);
            self.TransBeamXSpinner.ValueDisplayFormat = '%.2f';
            self.TransBeamXSpinner.ValueChangedFcn = createCallbackFcn(self, @transmitted_beam_callbacks, true);
            self.TransBeamXSpinner.Layout.Row = 6;
            self.TransBeamXSpinner.Layout.Column = 3;

            % Create TBX_NFLabel
            self.TBX_NFLabel = uilabel(self.TransBeamAlignGrid);
            self.TBX_NFLabel.Layout.Row = 6;
            self.TBX_NFLabel.Layout.Column = 4;
            self.TBX_NFLabel.Text = 'px';

            % Create TransBeamX
            self.TransBeamX = uislider(self.TransBeamAlignGrid);
            self.TransBeamX.MajorTicks = [];
            self.TransBeamX.ValueChangedFcn = createCallbackFcn(self, @transmitted_beam_callbacks, true);
            self.TransBeamX.ValueChangingFcn = createCallbackFcn(self, @transmitted_beam_callbacks, true);
            self.TransBeamX.Layout.Row = 7;
            self.TransBeamX.Layout.Column = [1 4];

            % Create TBYLabel
            self.TBYLabel = uilabel(self.TransBeamAlignGrid);
            self.TBYLabel.HorizontalAlignment = 'right';
            self.TBYLabel.Layout.Row = 9;
            self.TBYLabel.Layout.Column = 2;
            self.TBYLabel.Text = 'Y';

            % Create TransBeamYSpinner
            self.TransBeamYSpinner = uispinner(self.TransBeamAlignGrid);
            self.TransBeamYSpinner.Step = 0.25;
            self.TransBeamYSpinner.ValueChangingFcn = createCallbackFcn(self, @transmitted_beam_callbacks, true);
            self.TransBeamYSpinner.ValueDisplayFormat = '%.2f';
            self.TransBeamYSpinner.ValueChangedFcn = createCallbackFcn(self, @transmitted_beam_callbacks, true);
            self.TransBeamYSpinner.Layout.Row = 9;
            self.TransBeamYSpinner.Layout.Column = 3;

            % Create TBY_NFLabel
            self.TBY_NFLabel = uilabel(self.TransBeamAlignGrid);
            self.TBY_NFLabel.Layout.Row = 9;
            self.TBY_NFLabel.Layout.Column = 4;
            self.TBY_NFLabel.Text = 'px';

            % Create TransBeamY
            self.TransBeamY = uislider(self.TransBeamAlignGrid);
            self.TransBeamY.MajorTicks = [];
            self.TransBeamY.ValueChangedFcn = createCallbackFcn(self, @transmitted_beam_callbacks, true);
            self.TransBeamY.ValueChangingFcn = createCallbackFcn(self, @transmitted_beam_callbacks, true);
            self.TransBeamY.Layout.Row = 10;
            self.TransBeamY.Layout.Column = [1 4];

            % Create AlignmentHelpIcon
            self.AlignmentHelpIcon = uiimage(self.AlignmentGrid);
            self.AlignmentHelpIcon.Tooltip = {'1. Set "Convergence Angle"'; '2. Align the transmitted beam''s X/Y location'; '3. Switch from "Alignment" to another mode'};
            self.AlignmentHelpIcon.Layout.Row = 3;
            self.AlignmentHelpIcon.Layout.Column = 1;
            self.AlignmentHelpIcon.ImageSource = 'help.png';

            % Create AnnularDetectorTab
            self.AnnularDetectorTab = uitab(self.ModeTabGroup);
            self.AnnularDetectorTab.Title = 'Ann';
            self.AnnularDetectorTab.BackgroundColor = [0.9412 0.9412 0.9412];

            % Create AnnularDetectorGrid
            self.AnnularDetectorGrid = uigridlayout(self.AnnularDetectorTab);
            self.AnnularDetectorGrid.ColumnWidth = {'1x'};
            self.AnnularDetectorGrid.RowHeight = {'fit', 'fit', 'fit', '1x', 24};
            self.AnnularDetectorGrid.ColumnSpacing = 4;
            self.AnnularDetectorGrid.RowSpacing = 4;
            self.AnnularDetectorGrid.Padding = [4 4 4 4];

            % Create AnnularRadiiPanel
            self.AnnularRadiiPanel = uipanel(self.AnnularDetectorGrid);
            self.AnnularRadiiPanel.BorderType = 'none';
            self.AnnularRadiiPanel.TitlePosition = 'centertop';
            self.AnnularRadiiPanel.Title = 'Annular Detector Radii';
            self.AnnularRadiiPanel.Layout.Row = 1;
            self.AnnularRadiiPanel.Layout.Column = 1;
            self.AnnularRadiiPanel.FontName = 'Arial';
            self.AnnularRadiiPanel.FontWeight = 'bold';

            % Create AnnularRadiiGrid
            self.AnnularRadiiGrid = uigridlayout(self.AnnularRadiiPanel);
            self.AnnularRadiiGrid.ColumnWidth = {24, '1x', 52, 80, '1x'};
            self.AnnularRadiiGrid.RowHeight = {24, 'fit', 2, 24, 'fit', 2};
            self.AnnularRadiiGrid.ColumnSpacing = 4;
            self.AnnularRadiiGrid.RowSpacing = 2;
            self.AnnularRadiiGrid.Padding = [0 0 0 4];

            % Create AnnRiLabel
            self.AnnRiLabel = uilabel(self.AnnularRadiiGrid);
            self.AnnRiLabel.HorizontalAlignment = 'right';
            self.AnnRiLabel.Layout.Row = 1;
            self.AnnRiLabel.Layout.Column = [2 3];
            self.AnnRiLabel.Text = 'Inner Radius';

            % Create InnerAnnularRadiusSpinner
            self.InnerAnnularRadiusSpinner = uispinner(self.AnnularRadiiGrid);
            self.InnerAnnularRadiusSpinner.Step = 0.25;
            self.InnerAnnularRadiusSpinner.ValueChangingFcn = createCallbackFcn(self, @annular_detector_callbacks, true);
            self.InnerAnnularRadiusSpinner.ValueDisplayFormat = '%.2f';
            self.InnerAnnularRadiusSpinner.ValueChangedFcn = createCallbackFcn(self, @annular_detector_callbacks, true);
            self.InnerAnnularRadiusSpinner.Tag = 'AnnDetr RI';
            self.InnerAnnularRadiusSpinner.Layout.Row = 1;
            self.InnerAnnularRadiusSpinner.Layout.Column = 4;

            % Create AnnRi_NFLabel
            self.AnnRi_NFLabel = uilabel(self.AnnularRadiiGrid);
            self.AnnRi_NFLabel.Layout.Row = 1;
            self.AnnRi_NFLabel.Layout.Column = 5;
            self.AnnRi_NFLabel.Text = 'mrad';

            % Create InnerAnnularRadius
            self.InnerAnnularRadius = uislider(self.AnnularRadiiGrid);
            self.InnerAnnularRadius.MajorTicks = [];
            self.InnerAnnularRadius.ValueChangedFcn = createCallbackFcn(self, @annular_detector_callbacks, true);
            self.InnerAnnularRadius.ValueChangingFcn = createCallbackFcn(self, @annular_detector_callbacks, true);
            self.InnerAnnularRadius.Tag = 'AnnDetr RI';
            self.InnerAnnularRadius.Layout.Row = 2;
            self.InnerAnnularRadius.Layout.Column = [1 5];

            % Create AnnularRadiusLink
            self.AnnularRadiusLink = uibutton(self.AnnularRadiiGrid, 'state');
            self.AnnularRadiusLink.ValueChangedFcn = createCallbackFcn(self, @annular_detector_callbacks, true);
            self.AnnularRadiusLink.Tag = 'AnnDetr';
            self.AnnularRadiusLink.Tooltip = {'Move inner/outer annular sliders together'};
            self.AnnularRadiusLink.Icon = 'link.png';
            self.AnnularRadiusLink.Text = '';
            self.AnnularRadiusLink.Layout.Row = 4;
            self.AnnularRadiusLink.Layout.Column = 1;

            % Create AnnRoLabel
            self.AnnRoLabel = uilabel(self.AnnularRadiiGrid);
            self.AnnRoLabel.HorizontalAlignment = 'right';
            self.AnnRoLabel.Layout.Row = 4;
            self.AnnRoLabel.Layout.Column = [2 3];
            self.AnnRoLabel.Text = 'Outer Radius';

            % Create OuterAnnularRadiusSpinner
            self.OuterAnnularRadiusSpinner = uispinner(self.AnnularRadiiGrid);
            self.OuterAnnularRadiusSpinner.Step = 0.25;
            self.OuterAnnularRadiusSpinner.ValueChangingFcn = createCallbackFcn(self, @annular_detector_callbacks, true);
            self.OuterAnnularRadiusSpinner.ValueDisplayFormat = '%.2f';
            self.OuterAnnularRadiusSpinner.ValueChangedFcn = createCallbackFcn(self, @annular_detector_callbacks, true);
            self.OuterAnnularRadiusSpinner.Tag = 'AnnDetr RO';
            self.OuterAnnularRadiusSpinner.Layout.Row = 4;
            self.OuterAnnularRadiusSpinner.Layout.Column = 4;

            % Create AnnRo_NFLabel
            self.AnnRo_NFLabel = uilabel(self.AnnularRadiiGrid);
            self.AnnRo_NFLabel.Layout.Row = 4;
            self.AnnRo_NFLabel.Layout.Column = 5;
            self.AnnRo_NFLabel.Text = 'mrad';

            % Create OuterAnnularRadius
            self.OuterAnnularRadius = uislider(self.AnnularRadiiGrid);
            self.OuterAnnularRadius.MajorTicks = [];
            self.OuterAnnularRadius.ValueChangedFcn = createCallbackFcn(self, @annular_detector_callbacks, true);
            self.OuterAnnularRadius.ValueChangingFcn = createCallbackFcn(self, @annular_detector_callbacks, true);
            self.OuterAnnularRadius.Tag = 'AnnDetr RO';
            self.OuterAnnularRadius.Layout.Row = 5;
            self.OuterAnnularRadius.Layout.Column = [1 5];

            % Create ScanDirectionPanel
            self.ScanDirectionPanel = uipanel(self.AnnularDetectorGrid);
            self.ScanDirectionPanel.BorderType = 'none';
            self.ScanDirectionPanel.TitlePosition = 'centertop';
            self.ScanDirectionPanel.Title = 'Scanning Direction';
            self.ScanDirectionPanel.Visible = 'off';
            self.ScanDirectionPanel.Layout.Row = 2;
            self.ScanDirectionPanel.Layout.Column = 1;
            self.ScanDirectionPanel.FontName = 'Arial';
            self.ScanDirectionPanel.FontWeight = 'bold';

            % Create ScanDirectionGrid
            self.ScanDirectionGrid = uigridlayout(self.ScanDirectionPanel);
            self.ScanDirectionGrid.ColumnWidth = {24, 24, 24, 24, '1x', 80, '1x', 24};
            self.ScanDirectionGrid.RowHeight = {24, 14};
            self.ScanDirectionGrid.ColumnSpacing = 4;
            self.ScanDirectionGrid.RowSpacing = 2;
            self.ScanDirectionGrid.Padding = [0 0 0 4];

            % Create ScanDirectionLock
            self.ScanDirectionLock = uibutton(self.ScanDirectionGrid, 'state');
            self.ScanDirectionLock.ValueChangedFcn = createCallbackFcn(self, @annular_detector_callbacks, true);
            self.ScanDirectionLock.Tag = 'ScanDir';
            self.ScanDirectionLock.Icon = 'unlock.png';
            self.ScanDirectionLock.Text = '';
            self.ScanDirectionLock.Layout.Row = 1;
            self.ScanDirectionLock.Layout.Column = 1;

            % Create AutoCurl
            self.AutoCurl = uibutton(self.ScanDirectionGrid, 'push');
            self.AutoCurl.ButtonPushedFcn = createCallbackFcn(self, @annular_detector_callbacks, true);
            self.AutoCurl.Layout.Row = 1;
            self.AutoCurl.Layout.Column = [2 3];
            self.AutoCurl.Text = 'Auto';

            % Create ScanDirLabel
            self.ScanDirLabel = uilabel(self.ScanDirectionGrid);
            self.ScanDirLabel.HorizontalAlignment = 'right';
            self.ScanDirLabel.Layout.Row = 1;
            self.ScanDirLabel.Layout.Column = [3 5];
            self.ScanDirLabel.Text = 'Angle';

            % Create ScanDirectionSpinner
            self.ScanDirectionSpinner = uispinner(self.ScanDirectionGrid);
            self.ScanDirectionSpinner.Step = 4;
            self.ScanDirectionSpinner.ValueChangingFcn = createCallbackFcn(self, @annular_detector_callbacks, true);
            self.ScanDirectionSpinner.Limits = [-180 180];
            self.ScanDirectionSpinner.ValueDisplayFormat = '%.2f';
            self.ScanDirectionSpinner.ValueChangedFcn = createCallbackFcn(self, @annular_detector_callbacks, true);
            self.ScanDirectionSpinner.Tag = 'ScanDir';
            self.ScanDirectionSpinner.Layout.Row = 1;
            self.ScanDirectionSpinner.Layout.Column = 6;

            % Create ScanDir_NFLabel
            self.ScanDir_NFLabel = uilabel(self.ScanDirectionGrid);
            self.ScanDir_NFLabel.Layout.Row = 1;
            self.ScanDir_NFLabel.Layout.Column = 7;
            self.ScanDir_NFLabel.Text = '°';

            % Create FlipScanDirectionY
            self.FlipScanDirectionY = uibutton(self.ScanDirectionGrid, 'state');
            self.FlipScanDirectionY.ValueChangedFcn = createCallbackFcn(self, @annular_detector_callbacks, true);
            self.FlipScanDirectionY.Tag = 'ScanDir';
            self.FlipScanDirectionY.Tooltip = {'Flip Scan Y Direction'};
            self.FlipScanDirectionY.Icon = 'axis-y.png';
            self.FlipScanDirectionY.Text = '';
            self.FlipScanDirectionY.FontWeight = 'bold';
            self.FlipScanDirectionY.Layout.Row = 1;
            self.FlipScanDirectionY.Layout.Column = 8;

            % Create ScanDirectionSlider
            self.ScanDirectionSlider = uislider(self.ScanDirectionGrid);
            self.ScanDirectionSlider.Limits = [-180 180];
            self.ScanDirectionSlider.MajorTicks = [];
            self.ScanDirectionSlider.ValueChangedFcn = createCallbackFcn(self, @annular_detector_callbacks, true);
            self.ScanDirectionSlider.ValueChangingFcn = createCallbackFcn(self, @annular_detector_callbacks, true);
            self.ScanDirectionSlider.Tag = 'ScanDir';
            self.ScanDirectionSlider.Layout.Row = 2;
            self.ScanDirectionSlider.Layout.Column = [1 8];

            % Create SegmentedDetectorPanel
            self.SegmentedDetectorPanel = uipanel(self.AnnularDetectorGrid);
            self.SegmentedDetectorPanel.BorderType = 'none';
            self.SegmentedDetectorPanel.TitlePosition = 'centertop';
            self.SegmentedDetectorPanel.Title = 'Segmented Detector Controls';
            self.SegmentedDetectorPanel.Visible = 'off';
            self.SegmentedDetectorPanel.Layout.Row = 3;
            self.SegmentedDetectorPanel.Layout.Column = 1;
            self.SegmentedDetectorPanel.FontName = 'Arial';
            self.SegmentedDetectorPanel.FontWeight = 'bold';

            % Create SegmentedDetectorGrid
            self.SegmentedDetectorGrid = uigridlayout(self.SegmentedDetectorPanel);
            self.SegmentedDetectorGrid.ColumnWidth = {44, 24, '1x', 32, 44, 32, '1x', 24};
            self.SegmentedDetectorGrid.RowHeight = {24, 1, 24, 'fit', 1};
            self.SegmentedDetectorGrid.ColumnSpacing = 4;
            self.SegmentedDetectorGrid.RowSpacing = 2;
            self.SegmentedDetectorGrid.Padding = [0 4 0 4];

            % Create SegmentsLabel
            self.SegmentsLabel = uilabel(self.SegmentedDetectorGrid);
            self.SegmentsLabel.HorizontalAlignment = 'right';
            self.SegmentsLabel.Layout.Row = [1 2];
            self.SegmentsLabel.Layout.Column = [1 2];
            self.SegmentsLabel.Text = 'Segments';

            % Create NSeg
            self.NSeg = uispinner(self.SegmentedDetectorGrid);
            self.NSeg.Limits = [2 32];
            self.NSeg.RoundFractionalValues = 'on';
            self.NSeg.ValueDisplayFormat = '%d';
            self.NSeg.ValueChangedFcn = createCallbackFcn(self, @annular_detector_callbacks, true);
            self.NSeg.Tag = 'SegDetr';
            self.NSeg.Layout.Row = [1 2];
            self.NSeg.Layout.Column = [3 4];
            self.NSeg.Value = 4;

            % Create RungsLabel
            self.RungsLabel = uilabel(self.SegmentedDetectorGrid);
            self.RungsLabel.HorizontalAlignment = 'right';
            self.RungsLabel.Layout.Row = 1;
            self.RungsLabel.Layout.Column = 5;
            self.RungsLabel.Text = 'Rungs';

            % Create NRung
            self.NRung = uispinner(self.SegmentedDetectorGrid);
            self.NRung.Limits = [1 16];
            self.NRung.RoundFractionalValues = 'on';
            self.NRung.ValueDisplayFormat = '%d';
            self.NRung.ValueChangedFcn = createCallbackFcn(self, @annular_detector_callbacks, true);
            self.NRung.Tag = 'SegDetr';
            self.NRung.Layout.Row = 1;
            self.NRung.Layout.Column = [6 7];
            self.NRung.Value = 1;

            % Create DetRotLabel
            self.DetRotLabel = uilabel(self.SegmentedDetectorGrid);
            self.DetRotLabel.HorizontalAlignment = 'right';
            self.DetRotLabel.Layout.Row = 3;
            self.DetRotLabel.Layout.Column = [1 4];
            self.DetRotLabel.Text = 'Rotation';

            % Create DetectorRotationSpinner
            self.DetectorRotationSpinner = uispinner(self.SegmentedDetectorGrid);
            self.DetectorRotationSpinner.Step = 4;
            self.DetectorRotationSpinner.ValueChangingFcn = createCallbackFcn(self, @annular_detector_callbacks, true);
            self.DetectorRotationSpinner.Limits = [-180 180];
            self.DetectorRotationSpinner.ValueDisplayFormat = '%.2f';
            self.DetectorRotationSpinner.ValueChangedFcn = createCallbackFcn(self, @annular_detector_callbacks, true);
            self.DetectorRotationSpinner.Tag = 'SegDetr';
            self.DetectorRotationSpinner.Layout.Row = [2 3];
            self.DetectorRotationSpinner.Layout.Column = [5 6];

            % Create DetRot_NFLabel
            self.DetRot_NFLabel = uilabel(self.SegmentedDetectorGrid);
            self.DetRot_NFLabel.Layout.Row = [2 3];
            self.DetRot_NFLabel.Layout.Column = 7;
            self.DetRot_NFLabel.Text = '°';

            % Create DetectorRotationSlider
            self.DetectorRotationSlider = uislider(self.SegmentedDetectorGrid);
            self.DetectorRotationSlider.Limits = [-180 180];
            self.DetectorRotationSlider.MajorTicks = [];
            self.DetectorRotationSlider.ValueChangedFcn = createCallbackFcn(self, @annular_detector_callbacks, true);
            self.DetectorRotationSlider.ValueChangingFcn = createCallbackFcn(self, @annular_detector_callbacks, true);
            self.DetectorRotationSlider.Tag = 'SegDetr';
            self.DetectorRotationSlider.Layout.Row = [4 5];
            self.DetectorRotationSlider.Layout.Column = [1 8];

            % Create AnnularStepGrid
            self.AnnularStepGrid = uigridlayout(self.AnnularDetectorGrid);
            self.AnnularStepGrid.ColumnWidth = {'1x', '4x', 60, '1x'};
            self.AnnularStepGrid.RowHeight = {24};
            self.AnnularStepGrid.ColumnSpacing = 0;
            self.AnnularStepGrid.RowSpacing = 0;
            self.AnnularStepGrid.Padding = [0 0 0 0];
            self.AnnularStepGrid.Layout.Row = 5;
            self.AnnularStepGrid.Layout.Column = 1;

            % Create AnnularIntegrationStepEditFieldLabel
            self.AnnularIntegrationStepEditFieldLabel = uilabel(self.AnnularStepGrid);
            self.AnnularIntegrationStepEditFieldLabel.WordWrap = 'on';
            self.AnnularIntegrationStepEditFieldLabel.Layout.Row = 1;
            self.AnnularIntegrationStepEditFieldLabel.Layout.Column = [1 4];
            self.AnnularIntegrationStepEditFieldLabel.Text = 'Annular Integration Step';

            % Create AnnularStep
            self.AnnularStep = uieditfield(self.AnnularStepGrid, 'numeric');
            self.AnnularStep.Limits = [1e-05 Inf];
            self.AnnularStep.ValueDisplayFormat = '%11.2f mrad';
            self.AnnularStep.ValueChangedFcn = createCallbackFcn(self, @detector_coordinates_callbacks, true);
            self.AnnularStep.Tooltip = {'Set fine/coarse step size for annular integration (in mrad). '};
            self.AnnularStep.Layout.Row = 1;
            self.AnnularStep.Layout.Column = [3 4];
            self.AnnularStep.Value = 0.5;

            % Create VirtualApertureTab
            self.VirtualApertureTab = uitab(self.ModeTabGroup);
            self.VirtualApertureTab.Title = 'Vr';

            % Create VirtualApertureGrid
            self.VirtualApertureGrid = uigridlayout(self.VirtualApertureTab);
            self.VirtualApertureGrid.ColumnWidth = {'1x'};
            self.VirtualApertureGrid.RowHeight = {'fit', 'fit', '1x'};
            self.VirtualApertureGrid.ColumnSpacing = 4;
            self.VirtualApertureGrid.RowSpacing = 4;
            self.VirtualApertureGrid.Padding = [4 4 4 4];

            % Create VirtualApertureCoordinatesPanel
            self.VirtualApertureCoordinatesPanel = uipanel(self.VirtualApertureGrid);
            self.VirtualApertureCoordinatesPanel.BorderType = 'none';
            self.VirtualApertureCoordinatesPanel.TitlePosition = 'centertop';
            self.VirtualApertureCoordinatesPanel.Title = 'Aperture Coordinates';
            self.VirtualApertureCoordinatesPanel.Layout.Row = 1;
            self.VirtualApertureCoordinatesPanel.Layout.Column = 1;
            self.VirtualApertureCoordinatesPanel.FontName = 'Arial';
            self.VirtualApertureCoordinatesPanel.FontWeight = 'bold';

            % Create VirtualApertureCoordinatesGrid
            self.VirtualApertureCoordinatesGrid = uigridlayout(self.VirtualApertureCoordinatesPanel);
            self.VirtualApertureCoordinatesGrid.ColumnWidth = {'1x', 52, 24, 80, '1x'};
            self.VirtualApertureCoordinatesGrid.RowHeight = {24, 'fit', 2, 24, 'fit', 2, 24, 'fit', 2, 24};
            self.VirtualApertureCoordinatesGrid.ColumnSpacing = 4;
            self.VirtualApertureCoordinatesGrid.RowSpacing = 2;
            self.VirtualApertureCoordinatesGrid.Padding = [0 0 0 4];

            % Create VrApRLabel
            self.VrApRLabel = uilabel(self.VirtualApertureCoordinatesGrid);
            self.VrApRLabel.HorizontalAlignment = 'right';
            self.VrApRLabel.Layout.Row = 1;
            self.VrApRLabel.Layout.Column = [2 3];
            self.VrApRLabel.Text = 'Radius';

            % Create VirtualApertureRSpinner
            self.VirtualApertureRSpinner = uispinner(self.VirtualApertureCoordinatesGrid);
            self.VirtualApertureRSpinner.Step = 0.25;
            self.VirtualApertureRSpinner.ValueChangingFcn = createCallbackFcn(self, @virtual_aperture_callbacks, true);
            self.VirtualApertureRSpinner.ValueDisplayFormat = '%.2f';
            self.VirtualApertureRSpinner.ValueChangedFcn = createCallbackFcn(self, @virtual_aperture_callbacks, true);
            self.VirtualApertureRSpinner.Layout.Row = 1;
            self.VirtualApertureRSpinner.Layout.Column = 4;

            % Create VrApR_NFLabel
            self.VrApR_NFLabel = uilabel(self.VirtualApertureCoordinatesGrid);
            self.VrApR_NFLabel.Layout.Row = 1;
            self.VrApR_NFLabel.Layout.Column = 5;
            self.VrApR_NFLabel.Text = 'mrad';

            % Create VirtualApertureR
            self.VirtualApertureR = uislider(self.VirtualApertureCoordinatesGrid);
            self.VirtualApertureR.MajorTicks = [];
            self.VirtualApertureR.ValueChangedFcn = createCallbackFcn(self, @virtual_aperture_callbacks, true);
            self.VirtualApertureR.ValueChangingFcn = createCallbackFcn(self, @virtual_aperture_callbacks, true);
            self.VirtualApertureR.Layout.Row = 2;
            self.VirtualApertureR.Layout.Column = [1 5];

            % Create VrApXLabel
            self.VrApXLabel = uilabel(self.VirtualApertureCoordinatesGrid);
            self.VrApXLabel.HorizontalAlignment = 'right';
            self.VrApXLabel.Layout.Row = 4;
            self.VrApXLabel.Layout.Column = [2 3];
            self.VrApXLabel.Text = 'X';

            % Create VirtualApertureXSpinner
            self.VirtualApertureXSpinner = uispinner(self.VirtualApertureCoordinatesGrid);
            self.VirtualApertureXSpinner.Step = 0.25;
            self.VirtualApertureXSpinner.ValueChangingFcn = createCallbackFcn(self, @virtual_aperture_callbacks, true);
            self.VirtualApertureXSpinner.ValueDisplayFormat = '%.2f';
            self.VirtualApertureXSpinner.ValueChangedFcn = createCallbackFcn(self, @virtual_aperture_callbacks, true);
            self.VirtualApertureXSpinner.Layout.Row = 4;
            self.VirtualApertureXSpinner.Layout.Column = 4;

            % Create VrApX_NFLabel
            self.VrApX_NFLabel = uilabel(self.VirtualApertureCoordinatesGrid);
            self.VrApX_NFLabel.Layout.Row = 4;
            self.VrApX_NFLabel.Layout.Column = 5;
            self.VrApX_NFLabel.Text = 'mrad';

            % Create VirtualApertureX
            self.VirtualApertureX = uislider(self.VirtualApertureCoordinatesGrid);
            self.VirtualApertureX.MajorTicks = [];
            self.VirtualApertureX.ValueChangedFcn = createCallbackFcn(self, @virtual_aperture_callbacks, true);
            self.VirtualApertureX.ValueChangingFcn = createCallbackFcn(self, @virtual_aperture_callbacks, true);
            self.VirtualApertureX.Layout.Row = 5;
            self.VirtualApertureX.Layout.Column = [1 5];

            % Create VrApYLabel
            self.VrApYLabel = uilabel(self.VirtualApertureCoordinatesGrid);
            self.VrApYLabel.HorizontalAlignment = 'right';
            self.VrApYLabel.Layout.Row = 7;
            self.VrApYLabel.Layout.Column = [2 3];
            self.VrApYLabel.Text = 'Y';

            % Create VirtualApertureYSpinner
            self.VirtualApertureYSpinner = uispinner(self.VirtualApertureCoordinatesGrid);
            self.VirtualApertureYSpinner.Step = 0.25;
            self.VirtualApertureYSpinner.ValueChangingFcn = createCallbackFcn(self, @virtual_aperture_callbacks, true);
            self.VirtualApertureYSpinner.ValueDisplayFormat = '%.2f';
            self.VirtualApertureYSpinner.ValueChangedFcn = createCallbackFcn(self, @virtual_aperture_callbacks, true);
            self.VirtualApertureYSpinner.Layout.Row = 7;
            self.VirtualApertureYSpinner.Layout.Column = 4;

            % Create VrApY_NFLabel
            self.VrApY_NFLabel = uilabel(self.VirtualApertureCoordinatesGrid);
            self.VrApY_NFLabel.Layout.Row = 7;
            self.VrApY_NFLabel.Layout.Column = 5;
            self.VrApY_NFLabel.Text = 'mrad';

            % Create VirtualApertureY
            self.VirtualApertureY = uislider(self.VirtualApertureCoordinatesGrid);
            self.VirtualApertureY.MajorTicks = [];
            self.VirtualApertureY.ValueChangedFcn = createCallbackFcn(self, @virtual_aperture_callbacks, true);
            self.VirtualApertureY.ValueChangingFcn = createCallbackFcn(self, @virtual_aperture_callbacks, true);
            self.VirtualApertureY.Layout.Row = 8;
            self.VirtualApertureY.Layout.Column = [1 5];

            % Create VirtualApertureRotationGrid
            self.VirtualApertureRotationGrid = uigridlayout(self.VirtualApertureCoordinatesGrid);
            self.VirtualApertureRotationGrid.ColumnWidth = {24, '1x', 24, 'fit', 24, '1x', 24};
            self.VirtualApertureRotationGrid.RowHeight = {24};
            self.VirtualApertureRotationGrid.ColumnSpacing = 4;
            self.VirtualApertureRotationGrid.RowSpacing = 4;
            self.VirtualApertureRotationGrid.Padding = [0 0 0 0];
            self.VirtualApertureRotationGrid.Layout.Row = 10;
            self.VirtualApertureRotationGrid.Layout.Column = [1 5];

            % Create VirtualApertureReset
            self.VirtualApertureReset = uibutton(self.VirtualApertureRotationGrid, 'push');
            self.VirtualApertureReset.ButtonPushedFcn = createCallbackFcn(self, @virtual_aperture_callbacks, true);
            self.VirtualApertureReset.Icon = 'home.png';
            self.VirtualApertureReset.FontWeight = 'bold';
            self.VirtualApertureReset.Tooltip = {'Home'};
            self.VirtualApertureReset.Layout.Row = 1;
            self.VirtualApertureReset.Layout.Column = 1;
            self.VirtualApertureReset.Text = '';

            % Create VirtualApertureRotateCCW
            self.VirtualApertureRotateCCW = uibutton(self.VirtualApertureRotationGrid, 'push');
            self.VirtualApertureRotateCCW.ButtonPushedFcn = createCallbackFcn(self, @virtual_aperture_callbacks, true);
            self.VirtualApertureRotateCCW.Icon = 'left_rotate.png';
            self.VirtualApertureRotateCCW.Layout.Row = 1;
            self.VirtualApertureRotateCCW.Layout.Column = 3;
            self.VirtualApertureRotateCCW.Text = '';

            % Create VirtualApertureRotationStep
            self.VirtualApertureRotationStep = uidropdown(self.VirtualApertureRotationGrid);
            self.VirtualApertureRotationStep.Items = {'90°', '60°', '45°', '30°', '22.5°', '10°', '5°', '2°', '1°', '0.5°', '0.25°'};
            self.VirtualApertureRotationStep.ItemsData = [90 60 45 30 22.5 10 5 2 1 0.5 0.25];
            self.VirtualApertureRotationStep.ValueChangedFcn = createCallbackFcn(self, @virtual_aperture_callbacks, true);
            self.VirtualApertureRotationStep.Layout.Row = 1;
            self.VirtualApertureRotationStep.Layout.Column = 4;
            self.VirtualApertureRotationStep.Value = 90;

            % Create VirtualApertureRotateCW
            self.VirtualApertureRotateCW = uibutton(self.VirtualApertureRotationGrid, 'push');
            self.VirtualApertureRotateCW.ButtonPushedFcn = createCallbackFcn(self, @virtual_aperture_callbacks, true);
            self.VirtualApertureRotateCW.Icon = 'right_rotate.png';
            self.VirtualApertureRotateCW.Layout.Row = 1;
            self.VirtualApertureRotateCW.Layout.Column = 5;
            self.VirtualApertureRotateCW.Text = '';

            % Create VirtualApertureInvert
            self.VirtualApertureInvert = uibutton(self.VirtualApertureRotationGrid, 'state');
            self.VirtualApertureInvert.ValueChangedFcn = createCallbackFcn(self, @virtual_aperture_callbacks, true);
            self.VirtualApertureInvert.Tooltip = {'Invert virtual aperture mask'};
            self.VirtualApertureInvert.Icon = 'invertColors.png';
            self.VirtualApertureInvert.Text = '';
            self.VirtualApertureInvert.Layout.Row = 1;
            self.VirtualApertureInvert.Layout.Column = 7;

            % Create AnnularStepGrid_2
            self.AnnularStepGrid_2 = uigridlayout(self.VirtualApertureRotationGrid);
            self.AnnularStepGrid_2.ColumnWidth = {'1x', '4x', 60, '1x'};
            self.AnnularStepGrid_2.RowHeight = {'1x'};
            self.AnnularStepGrid_2.ColumnSpacing = 0;
            self.AnnularStepGrid_2.RowSpacing = 0;
            self.AnnularStepGrid_2.Padding = [0 0 0 0];
            self.AnnularStepGrid_2.Layout.Row = 1;
            self.AnnularStepGrid_2.Layout.Column = 2;

            % Create AnnularIntegrationStepEditFieldLabel_2
            self.AnnularIntegrationStepEditFieldLabel_2 = uilabel(self.AnnularStepGrid_2);
            self.AnnularIntegrationStepEditFieldLabel_2.WordWrap = 'on';
            self.AnnularIntegrationStepEditFieldLabel_2.Layout.Row = 1;
            self.AnnularIntegrationStepEditFieldLabel_2.Layout.Column = [1 2];
            self.AnnularIntegrationStepEditFieldLabel_2.Text = 'Annular Integration Step';

            % Create AnnularStep_2
            self.AnnularStep_2 = uieditfield(self.AnnularStepGrid_2, 'numeric');
            self.AnnularStep_2.Limits = [1e-05 Inf];
            self.AnnularStep_2.ValueDisplayFormat = '%11.2f mrad';
            self.AnnularStep_2.Layout.Row = 1;
            self.AnnularStep_2.Layout.Column = [3 4];
            self.AnnularStep_2.Value = 0.5;

            % Create VirtualApertureSymmetryPanel
            self.VirtualApertureSymmetryPanel = uipanel(self.VirtualApertureGrid);
            self.VirtualApertureSymmetryPanel.BorderType = 'none';
            self.VirtualApertureSymmetryPanel.TitlePosition = 'centertop';
            self.VirtualApertureSymmetryPanel.Title = 'Symmetry Operations';
            self.VirtualApertureSymmetryPanel.Layout.Row = 2;
            self.VirtualApertureSymmetryPanel.Layout.Column = 1;
            self.VirtualApertureSymmetryPanel.FontName = 'Arial';
            self.VirtualApertureSymmetryPanel.FontWeight = 'bold';

            % Create VirtualApertureSymmetryGrid
            self.VirtualApertureSymmetryGrid = uigridlayout(self.VirtualApertureSymmetryPanel);
            self.VirtualApertureSymmetryGrid.ColumnWidth = {'1x', 'fit', 'fit', '1x'};
            self.VirtualApertureSymmetryGrid.RowHeight = {24, 'fit'};
            self.VirtualApertureSymmetryGrid.ColumnSpacing = 4;
            self.VirtualApertureSymmetryGrid.RowSpacing = 4;
            self.VirtualApertureSymmetryGrid.Padding = [0 0 0 6];

            % Create VrApSymmLabel
            self.VrApSymmLabel = uilabel(self.VirtualApertureSymmetryGrid);
            self.VrApSymmLabel.HorizontalAlignment = 'right';
            self.VrApSymmLabel.Layout.Row = 1;
            self.VrApSymmLabel.Layout.Column = 2;
            self.VrApSymmLabel.Text = 'Rotational Symmetry';

            % Create VirtualApertureSymmetry
            self.VirtualApertureSymmetry = uidropdown(self.VirtualApertureSymmetryGrid);
            self.VirtualApertureSymmetry.Items = {'1', '2', '3', '4', '6'};
            self.VirtualApertureSymmetry.ItemsData = [1 2 3 4 6];
            self.VirtualApertureSymmetry.ValueChangedFcn = createCallbackFcn(self, @virtual_aperture_callbacks, true);
            self.VirtualApertureSymmetry.Layout.Row = 1;
            self.VirtualApertureSymmetry.Layout.Column = 3;
            self.VirtualApertureSymmetry.Value = 1;

            % Create VirtualApertureMirrorGrid
            self.VirtualApertureMirrorGrid = uigridlayout(self.VirtualApertureSymmetryGrid);
            self.VirtualApertureMirrorGrid.ColumnWidth = {24, 24, 52, '1x', 80, '1x', 24};
            self.VirtualApertureMirrorGrid.RowHeight = {24, 14};
            self.VirtualApertureMirrorGrid.ColumnSpacing = 4;
            self.VirtualApertureMirrorGrid.RowSpacing = 2;
            self.VirtualApertureMirrorGrid.Padding = [0 0 0 0];
            self.VirtualApertureMirrorGrid.Layout.Row = 2;
            self.VirtualApertureMirrorGrid.Layout.Column = [1 4];

            % Create VirtualApertureMirror
            self.VirtualApertureMirror = uibutton(self.VirtualApertureMirrorGrid, 'state');
            self.VirtualApertureMirror.ValueChangedFcn = createCallbackFcn(self, @virtual_aperture_callbacks, true);
            self.VirtualApertureMirror.Tooltip = {'Mirrored'};
            self.VirtualApertureMirror.Icon = 'mirrored.png';
            self.VirtualApertureMirror.Text = '';
            self.VirtualApertureMirror.Layout.Row = 1;
            self.VirtualApertureMirror.Layout.Column = 1;

            % Create VrApMirrRotLabel
            self.VrApMirrRotLabel = uilabel(self.VirtualApertureMirrorGrid);
            self.VrApMirrRotLabel.HorizontalAlignment = 'right';
            self.VrApMirrRotLabel.Layout.Row = 1;
            self.VrApMirrRotLabel.Layout.Column = [2 4];
            self.VrApMirrRotLabel.Text = 'Mirror Rotation';

            % Create VirtualApertureMirrorRotationSpinner
            self.VirtualApertureMirrorRotationSpinner = uispinner(self.VirtualApertureMirrorGrid);
            self.VirtualApertureMirrorRotationSpinner.Step = 4;
            self.VirtualApertureMirrorRotationSpinner.ValueChangingFcn = createCallbackFcn(self, @virtual_aperture_callbacks, true);
            self.VirtualApertureMirrorRotationSpinner.Limits = [-180 180];
            self.VirtualApertureMirrorRotationSpinner.ValueDisplayFormat = '%.2f';
            self.VirtualApertureMirrorRotationSpinner.ValueChangedFcn = createCallbackFcn(self, @virtual_aperture_callbacks, true);
            self.VirtualApertureMirrorRotationSpinner.Layout.Row = 1;
            self.VirtualApertureMirrorRotationSpinner.Layout.Column = 5;

            % Create VrApMirrRot_NFLabel
            self.VrApMirrRot_NFLabel = uilabel(self.VirtualApertureMirrorGrid);
            self.VrApMirrRot_NFLabel.Layout.Row = 1;
            self.VrApMirrRot_NFLabel.Layout.Column = 6;
            self.VrApMirrRot_NFLabel.Text = '°';

            % Create VirtualApertureMirrorRotation
            self.VirtualApertureMirrorRotation = uislider(self.VirtualApertureMirrorGrid);
            self.VirtualApertureMirrorRotation.Limits = [-180 180];
            self.VirtualApertureMirrorRotation.MajorTicks = [];
            self.VirtualApertureMirrorRotation.ValueChangedFcn = createCallbackFcn(self, @virtual_aperture_callbacks, true);
            self.VirtualApertureMirrorRotation.ValueChangingFcn = createCallbackFcn(self, @virtual_aperture_callbacks, true);
            self.VirtualApertureMirrorRotation.Layout.Row = 2;
            self.VirtualApertureMirrorRotation.Layout.Column = [1 7];

            % Create CustomDetectorTab
            self.CustomDetectorTab = uitab(self.ModeTabGroup);
            self.CustomDetectorTab.Title = 'C';

            % Create CustomDetectorGrid
            self.CustomDetectorGrid = uigridlayout(self.CustomDetectorTab);
            self.CustomDetectorGrid.ColumnWidth = {'1x'};
            self.CustomDetectorGrid.RowHeight = {'fit', 'fit', '1x', '0.8x'};
            self.CustomDetectorGrid.ColumnSpacing = 4;
            self.CustomDetectorGrid.RowSpacing = 0;
            self.CustomDetectorGrid.Padding = [0 0 0 0];

            % Create CustomDetectorNewMaskGrid
            self.CustomDetectorNewMaskGrid = uigridlayout(self.CustomDetectorGrid);
            self.CustomDetectorNewMaskGrid.ColumnWidth = {'1x', 28, 28, 28, 28, 28, 28, 28, 28, '1x'};
            self.CustomDetectorNewMaskGrid.RowHeight = {28};
            self.CustomDetectorNewMaskGrid.ColumnSpacing = 2;
            self.CustomDetectorNewMaskGrid.RowSpacing = 4;
            self.CustomDetectorNewMaskGrid.Padding = [4 0 4 4];
            self.CustomDetectorNewMaskGrid.Layout.Row = 1;
            self.CustomDetectorNewMaskGrid.Layout.Column = 1;

            % Create CustomDetectorNewCircle
            self.CustomDetectorNewCircle = uibutton(self.CustomDetectorNewMaskGrid, 'push');
            self.CustomDetectorNewCircle.ButtonPushedFcn = createCallbackFcn(self, @custom_detector_callbacks, true);
            self.CustomDetectorNewCircle.Icon = 'circle.png';
            self.CustomDetectorNewCircle.Tooltip = {'Add circular mask'};
            self.CustomDetectorNewCircle.Layout.Row = 1;
            self.CustomDetectorNewCircle.Layout.Column = 2;
            self.CustomDetectorNewCircle.Text = '';

            % Create CustomDetectorNewGrid
            self.CustomDetectorNewGrid = uibutton(self.CustomDetectorNewMaskGrid, 'push');
            self.CustomDetectorNewGrid.ButtonPushedFcn = createCallbackFcn(self, @custom_detector_callbacks, true);
            self.CustomDetectorNewGrid.Icon = fullfile(pathToMLAPP, 'icons', 'grid.png');
            self.CustomDetectorNewGrid.Tooltip = {'Add grid mask'};
            self.CustomDetectorNewGrid.Layout.Row = 1;
            self.CustomDetectorNewGrid.Layout.Column = 3;
            self.CustomDetectorNewGrid.Text = '';

            % Create CustomDetectorNewBandpass
            self.CustomDetectorNewBandpass = uibutton(self.CustomDetectorNewMaskGrid, 'push');
            self.CustomDetectorNewBandpass.ButtonPushedFcn = createCallbackFcn(self, @custom_detector_callbacks, true);
            self.CustomDetectorNewBandpass.Icon = 'bandpass.png';
            self.CustomDetectorNewBandpass.Tooltip = {'Add bandpass mask'};
            self.CustomDetectorNewBandpass.Layout.Row = 1;
            self.CustomDetectorNewBandpass.Layout.Column = 5;
            self.CustomDetectorNewBandpass.Text = '';

            % Create CustomDetectorNewWedge
            self.CustomDetectorNewWedge = uibutton(self.CustomDetectorNewMaskGrid, 'push');
            self.CustomDetectorNewWedge.ButtonPushedFcn = createCallbackFcn(self, @custom_detector_callbacks, true);
            self.CustomDetectorNewWedge.Icon = 'wedge.png';
            self.CustomDetectorNewWedge.FontSize = 10;
            self.CustomDetectorNewWedge.Tooltip = {'Add wedge mask'};
            self.CustomDetectorNewWedge.Layout.Row = 1;
            self.CustomDetectorNewWedge.Layout.Column = 6;
            self.CustomDetectorNewWedge.Text = '';

            % Create CustomDetectorNewPolygon
            self.CustomDetectorNewPolygon = uibutton(self.CustomDetectorNewMaskGrid, 'push');
            self.CustomDetectorNewPolygon.ButtonPushedFcn = createCallbackFcn(self, @custom_detector_callbacks, true);
            self.CustomDetectorNewPolygon.Icon = 'poly.png';
            self.CustomDetectorNewPolygon.Tooltip = {'Add polygon mask'};
            self.CustomDetectorNewPolygon.Layout.Row = 1;
            self.CustomDetectorNewPolygon.Layout.Column = 7;
            self.CustomDetectorNewPolygon.Text = '';

            % Create CustomDetectorNewFromFile
            self.CustomDetectorNewFromFile = uibutton(self.CustomDetectorNewMaskGrid, 'push');
            self.CustomDetectorNewFromFile.ButtonPushedFcn = createCallbackFcn(self, @custom_detector_callbacks, true);
            self.CustomDetectorNewFromFile.Icon = 'openMask.png';
            self.CustomDetectorNewFromFile.Tooltip = {'Add mask from file'};
            self.CustomDetectorNewFromFile.Layout.Row = 1;
            self.CustomDetectorNewFromFile.Layout.Column = 8;
            self.CustomDetectorNewFromFile.Text = '';

            % Create CustomDetectorNewMath
            self.CustomDetectorNewMath = uibutton(self.CustomDetectorNewMaskGrid, 'push');
            self.CustomDetectorNewMath.ButtonPushedFcn = createCallbackFcn(self, @custom_detector_callbacks, true);
            self.CustomDetectorNewMath.Icon = 'math.png';
            self.CustomDetectorNewMath.Tooltip = {'Add mask from formula'};
            self.CustomDetectorNewMath.Layout.Row = 1;
            self.CustomDetectorNewMath.Layout.Column = 9;
            self.CustomDetectorNewMath.Text = '';

            % Create CustomDetectorNewGridNoCenter
            self.CustomDetectorNewGridNoCenter = uibutton(self.CustomDetectorNewMaskGrid, 'push');
            self.CustomDetectorNewGridNoCenter.ButtonPushedFcn = createCallbackFcn(self, @custom_detector_callbacks, true);
            self.CustomDetectorNewGridNoCenter.Icon = fullfile(pathToMLAPP, 'icons', 'grid_no_tb.png');
            self.CustomDetectorNewGridNoCenter.Tooltip = {'Add grid mask without including transmitted beam'};
            self.CustomDetectorNewGridNoCenter.Layout.Row = 1;
            self.CustomDetectorNewGridNoCenter.Layout.Column = 4;
            self.CustomDetectorNewGridNoCenter.Text = '';

            % Create CustomDetectorInterMaskGrid
            self.CustomDetectorInterMaskGrid = uigridlayout(self.CustomDetectorGrid);
            self.CustomDetectorInterMaskGrid.ColumnWidth = {24, '1x', 'fit', 'fit', '1x', 24};
            self.CustomDetectorInterMaskGrid.RowHeight = {24};
            self.CustomDetectorInterMaskGrid.ColumnSpacing = 4;
            self.CustomDetectorInterMaskGrid.RowSpacing = 6;
            self.CustomDetectorInterMaskGrid.Padding = [4 4 4 4];
            self.CustomDetectorInterMaskGrid.Layout.Row = 2;
            self.CustomDetectorInterMaskGrid.Layout.Column = 1;

            % Create ShowDiffractionMaskWindow
            self.ShowDiffractionMaskWindow = uibutton(self.CustomDetectorInterMaskGrid, 'push');
            self.ShowDiffractionMaskWindow.ButtonPushedFcn = createCallbackFcn(self, @show_window, true);
            self.ShowDiffractionMaskWindow.Tag = 'DiffractionMask';
            self.ShowDiffractionMaskWindow.Icon = 'Aperture.png';
            self.ShowDiffractionMaskWindow.Tooltip = {'Show Diffraction Mask Image'};
            self.ShowDiffractionMaskWindow.Layout.Row = 1;
            self.ShowDiffractionMaskWindow.Layout.Column = 1;
            self.ShowDiffractionMaskWindow.Text = '';

            % Create IntermaskLabel
            self.IntermaskLabel = uilabel(self.CustomDetectorInterMaskGrid);
            self.IntermaskLabel.HorizontalAlignment = 'right';
            self.IntermaskLabel.FontName = 'Arial';
            self.IntermaskLabel.FontWeight = 'bold';
            self.IntermaskLabel.Layout.Row = 1;
            self.IntermaskLabel.Layout.Column = 3;
            self.IntermaskLabel.Text = 'Inter-mask';

            % Create CustomDetectorInterMask
            self.CustomDetectorInterMask = uidropdown(self.CustomDetectorInterMaskGrid);
            self.CustomDetectorInterMask.Items = {'Color Mix', 'Union', 'Intersection', 'Additive', 'Current-only'};
            self.CustomDetectorInterMask.ValueChangedFcn = createCallbackFcn(self, @custom_detector_callbacks, true);
            self.CustomDetectorInterMask.Tooltip = {'Combine different custom masks as:'; 'Union, e.g. Final = A ∪ B ∪ C;'; 'Intersection, e.g. Final = A ∩ B ∩ C;'; 'Additive, e.g. Final = A*WtA + B*WtB + C*WtC;'; 'Current-only, i.e. only the selected mask.'; 'Zero-weighted masks are always ignored. Weightings have no effect in Union and Intersection. Weightings are applied unnormalised in Additive and Current-only.'};
            self.CustomDetectorInterMask.FontName = 'Arial';
            self.CustomDetectorInterMask.FontWeight = 'bold';
            self.CustomDetectorInterMask.Layout.Row = 1;
            self.CustomDetectorInterMask.Layout.Column = 4;
            self.CustomDetectorInterMask.Value = 'Color Mix';

            % Create CustomDetectorDeleteMask
            self.CustomDetectorDeleteMask = uibutton(self.CustomDetectorInterMaskGrid, 'push');
            self.CustomDetectorDeleteMask.ButtonPushedFcn = createCallbackFcn(self, @custom_detector_callbacks, true);
            self.CustomDetectorDeleteMask.Icon = 'delete.png';
            self.CustomDetectorDeleteMask.FontWeight = 'bold';
            self.CustomDetectorDeleteMask.Tooltip = {'Delete seleced mask'};
            self.CustomDetectorDeleteMask.Layout.Row = 1;
            self.CustomDetectorDeleteMask.Layout.Column = 6;
            self.CustomDetectorDeleteMask.Text = '';

            % Create CustomDetectorTable
            self.CustomDetectorTable = uitable(self.CustomDetectorGrid);
            self.CustomDetectorTable.ColumnName = {'ID'; 'Type'; 'Label'; '✅'; '👁'; 'μ'};
            self.CustomDetectorTable.RowName = {};
            self.CustomDetectorTable.ColumnSortable = [false true true false false false];
            self.CustomDetectorTable.ColumnEditable = [false false true true true true];
            self.CustomDetectorTable.RowStriping = 'off';
            self.CustomDetectorTable.CellEditCallback = createCallbackFcn(self, @custom_detector_callbacks, true);
            self.CustomDetectorTable.CellSelectionCallback = createCallbackFcn(self, @custom_detector_callbacks, true);
            self.CustomDetectorTable.Tooltip = {'✅: Enable mask.'; '👁: Show annotation on pattern.'; 'μ: Weighting.'};
            self.CustomDetectorTable.FontName = 'MS Sans Serif';
            self.CustomDetectorTable.Layout.Row = 3;
            self.CustomDetectorTable.Layout.Column = 1;

            % Create CustomDetectorDetailsPanel
            self.CustomDetectorDetailsPanel = uipanel(self.CustomDetectorGrid);
            self.CustomDetectorDetailsPanel.BorderType = 'none';
            self.CustomDetectorDetailsPanel.TitlePosition = 'centertop';
            self.CustomDetectorDetailsPanel.BackgroundColor = [1 1 1];
            self.CustomDetectorDetailsPanel.Layout.Row = 4;
            self.CustomDetectorDetailsPanel.Layout.Column = 1;
            self.CustomDetectorDetailsPanel.FontWeight = 'bold';

            % Create CustomDetectorDetailsGrid
            self.CustomDetectorDetailsGrid = uigridlayout(self.CustomDetectorDetailsPanel);
            self.CustomDetectorDetailsGrid.ColumnWidth = {24, '1x', 24};
            self.CustomDetectorDetailsGrid.RowHeight = {24, 24, 24, 24, '1x'};
            self.CustomDetectorDetailsGrid.ColumnSpacing = 1;
            self.CustomDetectorDetailsGrid.RowSpacing = 1;
            self.CustomDetectorDetailsGrid.Padding = [1 1 1 1];

            % Create CustomDetectorRotationGrid
            self.CustomDetectorRotationGrid = uigridlayout(self.CustomDetectorDetailsGrid);
            self.CustomDetectorRotationGrid.ColumnWidth = {'fit', '1x', 1, 'fit', 24, 24};
            self.CustomDetectorRotationGrid.RowHeight = {24};
            self.CustomDetectorRotationGrid.ColumnSpacing = 1;
            self.CustomDetectorRotationGrid.RowSpacing = 4;
            self.CustomDetectorRotationGrid.Padding = [0 0 0 0];
            self.CustomDetectorRotationGrid.Layout.Row = 1;
            self.CustomDetectorRotationGrid.Layout.Column = [1 3];

            % Create CDIntraCombLabel
            self.CDIntraCombLabel = uilabel(self.CustomDetectorRotationGrid);
            self.CDIntraCombLabel.HorizontalAlignment = 'center';
            self.CDIntraCombLabel.Layout.Row = 1;
            self.CDIntraCombLabel.Layout.Column = 1;
            self.CDIntraCombLabel.Text = 'Intra-mask';

            % Create CustomDetectorIntraMask
            self.CustomDetectorIntraMask = uidropdown(self.CustomDetectorRotationGrid);
            self.CustomDetectorIntraMask.Items = {'Union', 'Intersection', 'Additive'};
            self.CustomDetectorIntraMask.ValueChangedFcn = createCallbackFcn(self, @custom_detector_callbacks, true);
            self.CustomDetectorIntraMask.Tooltip = {'Combine different regions in mask as:'; 'Union, e.g. A = A1 ∪ A2 ∪ A3;'; 'Intersection, e.g. A = A1 ∩ A2 ∩ A3;'; 'Additive, e.g. A = A1 + A2 + A3.'};
            self.CustomDetectorIntraMask.Layout.Row = 1;
            self.CustomDetectorIntraMask.Layout.Column = 2;
            self.CustomDetectorIntraMask.Value = 'Union';

            % Create CustomDetectorRotationStep
            self.CustomDetectorRotationStep = uidropdown(self.CustomDetectorRotationGrid);
            self.CustomDetectorRotationStep.Items = {'180°', '90°', '60°', '45°', '30°', '22.5°', '10°', '5°', '2°', '1°', '0.5°', '0.25°'};
            self.CustomDetectorRotationStep.ItemsData = [180 90 60 45 30 22.5 10 5 2 1 0.5 0.25];
            self.CustomDetectorRotationStep.Tooltip = {'Mask rotation step size'};
            self.CustomDetectorRotationStep.Layout.Row = 1;
            self.CustomDetectorRotationStep.Layout.Column = 4;
            self.CustomDetectorRotationStep.Value = 90;

            % Create CustomDetectorRotateCCW
            self.CustomDetectorRotateCCW = uibutton(self.CustomDetectorRotationGrid, 'push');
            self.CustomDetectorRotateCCW.ButtonPushedFcn = createCallbackFcn(self, @custom_detector_callbacks, true);
            self.CustomDetectorRotateCCW.Icon = 'left_rotate.png';
            self.CustomDetectorRotateCCW.Tooltip = {'Rotate mask'};
            self.CustomDetectorRotateCCW.Layout.Row = 1;
            self.CustomDetectorRotateCCW.Layout.Column = 5;
            self.CustomDetectorRotateCCW.Text = '';

            % Create CustomDetectorRotateCW
            self.CustomDetectorRotateCW = uibutton(self.CustomDetectorRotationGrid, 'push');
            self.CustomDetectorRotateCW.ButtonPushedFcn = createCallbackFcn(self, @custom_detector_callbacks, true);
            self.CustomDetectorRotateCW.Icon = 'right_rotate.png';
            self.CustomDetectorRotateCW.Tooltip = {'Rotate mask'};
            self.CustomDetectorRotateCW.Layout.Row = 1;
            self.CustomDetectorRotateCW.Layout.Column = 6;
            self.CustomDetectorRotateCW.Text = '';

            % Create CustomDetectorMirror
            self.CustomDetectorMirror = uibutton(self.CustomDetectorDetailsGrid, 'state');
            self.CustomDetectorMirror.ValueChangedFcn = createCallbackFcn(self, @custom_detector_callbacks, true);
            self.CustomDetectorMirror.Tooltip = {'Mirrored'};
            self.CustomDetectorMirror.Icon = 'mirrored.png';
            self.CustomDetectorMirror.Text = '';
            self.CustomDetectorMirror.Layout.Row = 2;
            self.CustomDetectorMirror.Layout.Column = 1;

            % Create CustomDetectorDetailsTable
            self.CustomDetectorDetailsTable = uitable(self.CustomDetectorDetailsGrid);
            self.CustomDetectorDetailsTable.ColumnName = {'X'; 'Y'; 'R'};
            self.CustomDetectorDetailsTable.RowName = {};
            self.CustomDetectorDetailsTable.ColumnSortable = true;
            self.CustomDetectorDetailsTable.ColumnEditable = true;
            self.CustomDetectorDetailsTable.CellEditCallback = createCallbackFcn(self, @custom_detector_callbacks, true);
            self.CustomDetectorDetailsTable.Layout.Row = [2 5];
            self.CustomDetectorDetailsTable.Layout.Column = 2;

            % Create CustomDetectorInvert
            self.CustomDetectorInvert = uibutton(self.CustomDetectorDetailsGrid, 'state');
            self.CustomDetectorInvert.ValueChangedFcn = createCallbackFcn(self, @custom_detector_callbacks, true);
            self.CustomDetectorInvert.Tooltip = {'Invert mask'};
            self.CustomDetectorInvert.Icon = 'invertColors.png';
            self.CustomDetectorInvert.Text = '';
            self.CustomDetectorInvert.Layout.Row = 3;
            self.CustomDetectorInvert.Layout.Column = 1;

            % Create CustomDetectorColor
            self.CustomDetectorColor = uibutton(self.CustomDetectorDetailsGrid, 'push');
            self.CustomDetectorColor.ButtonPushedFcn = createCallbackFcn(self, @custom_detector_callbacks, true);
            self.CustomDetectorColor.Icon = 'colorPicker.png';
            self.CustomDetectorColor.Tooltip = {'Change color of current mask display'};
            self.CustomDetectorColor.Layout.Row = 4;
            self.CustomDetectorColor.Layout.Column = 1;
            self.CustomDetectorColor.Text = '';

            % Create CustomDetectorFlipHorizontal
            self.CustomDetectorFlipHorizontal = uibutton(self.CustomDetectorDetailsGrid, 'state');
            self.CustomDetectorFlipHorizontal.ValueChangedFcn = createCallbackFcn(self, @custom_detector_callbacks, true);
            self.CustomDetectorFlipHorizontal.Icon = fullfile(pathToMLAPP, 'icons', 'mirrorHorz.png');
            self.CustomDetectorFlipHorizontal.Text = '';
            self.CustomDetectorFlipHorizontal.Layout.Row = 2;
            self.CustomDetectorFlipHorizontal.Layout.Column = 3;

            % Create CustomDetectorFlipVertical
            self.CustomDetectorFlipVertical = uibutton(self.CustomDetectorDetailsGrid, 'state');
            self.CustomDetectorFlipVertical.ValueChangedFcn = createCallbackFcn(self, @custom_detector_callbacks, true);
            self.CustomDetectorFlipVertical.Icon = fullfile(pathToMLAPP, 'icons', 'mirrorVert.png');
            self.CustomDetectorFlipVertical.Text = '';
            self.CustomDetectorFlipVertical.Layout.Row = 3;
            self.CustomDetectorFlipVertical.Layout.Column = 3;

            % Create CustomDetectorTranspose
            self.CustomDetectorTranspose = uibutton(self.CustomDetectorDetailsGrid, 'state');
            self.CustomDetectorTranspose.ValueChangedFcn = createCallbackFcn(self, @custom_detector_callbacks, true);
            self.CustomDetectorTranspose.Icon = fullfile(pathToMLAPP, 'icons', 'transpose.png');
            self.CustomDetectorTranspose.Text = '';
            self.CustomDetectorTranspose.Layout.Row = 4;
            self.CustomDetectorTranspose.Layout.Column = 3;

            % Create Quant4D_FigGrid
            self.Quant4D_FigGrid = uigridlayout(self.Quant4D_Fig);
            self.Quant4D_FigGrid.ColumnWidth = {'1x'};
            self.Quant4D_FigGrid.RowHeight = {'fit', 'fit', '1x', 'fit'};
            self.Quant4D_FigGrid.ColumnSpacing = 0;
            self.Quant4D_FigGrid.RowSpacing = 0;
            self.Quant4D_FigGrid.Padding = [0 0 0 0];

            % Create ShortcutButtonGrid
            self.ShortcutButtonGrid = uigridlayout(self.Quant4D_FigGrid);
            self.ShortcutButtonGrid.ColumnWidth = {'1x', 24, 24, 24, 24, 24, 24};
            self.ShortcutButtonGrid.RowHeight = {24};
            self.ShortcutButtonGrid.ColumnSpacing = 4;
            self.ShortcutButtonGrid.RowSpacing = 4;
            self.ShortcutButtonGrid.Padding = [4 4 4 4];
            self.ShortcutButtonGrid.Layout.Row = 1;
            self.ShortcutButtonGrid.Layout.Column = 1;

            % Create ShowImportWindow
            self.ShowImportWindow = uibutton(self.ShortcutButtonGrid, 'push');
            self.ShowImportWindow.ButtonPushedFcn = createCallbackFcn(self, @import_callbacks, true);
            self.ShowImportWindow.Icon = 'import.png';
            self.ShowImportWindow.BackgroundColor = [0.702 1 0.702];
            self.ShowImportWindow.FontName = 'arial';
            self.ShowImportWindow.FontWeight = 'bold';
            self.ShowImportWindow.Tooltip = {'Import Data'};
            self.ShowImportWindow.Layout.Row = 1;
            self.ShowImportWindow.Layout.Column = 1;
            self.ShowImportWindow.Text = 'Import';

            % Create ShowSaveWindow
            self.ShowSaveWindow = uibutton(self.ShortcutButtonGrid, 'push');
            self.ShowSaveWindow.ButtonPushedFcn = createCallbackFcn(self, @save_callbacks, true);
            self.ShowSaveWindow.Icon = 'save.png';
            self.ShowSaveWindow.Tooltip = {'Open the Saving/Export window'};
            self.ShowSaveWindow.Layout.Row = 1;
            self.ShowSaveWindow.Layout.Column = 2;
            self.ShowSaveWindow.Text = '';

            % Create AutoSaveImage
            self.AutoSaveImage = uibutton(self.ShortcutButtonGrid, 'push');
            self.AutoSaveImage.ButtonPushedFcn = createCallbackFcn(self, @save_callbacks, true);
            self.AutoSaveImage.Icon = 'autoSave.png';
            self.AutoSaveImage.Tooltip = {'Repeat Previous Image Saving Operation'};
            self.AutoSaveImage.Layout.Row = 1;
            self.AutoSaveImage.Layout.Column = 3;
            self.AutoSaveImage.Text = '';

            % Create UpdateImages
            self.UpdateImages = uibutton(self.ShortcutButtonGrid, 'push');
            self.UpdateImages.ButtonPushedFcn = createCallbackFcn(self, @update_images, true);
            self.UpdateImages.Icon = 'refresh.png';
            self.UpdateImages.Tooltip = {'Update Images (F5)'};
            self.UpdateImages.Layout.Row = 1;
            self.UpdateImages.Layout.Column = 4;
            self.UpdateImages.Text = '';

            % Create ShowSettingsWindow
            self.ShowSettingsWindow = uibutton(self.ShortcutButtonGrid, 'push');
            self.ShowSettingsWindow.ButtonPushedFcn = createCallbackFcn(self, @show_window, true);
            self.ShowSettingsWindow.Tag = 'Settings';
            self.ShowSettingsWindow.Icon = fullfile(pathToMLAPP, 'icons', 'settings.png');
            self.ShowSettingsWindow.Tooltip = {'Show Detector Controls'};
            self.ShowSettingsWindow.Layout.Row = 1;
            self.ShowSettingsWindow.Layout.Column = 7;
            self.ShowSettingsWindow.Text = '';

            % Create ModeGrid
            self.ModeGrid = uigridlayout(self.Quant4D_FigGrid);
            self.ModeGrid.ColumnWidth = {'1x', 'fit', '1x'};
            self.ModeGrid.RowHeight = {24};
            self.ModeGrid.ColumnSpacing = 4;
            self.ModeGrid.RowSpacing = 4;
            self.ModeGrid.Padding = [0 0 0 0];
            self.ModeGrid.Layout.Row = 2;
            self.ModeGrid.Layout.Column = 1;

            % Create Mode
            self.Mode = uidropdown(self.ModeGrid);
            self.Mode.Items = {'Import', 'Alignment', 'Annular/Round', 'Segmented (DPC)', 'Center of Mass', 'Virtual Aperture', 'Custom Detectors'};
            self.Mode.ItemsData = {'Preview', 'Alignment', 'Annular', 'DPC', 'CoM', 'Virtual', 'Custom'};
            self.Mode.ValueChangedFcn = createCallbackFcn(self, @detector_mode_callbacks, true);
            self.Mode.Tooltip = {'Diffraction Detector Mode'};
            self.Mode.FontSize = 14;
            self.Mode.FontWeight = 'bold';
            self.Mode.Layout.Row = 1;
            self.Mode.Layout.Column = 2;
            self.Mode.Value = 'Preview';

            % Create ModePanel
            self.ModePanel = uipanel(self.Quant4D_FigGrid);
            self.ModePanel.BorderType = 'none';
            self.ModePanel.TitlePosition = 'centertop';
            self.ModePanel.Layout.Row = 3;
            self.ModePanel.Layout.Column = 1;

            % Create RealPanelGrid
            self.RealPanelGrid = uigridlayout(self.Quant4D_FigGrid);
            self.RealPanelGrid.ColumnWidth = {'1x'};
            self.RealPanelGrid.RowHeight = {'fit'};
            self.RealPanelGrid.ColumnSpacing = 4;
            self.RealPanelGrid.RowSpacing = 4;
            self.RealPanelGrid.Padding = [4 4 4 0];
            self.RealPanelGrid.Layout.Row = 4;
            self.RealPanelGrid.Layout.Column = 1;

            % Create RealPanel
            self.RealPanel = uipanel(self.RealPanelGrid);
            self.RealPanel.AutoResizeChildren = 'off';
            self.RealPanel.Tooltip = {'Real-space region of interest (ROI)'};
            self.RealPanel.BorderType = 'none';
            self.RealPanel.TitlePosition = 'centertop';
            self.RealPanel.Title = 'Real-space ROI';
            self.RealPanel.Visible = 'off';
            self.RealPanel.Layout.Row = 1;
            self.RealPanel.Layout.Column = 1;
            self.RealPanel.FontName = 'Arial';
            self.RealPanel.FontWeight = 'bold';
            self.RealPanel.FontSize = 14;

            % Create RealGrid
            self.RealGrid = uigridlayout(self.RealPanel);
            self.RealGrid.ColumnWidth = {24, '1x', 24};
            self.RealGrid.RowHeight = {24, 24};
            self.RealGrid.ColumnSpacing = 4;
            self.RealGrid.RowSpacing = 4;
            self.RealGrid.Padding = [0 0 0 4];

            % Create RealROIInvert
            self.RealROIInvert = uibutton(self.RealGrid, 'state');
            self.RealROIInvert.ValueChangedFcn = createCallbackFcn(self, @realspace_ROI_callbacks, true);
            self.RealROIInvert.Tooltip = {'Invert real-space mask'};
            self.RealROIInvert.Icon = 'invertColors.png';
            self.RealROIInvert.Text = '';
            self.RealROIInvert.Layout.Row = 1;
            self.RealROIInvert.Layout.Column = 3;

            % Create ShowRealMaskWindow
            self.ShowRealMaskWindow = uibutton(self.RealGrid, 'push');
            self.ShowRealMaskWindow.ButtonPushedFcn = createCallbackFcn(self, @show_window, true);
            self.ShowRealMaskWindow.Tag = 'RealMask';
            self.ShowRealMaskWindow.Icon = 'Aperture.png';
            self.ShowRealMaskWindow.Tooltip = {'Show Real-space Mask'};
            self.ShowRealMaskWindow.Layout.Row = 1;
            self.ShowRealMaskWindow.Layout.Column = 1;
            self.ShowRealMaskWindow.Text = '';

            % Create RealROIGrid
            self.RealROIGrid = uigridlayout(self.RealGrid);
            self.RealROIGrid.ColumnWidth = {'fit', 'fit', '1x', 'fit', '1x'};
            self.RealROIGrid.RowHeight = {24};
            self.RealROIGrid.ColumnSpacing = 4;
            self.RealROIGrid.RowSpacing = 4;
            self.RealROIGrid.Padding = [0 0 0 0];
            self.RealROIGrid.Layout.Row = 2;
            self.RealROIGrid.Layout.Column = [1 3];

            % Create RealYLabel
            self.RealYLabel = uilabel(self.RealROIGrid);
            self.RealYLabel.HorizontalAlignment = 'right';
            self.RealYLabel.Layout.Row = 1;
            self.RealYLabel.Layout.Column = 4;
            self.RealYLabel.Text = 'Y';

            % Create RealROIFrameY
            self.RealROIFrameY = uispinner(self.RealROIGrid);
            self.RealROIFrameY.ValueChangingFcn = createCallbackFcn(self, @realspace_ROI_callbacks, true);
            self.RealROIFrameY.RoundFractionalValues = 'on';
            self.RealROIFrameY.ValueDisplayFormat = '%.0f';
            self.RealROIFrameY.ValueChangedFcn = createCallbackFcn(self, @realspace_ROI_callbacks, true);
            self.RealROIFrameY.Layout.Row = 1;
            self.RealROIFrameY.Layout.Column = 5;

            % Create RealXLabel
            self.RealXLabel = uilabel(self.RealROIGrid);
            self.RealXLabel.HorizontalAlignment = 'right';
            self.RealXLabel.Layout.Row = 1;
            self.RealXLabel.Layout.Column = 2;
            self.RealXLabel.Text = 'X';

            % Create RealROIFrameX
            self.RealROIFrameX = uispinner(self.RealROIGrid);
            self.RealROIFrameX.ValueChangingFcn = createCallbackFcn(self, @realspace_ROI_callbacks, true);
            self.RealROIFrameX.RoundFractionalValues = 'on';
            self.RealROIFrameX.ValueDisplayFormat = '%.0f';
            self.RealROIFrameX.ValueChangedFcn = createCallbackFcn(self, @realspace_ROI_callbacks, true);
            self.RealROIFrameX.Layout.Row = 1;
            self.RealROIFrameX.Layout.Column = 3;

            % Create RealROIFrameLabel
            self.RealROIFrameLabel = uilabel(self.RealROIGrid);
            self.RealROIFrameLabel.HorizontalAlignment = 'right';
            self.RealROIFrameLabel.Layout.Row = 1;
            self.RealROIFrameLabel.Layout.Column = 1;
            self.RealROIFrameLabel.Text = 'Frame';

            % Create RealROIShape
            self.RealROIShape = uidropdown(self.RealGrid);
            self.RealROIShape.Items = {'Full Image', 'Point', 'Ellipse', 'Rectangle', 'Draw Polygon', 'From File'};
            self.RealROIShape.ItemsData = {'full', 'point', 'ellipse', 'rectangle', 'poly', 'file'};
            self.RealROIShape.ValueChangedFcn = createCallbackFcn(self, @realspace_ROI_callbacks, true);
            self.RealROIShape.Layout.Row = 1;
            self.RealROIShape.Layout.Column = 2;
            self.RealROIShape.Value = 'full';

            % Create diffraction_dropdown
            self.diffraction_dropdown = uidropdown(self.Quant4D_Fig);
            self.diffraction_dropdown.Items = {'sum', 'mean', 'max', 'std', 'sqrt', 'ln', 'log10'};
            self.diffraction_dropdown.Tooltip = {'Set how patterns are combined in real space. NOTE: max() and std() can be significantly slower when interactiving with a real space ROI!'};
            self.diffraction_dropdown.Position = [-161 -4 65 22];
            self.diffraction_dropdown.Value = 'sum';

            % Create DebugContextMenu
            self.DebugContextMenu = uicontextmenu(self.Quant4D_Fig);

            % Create Test1Menu
            self.Test1Menu = uimenu(self.DebugContextMenu);
            self.Test1Menu.MenuSelectedFcn = createCallbackFcn(self, @test1, true);
            self.Test1Menu.Text = 'Test1';

            % Create Test2Menu
            self.Test2Menu = uimenu(self.DebugContextMenu);
            self.Test2Menu.MenuSelectedFcn = createCallbackFcn(self, @test2, true);
            self.Test2Menu.Text = 'Test2';

            % Create SaveVecMenu
            self.SaveVecMenu = uimenu(self.DebugContextMenu);
            self.SaveVecMenu.MenuSelectedFcn = createCallbackFcn(self, @first_moment, true);
            self.SaveVecMenu.Text = 'SaveVec';

            % Create ReimportMenu
            self.ReimportMenu = uimenu(self.DebugContextMenu);
            self.ReimportMenu.MenuSelectedFcn = createCallbackFcn(self, @import_callbacks, true);
            self.ReimportMenu.Text = 'Re-import';

            % Create ResetQuant4DMenu
            self.ResetQuant4DMenu = uimenu(self.DebugContextMenu);
            self.ResetQuant4DMenu.MenuSelectedFcn = createCallbackFcn(self, @reset_Quant4D, true);
            self.ResetQuant4DMenu.Text = 'ResetQuant4D';

            % Create EnableallUIsMenu
            self.EnableallUIsMenu = uimenu(self.DebugContextMenu);
            self.EnableallUIsMenu.MenuSelectedFcn = createCallbackFcn(self, @enable_all_UI, true);
            self.EnableallUIsMenu.Text = 'Enable all UIs';
            
            % Assign self.DebugContextMenu
            self.ShowImportWindow.ContextMenu = self.DebugContextMenu;

            % Create CDDelContext
            self.CDDelContext = uicontextmenu(self.Quant4D_Fig);

            % Create CDDelResetMenu
            self.CDDelResetMenu = uimenu(self.CDDelContext);
            self.CDDelResetMenu.MenuSelectedFcn = createCallbackFcn(self, @custom_detector_callbacks, true);
            self.CDDelResetMenu.Text = 'Reset';
            
            % Assign self.CDDelContext
            self.CustomDetectorNewMaskGrid.ContextMenu = self.CDDelContext;
            self.CustomDetectorDeleteMask.ContextMenu = self.CDDelContext;

            % Show the figure after all components are created
            self.Quant4D_Fig.Visible = 'on';
        end
    end

    % App creation and deletion
    methods (Access = public)

        % Construct self
        function self = Quant4D(varargin)

            % Create UIFigure and components
            createComponents(self)

            % Register the self with App Designer
            registerApp(self, self.Quant4D_Fig)

            % Execute the startup function
            runStartupFcn(self, @(self)startup_function(self, varargin{:}))

            if nargout == 0
                clear self
            end
        end

        % Code that executes before self deletion
        function delete(self)

            % Delete UIFigure when self is deleted
            delete(self.Quant4D_Fig)
        end
    end
end