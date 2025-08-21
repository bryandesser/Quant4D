classdef Quant4D < matlab.apps.AppBase

    % Properties that correspond to app components
    properties (Access = public)
        Quant4D_Fig                   matlab.ui.Figure
        guiLayout                     matlab.ui.container.GridLayout
        inputPanel                    matlab.ui.container.Panel
        displayImagesButton           matlab.ui.control.Button
        saveImagesButton              matlab.ui.control.Button
        importDataButton              matlab.ui.control.Button
        liveUpdate                    matlab.ui.control.CheckBox
        saveButton                    matlab.ui.control.Button
        autoSaveButton                matlab.ui.control.Button
        controlPanel                  matlab.ui.container.TabGroup
        detectorsTab                  matlab.ui.container.Tab
        detectorPanel                 matlab.ui.container.Panel
        adf_inner_mrad                matlab.ui.control.Label
        adfInnerField                 matlab.ui.control.NumericEditField
        adf_outer_mrad                matlab.ui.control.Label
        adfOuterField                 matlab.ui.control.NumericEditField
        adf_inner_label               matlab.ui.control.Label
        adfInner                      matlab.ui.control.Slider
        adf_outer_label               matlab.ui.control.Label
        adfOuter                      matlab.ui.control.Slider
        adfInnerPlus                  matlab.ui.control.Button
        adfInnerMinus                 matlab.ui.control.Button
        adfOuterPlus                  matlab.ui.control.Button
        adfOuterMinus                 matlab.ui.control.Button
        linkADF                       matlab.ui.control.StateButton
        detectorTypeButtonGroup       matlab.ui.container.ButtonGroup
        dpc                           matlab.ui.control.RadioButton
        adf                           matlab.ui.control.RadioButton
        vdf                           matlab.ui.control.RadioButton
        com                           matlab.ui.control.RadioButton
        detRotPanel                   matlab.ui.container.Panel
        detRotMinus                   matlab.ui.control.Button
        det_angle_deg_3               matlab.ui.control.Label
        detAngleField                 matlab.ui.control.NumericEditField
        det_angle_label               matlab.ui.control.Label
        detAngle                      matlab.ui.control.Slider
        nseg_label                    matlab.ui.control.Label
        nseg                          matlab.ui.control.NumericEditField
        nrung_label                   matlab.ui.control.Label
        nrung                         matlab.ui.control.NumericEditField
        detRotPlus                    matlab.ui.control.Button
        detAngleReset                 matlab.ui.control.Button
        scanRotPanel                  matlab.ui.container.Panel
        scanRotMinus                  matlab.ui.control.Button
        scanRotInput                  matlab.ui.control.NumericEditField
        scanRotLabel                  matlab.ui.control.Label
        scanRotPlus                   matlab.ui.control.Button
        scanRotMirror                 matlab.ui.control.CheckBox
        ScanRotationLabel             matlab.ui.control.Label
        scanRot                       matlab.ui.control.Slider
        scanRotReset                  matlab.ui.control.Button
        alignScanRot                  matlab.ui.control.StateButton
        brightnessContrastTab         matlab.ui.container.Tab
        brightnessContrastGrid        matlab.ui.container.GridLayout
        brightnessPanel               matlab.ui.container.Panel
        BrightnessLabel               matlab.ui.control.Label
        brightness                    matlab.ui.control.Slider
        ContrastLabel                 matlab.ui.control.Label
        contrast                      matlab.ui.control.Slider
        GammaLabel                    matlab.ui.control.Label
        gamma                         matlab.ui.control.Slider
        brightnessReset               matlab.ui.control.Button
        contrastReset                 matlab.ui.control.Button
        gammaReset                    matlab.ui.control.Button
        invertColors                  matlab.ui.control.StateButton
        histLog                       matlab.ui.control.StateButton
        ImageLabel                    matlab.ui.control.Label
        ImageDropDown                 matlab.ui.control.DropDown
        ColormapLabel                 matlab.ui.control.Label
        imColormap                    matlab.ui.control.DropDown
        imStats                       matlab.ui.control.Table
        histogramPlot                 matlab.ui.control.UIAxes
        diffractionPanel              matlab.ui.container.Panel
        diffractionPanelGrid          matlab.ui.container.GridLayout
        diffControlPanel              matlab.ui.container.Panel
        diffControlGrid               matlab.ui.container.GridLayout
        dpLog                         matlab.ui.control.StateButton
        dpReset                       matlab.ui.control.Button
        dpPan                         matlab.ui.control.StateButton
        dpZoom                        matlab.ui.control.StateButton
        diffPattern                   matlab.ui.control.UIAxes
        alignmentPanel                matlab.ui.container.TabGroup
        alignmentTab                  matlab.ui.container.Tab
        alignmentTabGrid              matlab.ui.container.GridLayout
        transBeamPanel                matlab.ui.container.Panel
        trans_beam_x_label            matlab.ui.control.Label
        transBeamX                    matlab.ui.control.Slider
        trans_beam_y_label            matlab.ui.control.Label
        transBeamY                    matlab.ui.control.Slider
        trans_beam_radius_label       matlab.ui.control.Label
        transBeamRadius               matlab.ui.control.Slider
        conv_angle_label              matlab.ui.control.Label
        alpha                         matlab.ui.control.NumericEditField
        transBeamXplus                matlab.ui.control.Button
        transBeamXminus               matlab.ui.control.Button
        transBeamYplus                matlab.ui.control.Button
        transBeamYminus               matlab.ui.control.Button
        transBeamRadiusPlus           matlab.ui.control.Button
        transBeamRadiusMinus          matlab.ui.control.Button
        transBeamAlign                matlab.ui.control.StateButton
        autoAlignButton               matlab.ui.control.Button
        manualCalButton               matlab.ui.control.Button
        diffPatternGroup              matlab.ui.container.ButtonGroup
        pacbedRadio                   matlab.ui.control.RadioButton
        roiRadio                      matlab.ui.control.RadioButton
        roiButtonGroup                matlab.ui.container.ButtonGroup
        roiEllipse                    matlab.ui.control.ToggleButton
        roiRectangle                  matlab.ui.control.ToggleButton
        roiPoly                       matlab.ui.control.ToggleButton
        roiPoint                      matlab.ui.control.ToggleButton
        negativeROI                   matlab.ui.control.CheckBox
        probeX                        matlab.ui.control.Spinner
        probeY                        matlab.ui.control.Spinner
        probePosition                 matlab.ui.control.Slider
        probePositionLabel            matlab.ui.control.Label
        calibrationTab                matlab.ui.container.Tab
        calibrationTabGrid            matlab.ui.container.GridLayout
        diffractionCalibration        matlab.ui.container.ButtonGroup
        mradButton                    matlab.ui.control.ToggleButton
        invAButton                    matlab.ui.control.ToggleButton
        pixelsmradEditFieldLabel      matlab.ui.control.Label
        transCal                      matlab.ui.control.NumericEditField
        keVLabel                      matlab.ui.control.Label
        keV                           matlab.ui.control.NumericEditField
        transmittedDiskPosition       matlab.ui.container.Panel
        XEditFieldLabel               matlab.ui.control.Label
        centerX                       matlab.ui.control.NumericEditField
        centerXLabel                  matlab.ui.control.Label
        YEditFieldLabel               matlab.ui.control.Label
        centerY                       matlab.ui.control.NumericEditField
        centerYLabel                  matlab.ui.control.Label
        transmittedDiskRadius         matlab.ui.container.ButtonGroup
        transRadPix                   matlab.ui.control.ToggleButton
        transRadMrad                  matlab.ui.control.ToggleButton
        transRad                      matlab.ui.control.NumericEditField
        transRadInvA                  matlab.ui.control.ToggleButton
        editManualCalButton           matlab.ui.control.StateButton
        colorwheelTab                 matlab.ui.container.Tab
        GridLayout                    matlab.ui.container.GridLayout
        colorwheelPlot                matlab.ui.control.UIAxes
        virtualApertureTab            matlab.ui.container.Tab
        virtualApertureGrid           matlab.ui.container.GridLayout
        symmetryOperationsPanel       matlab.ui.container.Panel
        mirrorPanel                   matlab.ui.container.Panel
        apMirrorMinus                 matlab.ui.control.Button
        MirrorPlaneRotationLabel      matlab.ui.control.Label
        apMirrorAngle                 matlab.ui.control.Slider
        aperture_y_Label_2            matlab.ui.control.Label
        apMirrorInput                 matlab.ui.control.NumericEditField
        apMirrorPlus                  matlab.ui.control.Button
        apMirrorReset                 matlab.ui.control.Button
        apMirror                      matlab.ui.control.CheckBox
        apertureSymmetrySpinnerLabel  matlab.ui.control.Label
        apertureSymmetry              matlab.ui.control.Spinner
        apNegative                    matlab.ui.control.CheckBox
        apLattice                     matlab.ui.control.CheckBox
        virtualAperturePanelParent    matlab.ui.container.Panel
        coordinatesButtonGroup        matlab.ui.container.ButtonGroup
        cartesianRadio                matlab.ui.control.RadioButton
        polarRadio                    matlab.ui.control.RadioButton
        virtualAperturePanel          matlab.ui.container.Panel
        DistanceLabel                 matlab.ui.control.Label
        apX                           matlab.ui.control.Slider
        RotationLabel                 matlab.ui.control.Label
        apY                           matlab.ui.control.Slider
        apXPlus                       matlab.ui.control.Button
        apXMinus                      matlab.ui.control.Button
        apYPlus                       matlab.ui.control.Button
        apYMinus                      matlab.ui.control.Button
        apXReset                      matlab.ui.control.Button
        apYReset                      matlab.ui.control.Button
        adf_inner_mrad_2              matlab.ui.control.Label
        apXField                      matlab.ui.control.NumericEditField
        aperture_y_Label              matlab.ui.control.Label
        apYField                      matlab.ui.control.NumericEditField
        apSizePlus                    matlab.ui.control.Button
        apSizeMinus                   matlab.ui.control.Button
        SizeLabel                     matlab.ui.control.Label
        apSize                        matlab.ui.control.Slider
        adf_inner_mrad_4              matlab.ui.control.Label
        apSizeField                   matlab.ui.control.NumericEditField
        apRotAngle                    matlab.ui.control.DropDown
        apRotLeft                     matlab.ui.control.Button
        apRotRight                    matlab.ui.control.Button
        outputPanel                   matlab.ui.container.TabGroup
        bfdfTab                       matlab.ui.container.Tab
        bfdfGrid                      matlab.ui.container.GridLayout
        bfdfPlot                      matlab.ui.control.UIAxes
        comTab                        matlab.ui.container.Tab
        comGrid                       matlab.ui.container.GridLayout
        comx                          matlab.ui.control.UIAxes
        comMag                        matlab.ui.control.UIAxes
        comy                          matlab.ui.control.UIAxes
        comPhase                      matlab.ui.control.UIAxes
        comxPanel                     matlab.ui.container.Panel
        comxGrid                      matlab.ui.container.GridLayout
        comxButtonGroup               matlab.ui.container.ButtonGroup
        comx_ADF                      matlab.ui.control.ToggleButton
        comx_comx                     matlab.ui.control.ToggleButton
        comx_comMag                   matlab.ui.control.ToggleButton
        comMagPanel                   matlab.ui.container.Panel
        comMagGrid                    matlab.ui.container.GridLayout
        comMagButtonGroup             matlab.ui.container.ButtonGroup
        comMag_dcom                   matlab.ui.control.ToggleButton
        comMag_comMag                 matlab.ui.control.ToggleButton
        comMag_icom                   matlab.ui.control.ToggleButton
        comyPanel                     matlab.ui.container.Panel
        comyGrid                      matlab.ui.container.GridLayout
        comyButtonGroup               matlab.ui.container.ButtonGroup
        comy_ADF                      matlab.ui.control.ToggleButton
        comy_comy                     matlab.ui.control.ToggleButton
        comy_comPhase                 matlab.ui.control.ToggleButton
        comPhasePanel                 matlab.ui.container.Panel
        comPhaseGrid                  matlab.ui.container.GridLayout
        comPhaseButtonGroup           matlab.ui.container.ButtonGroup
        comPhase_dcom                 matlab.ui.control.ToggleButton
        comPhase_com                  matlab.ui.control.ToggleButton
        comPhase_icom                 matlab.ui.control.ToggleButton
        vectorFieldTab                matlab.ui.container.Tab
        vectorFieldGrid               matlab.ui.container.GridLayout
        vectorField                   matlab.ui.control.UIAxes
        vectorFieldPanel              matlab.ui.container.Panel
        vectorFieldPanelGrid          matlab.ui.container.GridLayout
        vectZoom                      matlab.ui.control.StateButton
        vectPan                       matlab.ui.control.StateButton
        vectReset                     matlab.ui.control.Button
        saveVecField                  matlab.ui.control.Button
        vectSubsample                 matlab.ui.control.DropDown
        vectButtonGroup               matlab.ui.container.ButtonGroup
        vectorButton                  matlab.ui.control.RadioButton
        magnitudeButton               matlab.ui.control.RadioButton
        phaseButton                   matlab.ui.control.RadioButton
    end

    
    properties (Access = public)
        annotations
        data
        imageProperties
        images
        m
        mask
        params
    end
    
    methods (Access = public)
        
        function import_bar = autoAlign(app,event,import_bar)
            import_bar.Message = sprintf('Aligning transmitted beam\nPlease Wait...');
            
            % Align transmitted beam by trying to find the transmitted disk in the PACBED pattern (app.images.pacbed),
            % apply slight gaussaian blur of 5 pixels to help the fit if necessary
            warning('off')
            [center, app.params.radius, ~] = imfindcircles(app.images.pacbed,[1 round(max(app.params.nopiy,app.params.nopix)/2)]);
            warning('on')
            if isempty([app.centerX.Value,app.centerY.Value])
                warning('off')
                [center, app.params.radius, ~] = imfindcircles(imgaussfilt(app.images.pacbed,5),[1 round(max(app.params.nopiy,app.params.nopix)/2)]);
                warning('on')
            end
            
            % Close the status bar
            close(import_bar)
            
            % Find circle closest to the center of the diffraction pattern,
            % plot for user confirmation
            
            if ~isempty(center)
                % Assign radius and center value(s) found above using
                % imfindcircles based on whichever is found to be closest
                % to the center of the diffraction pattern ([app.centerX.Value,app.centerY.Value])
                tmp_rad    = app.params.radius(sqrt(sum((center-app.params.center0).^2,2))==min(sqrt(sum((center-app.params.center0).^2,2))));
                tmp_center = center(sqrt(sum((center-app.params.center0).^2,2))==min(sqrt(sum((center-app.params.center0).^2,2))),:);
                
                % plot circle on the diffraction pattern around transmitted disk
                try delete(app.annotations.disk_edge);catch;end
                app.annotations.disk_edge = drawcircle(app.diffPattern,"Radius",tmp_rad,"Center",tmp_center,"Color",'b',"Deletable",false,"FaceAlpha",0,"Visible",true);
                
                % allow for disk as large as the entire diffraction pattern
                app.annotations.disk_edge.DrawingArea = [[app.params.nopix app.params.nopiy]*(1-sqrt(2))/2 [app.params.nopix app.params.nopiy]*sqrt(2)];
                
                % add listening functions for live updates
                app.annotations.listeners.diskMoving = addlistener(app.annotations.disk_edge,'MovingROI',@app.moveTransBeam);
                app.annotations.listeners.diskMoved = addlistener(app.annotations.disk_edge,'ROIMoved',@app.moveTransBeam);
                
                selection  = uiconfirm(app.Quant4D_Fig,'Is the transmitted beam correctly identified?',...
                                                       'Confirm transmitted beam location/size',...
                                                       'Options',{'Yes','No, Manually Align'},'DefaultOption',1);
                %'Options',{'Yes','Fine Tune','No, Manually Align'},'DefaultOption',1);
                axis(app.diffPattern,app.params.limits.dp);
                
                switch selection
                    case 'Yes' % Correct choice for transmitted beam
                        app.centerX.Value = tmp_center(1); app.centerY.Value = tmp_center(2);
                        app.params.radius = tmp_rad;
                        try app.annotations.disk_edge.Visible = false; catch;end
                        % Do a radial integration for BF/ADF images
                        import_bar = uiprogressdlg(app.Quant4D_Fig,'Title','Processing Data...','Message',sprintf('Generating radial masks... Please Wait\n'),'Indeterminate','off');
                        import_bar = integrateADF(app,import_bar);
                        
                    otherwise % Wrong choice for transmitted beam
                        app.transBeamAlign.Enable='on';
                        app.transBeamAlign.Value=1;
                        
                        % bring brightness/contrast/gamma tab to focus just in case
                        app.brightnessContrastTab.Parent = app.controlPanel;
                        app.controlPanel.SelectedTab = app.brightnessContrastTab;
                        
                        switch selection
                            case 'No, Manually Align'
                                try app.annotations.disk_edge.Visible = false; catch;end
                                axis(app.diffPattern,app.params.limits.dp);
                                % Set some initial values, these will be refined later
                                app.centerX.Value = app.params.center0(1); app.centerY.Value = app.params.center0(2); % reset transmitted disk location to the center of the diffraction pattern
                                app.params.radius = 20;          % reset transmitted disk size to 20 pixels
                            otherwise % Fine Tune
                                axis(app.diffPattern,[tmp_center(1)-2*tmp_rad tmp_center(1)+2*tmp_rad tmp_center(2)-2*tmp_rad tmp_center(2)+2*tmp_rad]);
                                app.centerX.Value = tmp_center(1); app.centerY.Value = tmp_center(2);
                                app.params.radius = tmp_rad;
                        end
                        app.params.rmax   = app.params.max_dist;
                        app.params.mrad_per_pix = app.alpha.Value/app.params.radius;
                        set(app.transBeamX,'Limits',[-app.params.rmax,app.params.rmax],'Value',0);
                        set(app.transBeamY,'Limits',[-app.params.rmax,app.params.rmax],'Value',0);
                        set(app.transBeamRadius,'Limits',[0,app.params.rmax],'Value',app.params.radius);
                        set(app.probePosition,'Limits',[1,app.params.frames]);
                        set(app.adfInner,'Limits',[0,app.params.rmax],'Value',app.params.radius);app.adfInnerField.Value=app.adfInner.Value*app.params.mrad_per_pix;
                        set(app.adfOuter,'Limits',[0,app.params.rmax],'Value',app.params.rmax/2);app.adfOuterField.Value=app.adfOuter.Value*app.params.mrad_per_pix;
                        set(app.detAngle,'Limits',[-pi,pi],'Value',app.detAngleField.Value*pi/180);app.detAngleField.Value=app.detAngle.Value*180/pi;
                        set(app.diffControlGrid.Children,'Enable','on');
                        
                        tmp.Source = app.transBeamAlign;
                        alignment(app,tmp)
                        
                        % Wait until user finishes aligning the transmitted beam
                        waitfor(app.transBeamAlign,'Value',0)
                        
                        % Reset any zoom on the transmitted beam
                        tmp.Source=app.dpReset;
                        imageControls(app,tmp)
                        
                        % Repopulate the status bar for the next part of the
                        % import process
                        import_bar = uiprogressdlg(app.Quant4D_Fig,'Title','Processing Data...','Message',sprintf('100%% Complete!\nForming Images... Please Wait'),'Indeterminate','off');
                end
            else % No transmitted beam automatically detected
                uiconfirm(app.Quant4D_Fig,'Please manually align the transmitted beam location/size','No transmitted beam automatically detected...','Options',{'OK'},'Icon','warning');
                
                app.transBeamAlign.Enable='on';
                app.transBeamAlign.Value=1;
                
                % Set some initial values, these will be refined later
                app.centerX.Value = app.params.center0(1); app.centerY.Value = app.params.center0(2); % reset transmitted disk location to the center of the diffraction pattern
                app.params.radius = 20;          % reset transmitted disk size to 20 pixels
                app.params.rmax   = app.params.max_dist;
                app.params.mrad_per_pix = app.alpha.Value/app.params.radius;
                set(app.transBeamX,'Limits',[-app.params.rmax,app.params.rmax],'Value',0);
                set(app.transBeamY,'Limits',[-app.params.rmax,app.params.rmax],'Value',0);
                set(app.transBeamRadius,'Limits',[0,app.params.rmax],'Value',app.params.radius);
                set(app.probePosition,'Limits',[1,app.params.frames]);
                set(app.adfInner,'Limits',[0,app.params.rmax],'Value',app.params.radius);app.adfInnerField.Value=app.adfInner.Value*app.params.mrad_per_pix;
                set(app.adfOuter,'Limits',[0,app.params.rmax],'Value',app.params.rmax/2);app.adfOuterField.Value=app.adfOuter.Value*app.params.mrad_per_pix;
                set(app.detAngle,'Limits',[-pi,pi],'Value',app.detAngleField.Value*pi/180);app.detAngleField.Value=app.detAngle.Value*180/pi;
                set(app.diffControlGrid.Children,'Enable','on');
                
                alignment(app,event)
                
                % Wait until user finishes aligning the transmitted beam
                waitfor(app.transBeamAlign,'Value',0)
                
                % Reset any zoom on the transmitted beam
                tmp.Source=app.dpReset;
                imageControls(app,tmp)
                
                % Repopulate the status bar for the next part of the
                % import process
                import_bar = uiprogressdlg(app.Quant4D_Fig,'Title','Processing Data...','Message',sprintf('100%% Complete!\nForming Images... Please Wait'),'Indeterminate','off');
                import_bar = integrateADF(app,import_bar);
            end

        end
        
        % Function to clear any plotted images/data
        function clearPlots(app)
            delete(findall(app.bfdfPlot,'Type','Image'));
            delete(findall(app.comMag,'Type','Image'));
            delete(findall(app.comPhase,'Type','Image'));
            delete(findall(app.comx,'Type','Image'));
            delete(findall(app.comy,'Type','Image'));
            cla(app.vectorField);
        end
        
        % Function to hide any/all plotted detectors if they exist
        function clearDetectors(app)
            % Annular/Round detectors
            try app.annotations.adfInner.Visible = 'off';catch;end
            try app.annotations.adfOuter.Visible = 'off';catch;end
            
            % Virtual apertures
            if isfield(app.annotations,'aperture')
                for ii=1:size(app.annotations.aperture,1)
                    try app.annotations.aperture(ii,1).Visible = 'off';catch;end
                end
            end
            try app.annotations.mirror_line.Visible = 'off';catch;end
            
            % Segmented detectors
            if isfield(app.annotations,'rung')
                for ii=1:size(app.annotations.rung,1)
                    try app.annotations.rung(ii,1).Visible = 'off';catch;end
                end
            end
            if isfield(app.annotations,'segment')
                for ii=1:size(app.annotations.segment,1)
                    try app.annotations.segment(ii,1).Visible = 'off';catch;end
                end
            end
            
            %scan rotation vectors and/or text
            try delete(findall(app.diffPattern,'Type','Quiver'));catch;end
            try delete(findall(app.diffPattern,'Type','Text'));catch;end
            
        end
        
        % Show the BF/DF image
        
        function displayCoM(app)
            % CoM angle is calculated from the arctangent of the difference images (CoMx and CoMy)
            app.images.comPhase = atan2(app.images.comy,app.images.comx);%-app.detAngle.Value+app.scanRot.Value;
            app.images.comPhase = app.images.comPhase .* (app.images.comPhase >= 0) + (app.images.comPhase + 2 * pi) .* (app.images.comPhase < 0); %adjust atan2 range from [-pi/2:pi/2) to [0:2pi)
            
            % CoM magnitude is the length of the vector -- in mrad
            app.images.comMag = sqrt(app.images.comx.^2+app.images.comy.^2);
            
            % Normalize com_mag range to [0:1] for alpha channel
            app.images.comMagNorm = rescale(app.images.comMag);
            
            % Make iCoM/iDPC and dCoM/dDPC images - based on maths from Lazic et al.,
            % (https://doi.org/10.1016/j.ultramic.2015.10.011)
            [k.y,k.x]=meshgrid(floor(-app.params.framesy/2):floor(-app.params.framesy/2)+app.params.framesy-1,...
                               floor(-app.params.framesx/2):floor(-app.params.framesx/2)+app.params.framesx-1);
            k.radius = sqrt(k.x.^2+k.y.^2); k.radius(k.radius==0) = 1; % a zero pixel will mess up the maths here

            k.x = fftshift(k.x);
            k.y = fftshift(k.y);
            k.radius = fftshift(k.radius);
            
            % integrated center of mass
            app.images.icom = real(ifft2(k.x.*fft2(app.images.comx)./(2*pi*1j*k.radius.^2))+...
                                   ifft2(k.y.*fft2(app.images.comy)./(2*pi*1j*k.radius.^2)));
            % differential center of mass
            app.images.dcom = real(ifft2(2*pi*1i*k.x.*fft2(app.images.comx)+2*pi*1i*k.y.*fft2(app.images.comy)));
            
            % Plot difference/com(x) images - first clear any
            % instances of 'app.comx' axis in app.imageProperties.axis
            app.imageProperties.axis(cellfun(@(c) any(strcmp(c, 'app.comx')), app.imageProperties.axis))={''};
            switch app.comxButtonGroup.SelectedObject
                case app.comx_ADF
                    % add 'app.comx' axis to the first empty column in the row corresponding to the image 'app.images.adf' in structured array 'app.imageProperties'
                    app.imageProperties.axis{strcmp(app.imageProperties.image,'app.images.adf'),find(cellfun(@(c) any(strcmp(c, '')), app.imageProperties.axis(strcmp(app.imageProperties.image,'app.images.adf'),:)),1)} = 'app.comx';
                    plotImage(app,'adf');
                case app.comx_comx
                    % add 'app.comx' axis to the first empty column in the row corresponding to the image 'app.images.comx' in structured array 'app.imageProperties'
                    app.imageProperties.axis{strcmp(app.imageProperties.image,'app.images.comx'),find(cellfun(@(c) any(strcmp(c, '')), app.imageProperties.axis(strcmp(app.imageProperties.image,'app.images.comx'),:)),1)} = 'app.comx';
                    plotImage(app,'comx');
                case app.comx_comMag
                    % add 'app.comx' axis to the first empty column in the row corresponding to the image 'app.images.comMag' in structured array 'app.imageProperties'
                    app.imageProperties.axis{strcmp(app.imageProperties.image,'app.images.comMag'),find(cellfun(@(c) any(strcmp(c, '')), app.imageProperties.axis(strcmp(app.imageProperties.image,'app.images.comMag'),:)),1)} = 'app.comx';
                    plotImage(app,'comMag');
            end

            % Plot difference/com(y) images - first clear any
            % instances of 'app.comy' axis in app.imageProperties.axis
            app.imageProperties.axis(cellfun(@(c) any(strcmp(c, 'app.comy')), app.imageProperties.axis))={''};
            switch app.comyButtonGroup.SelectedObject
                case app.comy_ADF
                    % add 'app.comy' axis to the first empty column in the row corresponding to the image 'app.images.adf' in structured array 'app.imageProperties'
                    app.imageProperties.axis{strcmp(app.imageProperties.image,'app.images.adf'),find(cellfun(@(c) any(strcmp(c, '')), app.imageProperties.axis(strcmp(app.imageProperties.image,'app.images.adf'),:)),1)} = 'app.comy';
                    plotImage(app,'adf');
                case app.comy_comy
                    % add 'app.comy' axis to the first empty column in the row corresponding to the image 'app.images.comy' in structured array 'app.imageProperties'
                    app.imageProperties.axis{strcmp(app.imageProperties.image,'app.images.comy'),find(cellfun(@(c) any(strcmp(c, '')), app.imageProperties.axis(strcmp(app.imageProperties.image,'app.images.comy'),:)),1)} = 'app.comy';
                    plotImage(app,'comy');
                case app.comy_comPhase
                    % add 'app.comy' axis to the first empty column in the row corresponding to the image 'app.images.comPhase' in structured array 'app.imageProperties'
                    app.imageProperties.axis{strcmp(app.imageProperties.image,'app.images.comPhase'),find(cellfun(@(c) any(strcmp(c, '')), app.imageProperties.axis(strcmp(app.imageProperties.image,'app.images.comPhase'),:)),1)} = 'app.comy';
                    plotImage(app,'comPhase');
            end
            
            % Plot CoM/DPC magnitude, iCom/iDPC, and dCoM/dDPC images - first clear any
            % instances of 'app.comMag' axis in app.imageProperties.axis
            app.imageProperties.axis(cellfun(@(c) any(strcmp(c, 'app.comMag')), app.imageProperties.axis))={''};
            switch app.comMagButtonGroup.SelectedObject
                case app.comMag_dcom
                    % add 'app.comMag' axis to the first empty column in the row corresponding to the image 'app.images.dcom' in structured array 'app.imageProperties'
                    app.imageProperties.axis{strcmp(app.imageProperties.image,'app.images.dcom'),find(cellfun(@(c) any(strcmp(c, '')), app.imageProperties.axis(strcmp(app.imageProperties.image,'app.images.dcom'),:)),1)} = 'app.comMag';
                    plotImage(app,'dcom');
                case app.comMag_comMag
                    % add 'app.comMag' axis to the first empty column in the row corresponding to the image 'app.images.comMag' in structured array 'app.imageProperties'
                    app.imageProperties.axis{strcmp(app.imageProperties.image,'app.images.comMag'),find(cellfun(@(c) any(strcmp(c, '')), app.imageProperties.axis(strcmp(app.imageProperties.image,'app.images.comMag'),:)),1)} = 'app.comMag';
                    plotImage(app,'comMag');
                case app.comMag_icom
                    % add 'app.comMag' axis to the first empty column in the row corresponding to the image 'app.images.icom' in structured array 'app.imageProperties'
                    app.imageProperties.axis{strcmp(app.imageProperties.image,'app.images.icom'),find(cellfun(@(c) any(strcmp(c, '')), app.imageProperties.axis(strcmp(app.imageProperties.image,'app.images.icom'),:)),1)} = 'app.comMag';
                    plotImage(app,'icom');
            end

            % Plot CoM/DPC phase, iCom/iDPC, and dCoM/dDPC images - first clear any
            % instances of 'app.comPhase' axis in app.imageProperties.axis
            app.imageProperties.axis(cellfun(@(c) any(strcmp(c, 'app.comPhase')), app.imageProperties.axis))={''};
            switch app.comPhaseButtonGroup.SelectedObject
                case app.comPhase_dcom
                    % add 'app.comPhase' axis to the first empty column in the row corresponding to the image 'app.images.dcom' in structured array 'app.imageProperties'
                    app.imageProperties.axis{strcmp(app.imageProperties.image,'app.images.dcom'),find(cellfun(@(c) any(strcmp(c, '')), app.imageProperties.axis(strcmp(app.imageProperties.image,'app.images.dcom'),:)),1)} = 'app.comPhase';
                    plotImage(app,'dcom');
                case app.comPhase_com
                    % plot the CoM/DPC vector colorized by phase and saturated by magnitude
                    delete(findall(app.comPhase,'Type','Image'));
                    app.comPhase.NextPlot='add';
                    imagesc(app.comPhase,app.images.comPhase,'AlphaData',app.images.comMagNorm);
                    colormap(app.comPhase,hsv);caxis(app.comPhase,[0 2*pi]);
                    set(app.comPhase,'DataAspectRatio',[1 1 1],'XTick',[],'Ytick',[],'YDir','reverse','Color','k','XLim',[1 app.params.framesx],'YLim',[1 app.params.framesy]);
                    set(app.comPhase,'Color','k');app.comPhase.Toolbar=app.comMag.Toolbar;
                    axis(app.comPhase,app.params.limits.im);
                case app.comPhase_icom
                    % add 'app.comPhase' axis to the first empty column in the row corresponding to the image 'app.images.icom' in structured array 'app.imageProperties'
                    app.imageProperties.axis{strcmp(app.imageProperties.image,'app.images.icom'),find(cellfun(@(c) any(strcmp(c, '')), app.imageProperties.axis(strcmp(app.imageProperties.image,'app.images.icom'),:)),1)} = 'app.comPhase';
                    plotImage(app,'icom');
            end
            
            plotVectorField(app)
            
        end
        
        function import4D(app,params_in,mem_in)
            % nopiy, nopix          -	number of pixels in the diffraction pattern
            % framesy, framesx      -	number of probe positions in the image
            % bitdepth              -   bitdepth of the dataset
            % header                -   BYTES before each diffraction pattern
            % footer                -   BYTES after each diffraction patterns
            % ordering              -   endianness (big or little)
            % gpu                   -   device selection if acceleration is enabled
            % mem.type              -   physical or virtual memory loading
            % mem.convertFloat      -   only used for integer type datasets, convert int to float
            
            app.params.nopiy        = params_in.nopiy;
            app.params.nopix        = params_in.nopix;
            app.params.framesy      = params_in.framesy;
            app.params.framesx      = params_in.framesx;
            app.params.header       = params_in.header;
            app.params.footer       = params_in.footer;
            app.params.ordering     = params_in.ordering;
            app.params.bitdepth     = params_in.bitdepth{:};
            app.params.gpu          = params_in.gpu;
            app.params.mem          = mem_in.type;
            app.params.convertFloat = mem_in.convertFloat;
            
            if app.params.gpu > 0
                app.params.device = gpuDevice(app.params.gpu);
            end
            
            % figure out number of bytes per element
            tmp = ones(1,1,app.params.bitdepth);
            app.params.bytesize = whos('tmp').bytes;
            
        end
        
        function import_bar = integrateADF(app,import_bar)
            % Make pixel array for mask
            [xgrid, ygrid] = meshgrid(1:app.params.nopix,1:app.params.nopiy);
            if app.params.gpu>0
                xgrid = gpuArray(xgrid);
                ygrid = gpuArray(ygrid);
            end
            
            % Find pixel farthest from center of transmitted disk
            app.params.max_dist=gather(floor(max(max(sqrt((xgrid-app.centerX.Value).^2+(ygrid-app.centerY.Value).^2)))*2)/2);
            
            % Integrate in 0.5 pixel increments all the way out to the furthest corner
            import_bar.Indeterminate = 'on';
            import_bar.Message = 'Generating radial masks... Please Wait';
            dist = 0:0.5:app.params.max_dist;
            app.mask.adf = sqrt((xgrid-app.centerX.Value).^2 + (ygrid-app.centerY.Value).^2);
            app.mask.adf = permute(bsxfun(@and,bsxfun(@ge,app.mask.adf(:),dist),bsxfun(@lt,app.mask.adf(:),dist+0.5)),[2 1]);
            
            % Multiply data by the ADF masks
            import_bar.Message = sprintf('Performing radial integration... Please Wait\n');
            % Matlab does not implement mtimes() for integer class arrays,
            % so check if it is an integer. If it is an integer class array
            % (i.e. Medipix data), check if it should be multiplied as
            % single or double precision float
            if isinteger(app.data) && app.params.bytesize<=4 % int32/uint32 (or less) data
                app.images.annular = permute(reshape(app.mask.adf*single(app.data),[size(dist,2) app.params.framesx app.params.framesy]),[2 3 1]);
            elseif isinteger(app.data) && app.params.bytesize>4 % int64/uint64 data
                app.images.annular = permute(reshape(app.mask.adf*double(app.data),[size(dist,2) app.params.framesx app.params.framesy]),[2 3 1]);
            else % floating point data
                app.images.annular = permute(reshape(app.mask.adf*app.data,[size(dist,2) app.params.framesx app.params.framesy]),[2 3 1]);
            end
            
        end
        
        function integrateMasks(app)
            % Make pixel array for masks
            [ygrid, xgrid] = meshgrid(1:app.params.nopix,1:app.params.nopiy);
            
            % move to GPU if selected
            if app.params.gpu>0
                xgrid = gpuArray(xgrid);ygrid=gpuArray(ygrid);
            end
            
            % switch between detector types (except annular/round)
            switch app.detectorTypeButtonGroup.SelectedObject
                case app.com
                    % Mask off diffraction pattern
                    app.mask.sum = ((xgrid-app.centerX.Value).^2 + (ygrid-app.centerY.Value).^2) <= app.adfOuter.Value^2 & ... % less than outer angle
                                   ((xgrid-app.centerX.Value).^2 + (ygrid-app.centerY.Value).^2) >= app.adfInner.Value^2;      % greater than inner angle
                    app.mask.sum = app.mask.sum(:);
                    xgrid = xgrid(:).*app.mask.sum;ygrid = ygrid(:).*app.mask.sum;
                    
                    % Set up a pixel grid
                    app.images.com = zeros([size(app.data,2),2],app.params.bitdepth);
                    if app.params.gpu>0
                        app.images.com = gpuArray(app.images.com);
                    end
                    
                    % Adjust for scan rotation
                    R = [cos(app.scanRot.Value) -sin(app.scanRot.Value); sin(app.scanRot.Value) cos(app.scanRot.Value)];

                    % Integrated mass of each diffraction pattern within the mask:
                    % Center of Mass adjusted to the center of the diffraction pattern
                    % Matlab does not implement mtimes() for integer class arrays,
                    % so check if it is an integer. If it is an integer class array
                    % (i.e. Medipix data), check if it should be multiplied as
                    % single or double precision float
                    if isinteger(app.data) && app.params.bytesize<=4 % int32/uint32 (or less) data
                        app.images.com(:,1) = single(xgrid'*single(app.data)./(app.mask.sum'*single(app.data))-app.centerX.Value);
                        app.images.com(:,2) = single(ygrid'*single(app.data)./(app.mask.sum'*single(app.data))-app.centerY.Value);
                        app.images.com = single(app.images.com);
                    elseif isinteger(app.data) && app.params.bytesize>4 % int64/uint64 data
                        app.images.com(:,1) = double(xgrid'*double(app.data)./(app.mask.sum'*double(app.data))-app.centerX.Value);
                        app.images.com(:,2) = double(ygrid'*double(app.data)./(app.mask.sum'*double(app.data))-app.centerY.Value);
                        app.images.com = double(app.images.com);
                    else % floating point data
                        app.images.com(:,1) = xgrid'*app.data./(app.mask.sum'*app.data)-app.centerX.Value;
                        app.images.com(:,2) = ygrid'*app.data./(app.mask.sum'*app.data)-app.centerY.Value;
                    end
                    
                    % if scan rotation is mirrored, add a negative to the y-coordinates
                    if app.scanRotMirror.Value
                        app.images.com(:,2) = -app.images.com(:,2);
                    end
                    
                    app.images.com = app.images.com*R;
                    
                    % CoM components
                    app.images.comx = reshape(app.images.com(:,1),[app.params.framesx app.params.framesy])*app.params.mrad_per_pix;
                    app.images.comy = reshape(app.images.com(:,2),[app.params.framesx app.params.framesy])*app.params.mrad_per_pix;
                    
                case app.dpc
                    xgrid = xgrid(:);
                    ygrid = ygrid(:);
                    
                    % Calculate the atan of all pixel positions within the image
                    a = atan2(ygrid-app.centerY.Value,xgrid-app.centerX.Value);     % Get atan from -pi to pi
                    a = a - app.detAngle.Value;                                    % subtract off any detector rotation applied
                    a = a + pi/app.nseg.Value;                                      % shift atan by half of a segment span
                    a = a .* (a >= 0) + (a + 2 * pi) .* (a < 0);                    % shift the negative values of atan up by 2pi
                    a = a .* (a<2*pi) + (a-2*pi) .* (a>=2*pi);                      % Get total range of atan from [0,2pi)
                    
                    % Preallocate a DPC/COM vector image that will be the sum of all segments (i.e. DPC_A, DPC_B, ...)
                    if app.params.gpu>0
                        app.images.com=zeros(app.params.framesy,app.params.framesx,2,app.params.bitdepth,'gpuArray');
                        com_length = zeros(app.nrung.Value*app.nseg.Value,2,app.params.bitdepth,'gpuArray');
                        app.mask.all = zeros(app.nrung.Value*app.nseg.Value,app.params.nopix*app.params.nopiy,'logical','gpuArray');
                    else
                        app.images.com=zeros(app.params.framesy,app.params.framesx,2,app.params.bitdepth);
                        com_length = zeros(app.nrung.Value*app.nseg.Value,2,app.params.bitdepth);
                        app.mask.all = zeros(app.nrung.Value*app.nseg.Value,app.params.nopix*app.params.nopiy,'logical');
                    end
                    
                    for j=1:app.nrung.Value
                        for i=1:app.nseg.Value
                            % Define vectors k1 and k2 that correspond to the inner and outer angles of the detector for a given number of rungs
                            k1=(j-1)*(app.adfOuter.Value-app.adfInner.Value)/app.nrung.Value+app.adfInner.Value;
                            k2=(j)*(app.adfOuter.Value-app.adfInner.Value)/app.nrung.Value+app.adfInner.Value;
                            
                            app.mask.all(app.nseg.Value*(j-1)+i,:)=((xgrid-app.centerX.Value).^2 + (ygrid-app.centerY.Value).^2) < k2^2 & ...   % less than outer angle
                                                                   ((xgrid-app.centerX.Value).^2 + (ygrid-app.centerY.Value).^2) >= k1^2 & ...  % greater than/equal to inner angle
                                                                   a >= (i-1)*2*pi/app.nseg.Value & ...                                         % greater than the start of the segment angle
                                                                   a <  (i)*2*pi/app.nseg.Value;                                                % less than the end of the segmenet angle
                            
                            % Adjust for scan and detector rotation, if present
                            Rscan = [cos(-app.scanRot.Value) -sin(-app.scanRot.Value); sin(-app.scanRot.Value) cos(-app.scanRot.Value)];
                            Rdet = [cos(app.detAngle.Value) -sin(app.detAngle.Value); sin(app.detAngle.Value) cos(app.detAngle.Value)];
                            
                            % Find center of mass of each segment in each rung
                            com_length(app.nseg.Value*(j-1)+i,:) = 2*sin(2*pi/app.nseg.Value/2)/(3*2*pi/app.nseg.Value/2)*(k1^3-k2^3)/(k1^2-k2^2)*...
                                                                    [cos((i-1)*2*pi/app.nseg.Value+app.detAngle.Value),...
                                                                     sin((i-1)*2*pi/app.nseg.Value+app.detAngle.Value)]*Rscan*Rdet;
                        end
                    end
                    
                    % if scan rotation is mirrored, add a negative to the y-coordinates
                    if app.scanRotMirror.Value
                        com_length(:,2) = -com_length(:,2);
                    end
                    
                    app.mask.sum = sum(app.mask.all,1);
                                        
                    % integrated mass of each diffraction pattern within the mask:
                    % Matlab does not implement mtimes() for integer class arrays,
                    % so check if it is an integer. If it is an integer class array
                    % (i.e. Medipix data), check if it should be multiplied as
                    % single or double precision float
                    if isinteger(app.data) && app.params.bytesize<=4 % int32/uint32 (or less) data
                        app.images.com = reshape(permute(single(app.mask.all)*single(app.data)./(app.mask.sum*single(app.data)),[2 1])*single(com_length),[app.params.framesx app.params.framesy 2]);
                    elseif isinteger(app.data) && app.params.bytesize>4 % int64/uint64 data
                        app.images.com = reshape(permute(double(app.mask.all)*double(app.data)./(app.mask.sum*double(app.data)),[2 1])*double(com_length),[app.params.framesx app.params.framesy 2]);
                    else % floating point data
                        app.images.com = reshape(permute(app.mask.all*(app.data)./(app.mask.sum*(app.data)),[2 1])*com_length,[app.params.framesx app.params.framesy 2]);
                    end
                    
                    % pull out horizontal (x) and vertical (y) components
                    % of the CoM and convert to mrad
                    app.images.comx = app.images.com(:,:,1)*app.params.mrad_per_pix;
                    app.images.comy = app.images.com(:,:,2)*app.params.mrad_per_pix;
                    
            end
        end
        
        function output = mrad2invA(app,input,type)
            % calculate wavevector for a given accelerating voltage - app.keV
            c1  = 9.78475598e-07;
            c2  = 12.2642596;
            ak1 = sqrt((app.keV.Value*1000)+c1*(app.keV.Value*1000)^2)/c2;
            
            switch type
                case 'mrad'
                    output=tan(input/1000)*ak1;
                case 'invA'
                    output=1000*atan(input/ak1);
            end
        end

        
        % Plot the selected detector over top of the PACBED pattern (or
        % individual diffraction patterns)
        function plotDetector(app,event)
            clearDetectors(app);
            switch app.detectorTypeButtonGroup.SelectedObject
                case app.vdf % 'virtual Aperture'
                    drawApertures(app,event);
                    moveApertures(app,event.Source,event);
                    
                otherwise % 'Segmented', 'Center of Mass', or 'Annular/Round'
                    drawDetectors(app);
                    moveDetectors(app,event.Source,event);
            end
           
        end
        
        % Generic function for plotting an image on a given axis with
        % brightness/contrast/gamma values
        function plotImage(app,imageName)
            % Define brightness, contrast, and gamma values for current image
            brightness = app.imageProperties(imageName,:).brightness; %#ok<*ADPROPLC> 
            contrast   = app.imageProperties(imageName,:).contrast;
            gamma      = app.imageProperties(imageName,:).gamma;
            
            % loop over any/all axes this image should be displayed on
            for ii=1:sum(~strcmp(app.imageProperties(imageName,:).axis,''))
                ax = eval(app.imageProperties(imageName,:).axis{ii});
                ax_limits=axis(ax);
                im = eval(app.imageProperties(imageName,:).image{:});
                
                % clear any images already on 'ax' and replot the updated image
                delete(findall(ax,'Type','Image'));
                set(ax,"NextPlot",'add');
                imagesc(ax,imadjust(rescale(im),[],[],gamma)*range(im(:))+min(im(:)));
                set(ax,'DataAspectRatio',[1 1 1],'XTick',[],'Ytick',[],'YDir','reverse');
                axis(ax,ax_limits);
                
                % setup custom toolbar
                axtoolbar(ax,{'zoomin','zoomout','pan'});
                app.params.restoreView = axtoolbarbtn(ax.Toolbar,'push');
                app.params.restoreView.Icon = 'restoreView.png';
                app.params.restoreView.Tooltip = 'Restore original view';
                app.params.restoreView.ButtonPushedFcn = @app.restoreView;
                
                if app.imageProperties(imageName,:).inverted
                    colormap(ax,flipud(eval(app.imageProperties(imageName,:).colormap{:})));
                else
                    colormap(ax,app.imageProperties(imageName,:).colormap{:});
                end
                
                
                switch imageName
                    case 'comPhase'
                        caxis(ax,[0 2*pi]);set(ax,'Color','k');
                    otherwise                        
                        % Change intensity limits on selected image based on
                        % brightness and contrast values
                        try
                            set(ax,'CLim',gather([min(im(:)) max(im(:))]-...
                                                 brightness*range(im(:))-...
                                                 contrast*range(im(:))*[-1 1]));
                        catch
                            if numel(im(:))~=sum(isnan(im(:)))
                                set(ax,'CLim',gather(mean(im(:))+[-1 1]));
                            else
                                set(ax,'CLim',[-1 1]);
                            end
                        end
                end
            end
            
            % log intensity on the diffraction pattern?
            if app.dpLog.Value
                set(app.diffPattern,'ColorScale','log');
                % To account for any negative values in the diffraction
                % pattern while in log scale
                if app.diffPattern.CLim(2)<1e-7 app.diffPattern.CLim(2)=1e-7;end
                if app.diffPattern.CLim(1)<=0 app.diffPattern.CLim(1)=1e-8; end
            else
                set(app.diffPattern,'ColorScale','linear');
            end
        end
        
        % Function to plot a vector field image over top of the DPC or COM
        % images (either magnitude, angle, or combination)
        function plotVectorField(app)
            ax_limits = axis(app.vectorField);
            delete(findall(app.vectorField,'Type','Image'));
            switch app.vectButtonGroup.SelectedObject
                case app.vectorButton
                    imagesc(app.vectorField,app.images.comPhase,'AlphaData',app.images.comMagNorm);
                    set(app.vectorField,'DataAspectRatio',[1 1 1],'XTick',[],'Ytick',[],'YDir','reverse','Color','k');
                    colormap(app.vectorField,hsv);
                    app.params.vectColor = 'w';
                case app.phaseButton
                    imagesc(app.vectorField,app.images.comPhase);
                    set(app.vectorField,'DataAspectRatio',[1 1 1],'XTick',[],'Ytick',[],'YDir','reverse','Color','k');
                    colormap(app.vectorField,hsv);
                    app.params.vectColor = 'w';
                case app.magnitudeButton
                    imagesc(app.vectorField,app.images.comMag);
                    set(app.vectorField,'DataAspectRatio',[1 1 1],'XTick',[],'Ytick',[],'YDir','reverse');
                    colormap(app.vectorField,gray);
                    app.params.vectColor = 'r';
            end
            
            % Plot vector arrows over the selected image
            try delete(app.annotations.vectors);delete(get(app.annotations.vectors,'Children'));catch;end
            set(app.vectorField,'NextPlot','add');
            app.annotations.vectors=quiver(1:app.params.subsample:app.params.framesy,...
                                           1:app.params.subsample:app.params.framesx,...
                                           app.images.comx(1:app.params.subsample:end,1:app.params.subsample:end)./app.params.subsample,...
                                           app.images.comy(1:app.params.subsample:end,1:app.params.subsample:end)./app.params.subsample,...
                                           1/app.params.subsample,app.params.vectColor,'Parent', app.vectorField);%'LineWidth',2,
            set(app.vectorField,'DataAspectRatio',[1 1 1],'XTick',[],'Ytick',[],'YDir','reverse','NextPlot','replace');
            axis(app.vectorField,ax_limits);
            caxis(app.vectorField,[0 2*pi]);
        end
        
        function import_bar = readFile(app,import_bar)
            % Set the framesize for the importbar
            framesize=app.params.nopix*app.params.nopiy*app.params.bytesize;
            
            switch app.params.mem
                case 'p' % read data into physical memory
                    % Open the user-selected file for reading
                    fid=fopen(app.params.filename,'r');
                    
                    % Pre-allocate the array for speed
                    app.data=zeros(app.params.nopiy*app.params.nopix,app.params.frames,app.params.bitdepth);
                    
                    % Read in the 4D dataset in bunches the size of one diffraction pattern and
                    % loop over the total number of diffraction patterns (# of probe positions)
                    import_bar.Indeterminate = 'off';
                    
                    for j=1:app.params.frames
                        if mod(j,100)==0 tic; end %#ok<*SEPEX>
                        if contains(app.params.filename,{'.mrc','.dm4'},'IgnoreCase',1) % .mrc and .dm4 files have a single header offset at the beginning of the file
                            if j==1
                                %fread(fid,1024,'*int8',0,'l');
                                fread(fid,app.params.header,'*int8',0,'l');
                            end
                            app.data(1:app.params.nopiy*app.params.nopix,j)=fread(fid,app.params.nopiy*app.params.nopix,app.params.bitdepth,0,app.params.ordering);
                        else
                            fread(fid,app.params.header,app.params.bitdepth,0,app.params.ordering);
                            app.data(1:app.params.nopiy*app.params.nopix,j)=fread(fid,app.params.nopiy*app.params.nopix,app.params.bitdepth,0,app.params.ordering);
                            fread(fid,app.params.footer,app.params.bitdepth,0,app.params.ordering);
                        end
                        
                        if mod(j,100)==0
                            import_bar.Value = j/app.params.frames;
                            import_bar.Message = sprintf('%.1f%% Complete\n%6.2f MB/s \t %02.0f:%02.0f',100*j/app.params.frames,framesize/toc/1e6,floor(toc(app.params.timer)/60),toc(app.params.timer)-floor(toc(app.params.timer)/60)*60);
                        end
                    end
                    fclose(fid);
                case 'v' % Virtual memory mapping
                    % Create a memory mapped file, rather than reading the file
                    % directly into memory
                    
                    import_bar.Indeterminate = 'off';
                    if app.params.header == 0 && app.params.footer == 0
                        app.m = memmapfile(app.params.filename,'Format',app.params.bitdepth);
                        app.data=reshape(app.m.Data,[app.params.nopiy*app.params.nopix app.params.frames]);
                    elseif contains(app.params.filename,{'.mrc','.dm4'},'IgnoreCase',1) % .mrc and .dm4 files only have a single header offset at the beginning of the file
                        app.m = memmapfile(app.params.filename,'Format',{app.params.bitdepth,[app.params.nopix*app.params.nopiy app.params.frames],'data'},'Offset',app.params.header,'Repeat',1);
                        app.data=reshape(app.m.Data.data,[app.params.nopiy*app.params.nopix app.params.frames]);
                    else
                        app.m = memmapfile(app.params.filename,'Format',app.params.bitdepth);
                        for j=1:app.params.frames
                            if mod(j,100)==0 tic; end
                            start  = (j-1)*app.params.nopiy*app.params.nopix + (j-1)*(app.params.header+app.params.footer) + app.params.header + 1;
                            finish = start+app.params.nopiy*app.params.nopix-1;
                            app.data(:,j)=app.m.Data(start:finish);
                            if mod(j,100)==0
                                import_bar.Value = j/app.params.frames;
                                import_bar.Message = sprintf('%.1f%% Complete\n%.2f MB/s \t %02.0f:%02.0f',100*j/app.params.frames,framesize/toc/1e6,floor(toc(app.params.timer)/60),toc(app.params.timer)-floor(toc(app.params.timer)/60)*60);
                            end
                        end
                    end
                    
                    % Check the endianness of the data vs that of the
                    % computer, perform a byteswap if necessary
                    [~,~,endian] = computer;
                    if ~strcmpi(endian,app.params.ordering)
                        app.data = swapbytes(app.data);
                    end
                    
                otherwise
                    return;
            end
            
            % convert int=>float if selected
            if app.params.convertFloat
                switch app.params.bytesize
                    case 8
                        app.data = double(app.data);
                        app.params.bytesize = 8;
                        app.params.bitdepth = 'double';
                    otherwise
                        app.data = single(app.data);
                        app.params.bytesize = 4;
                        app.params.bitdepth = 'single';
                end
            end
            
            
            % move to GPU device if selected
            if app.params.gpu>0
                app.data = gpuArray(app.data);
            end
        end
        
        function resetGui(app)
            app.liveUpdate.Enable='off';
            app.transBeamAlign.Text='Align Transmitted Beam';app.transBeamAlign.Value=0;
            app.alignScanRot.Enable='off';
            app.displayImagesButton.Enable='off';
            app.saveImagesButton.Enable='off';
            set(app.detectorTypeButtonGroup.Children,'Enable','off');
            app.saveImagesButton.Visible=1;
            app.saveButton.Visible=0;app.saveButton.Enable=0;
            app.autoSaveButton.Visible=0;app.autoSaveButton.Enable=0;
            app.Quant4D_Fig.Name = 'Quant4D';
            
            % Default to the detector panel
            app.controlPanel.SelectedTab=app.detectorsTab;
            
            % Remove all data from GPU if in use
            try
                if app.params.gpu>0
                    reset(app.params.device);
                end
            catch
            end
            
            % delete previous pacbedROI if it exists
            try delete(app.annotations.bfdfROI);catch;end
            try delete(app.annotations.comxROI);catch;end
            try delete(app.annotations.comyROI);catch;end
            try delete(app.annotations.comMagROI);catch;end
            try delete(app.annotations.comPhaseROI);catch;end
            
            % Clear any previous images
            clearPlots(app);
            
            % Hide panels that are not in use (default to annular/round
            % detector geometry)
            app.comTab.Parent=[];
            app.vectorFieldTab.Parent=[];
            app.virtualApertureTab.Parent=[];
            app.colorwheelTab.Parent=[];cla(app.colorwheelPlot);
            app.calibrationTab.Parent=[];
            app.brightnessContrastTab.Parent=[];
            
            % Clear any previous data
            app.annotations=[];
            app.data=[];
            app.imageProperties=[];
            app.images=[];
            app.m=[];
            app.mask=[];
            app.params=[];
            
            % Structured array including the different images (1), their
            % respective axes (2), variables (3), brightness (4), contrast
            % (5), gamma (6), colormap (7), and if the colormap is inverted.
            % The user can change these using the
            % 'Brightness/Contrast' tab. Axis has up to 3 positions to
            % allow for the same image to be shown on multiple axes (i.e.
            % the ADF image can be shown up to 3 times simultaneously, and
            % CoM mag can be shown up to 2 times).
            app.imageProperties = table({'app.images.adf';'app.images.annular';'app.images.colorwheel';'app.images.com';'app.images.comMag';'app.images.comMagNorm';'app.images.comPhase';'app.images.comx';'app.images.comy';'app.images.dcom';'app.images.icom';'app.images.pacbed'},...
                                        {'app.bfdfPlot','','';'','','';'app.colorWheelPlot','','';'','','';'app.comMag','','';'','','';'app.comPhase','','';'app.comx','','';'app.comy','','';'','','';'','','';'app.diffPattern','',''},...
                                        zeros(12,1),...
                                        zeros(12,1),...
                                        ones(12,1),...
                                        {'gray';'';'hsv';'';'gray';'';'hsv';'gray';'gray';'gray';'gray';'gray'},...
                                        zeros(12,1),...
                                        'RowNames',{'adf';'annular';'colorWheel';'com';'comMag';'comMagNorm';'comPhase';'comx';'comy';'dcom';'icom';'pacbed'},...
                                        'VariableNames',{'image';'axis';'brightness';'contrast';'gamma';'colormap';'inverted'});
            app.ImageDropDown.Value = 'pacbed';
            
           
            % Set some default values, limits, and colors
            app.nseg.Value=4;app.nrung.Value = 1;
            app.detAngle.Value=0;app.detAngleField.Value=0;
            app.scanRot.Value=0;app.scanRotInput.Value=0;
            set(app.detAngle,'Limits',[-pi pi],'Value',0);app.detAngleField.Value=0;
            app.probeX.Value=1;app.probeY.Value=1;
            app.probePosition.Value=1;
            app.params.subsample=1;
            app.params.vectColor = 'w';
            app.scanRot.Value=0;
            app.scanRotInput.Value=0;
            app.dpLog.Value=0;
            app.apertureSymmetry.Value = 1;
            app.polarRadio.Value = 1;
            app.pacbedRadio.Value = 1;
            app.apNegative.Value = 0;
            app.negativeROI.Value = 0;
            app.apX.Value = 0;
            app.apY.Value = 0;
            app.apMirrorAngle.Value = 0;
            app.apMirrorInput.Value = 0;
            app.apertureSymmetry.Value = 1;
            app.apMirror.Value = 0;
            app.apNegative.Value = 0;
            
            % set CoM/DPC panel
            app.comx_comx.Value = 1;
            app.comy_comy.Value = 1;
            app.comMag_comMag.Value = 1;
            app.comPhase_com.Value = 1;
            
            % Initial save image preferences
            app.params.savePrefs.prefix = '';
            app.params.savePrefs.InnerAngleCheckBox.Value = 1;
            app.params.savePrefs.OuterAngleCheckBox.Value = 1;
            app.params.savePrefs.SaveAllCheckBox.Value = 0;
            app.params.savePrefs.previous_list = 1;
            app.params.savePrefs.autosave = 0;
            
            % Start the GUI with all options disabled to force user to
            % select the "Import Dataset" button
            set(app.transBeamPanel.Children,'Enable','off');
            set(app.diffControlGrid.Children,'Enable','off');
            set(app.detectorPanel.Children,'Enable','off');
            app.pacbedRadio.Enable='off';app.roiRadio.Enable='off';
            app.transBeamAlign.Enable='off';
            app.adf.Value=1;
            app.pacbedRadio.Value=1;
            app.probePosition.Visible='off';app.probePositionLabel.Visible='off';
            app.probeX.Visible='off';app.probeY.Visible='off';
        end
        
        function saveImagePrefs(app,prefix_in,innerBox_in,outerBox_in,saveAllBox_in,selection_in)
            app.params.savePrefs.prefix = prefix_in;
            app.params.savePrefs.InnerAngleCheckBox.Value = innerBox_in;
            app.params.savePrefs.OuterAngleCheckBox.Value = outerBox_in;
            app.params.savePrefs.SaveAllCheckBox.Value = saveAllBox_in;
            app.params.savePrefs.previous_list = selection_in;
        end
        
        function saveVect(app)
            % Create temporary figure with axes - saveas() is not supported as of r2019a in AppDesigner
            fig=figure;
            fig.Visible='off';
            figAxes=axes(fig);
            figAxes.NextPlot='replace';
            imagesc(figAxes,app.images.comPhase,'AlphaData',app.images.comMagNorm);
            set(figAxes,'DataAspectRatio',[1 1 1],'XTick',[],'Ytick',[],'YDir','reverse','Color','k');
            axis(figAxes,app.params.limits.im);
            colormap(figAxes,hsv);
            
            set(figAxes,'NextPlot','add');
            quiver(1:app.params.subsample:app.params.framesx,...
                1:app.params.subsample:app.params.framesy,...
                -app.images.comx(1:app.params.subsample:end,1:app.params.subsample:end)./app.params.subsample,...
                -app.images.comy(1:app.params.subsample:end,1:app.params.subsample:end)./app.params.subsample,...
                1/app.params.subsample,app.params.vectColor,'Parent', figAxes);
            set(figAxes,'DataAspectRatio',[1 1 1],'XTick',[],'Ytick',[],'YDir','reverse','NextPlot','replace');
            axis(figAxes,app.params.limits.im);
            
            % Save as a .png, .fig, and .eps (vector image, not pixelated)
            set(fig, 'Renderer', 'Painters');
            fig.InvertHardcopy = 'off';
            saveas(fig,strcat(app.params.savePrefs.prefix,'VectField.png'),'png');
            fig.Visible='on';savefig(fig,strcat(app.params.savePrefs.prefix,'VectField.fig'));fig.Visible='off';
            %saveas(fig,strcat(app.params.savePrefs.prefix,'VectField.svg'),'svg');
            
            csvwrite(strcat(app.params.savePrefs.prefix,'vector_field.txt'),[-app.images.comx(1:app.params.subsample:end,1:app.params.subsample:end)./app.params.subsample ...
                -app.images.comy(1:app.params.subsample:end,1:app.params.subsample:end)./app.params.subsample])
        end
        
        function updateImStats(app)
            % figure out which image is selected in the drop down, and
            % which axis is its primary axis
            try ax = eval(app.imageProperties(app.ImageDropDown.Value,:).axis{1});catch; end
            im = gather(eval(app.imageProperties(app.ImageDropDown.Value,:).image{:}));
            
            app.imStats.ColumnName   = {strcat(app.ImageDropDown.Items{strcmp(app.ImageDropDown.Value,app.ImageDropDown.ItemsData)},' stats')};
            app.imStats.ColumnFormat = {'numeric'};
            app.imStats.Data         = [min(im(:));
                                        max(im(:));
                                        mean(im(:));
                                        std(im(:));
                                        sum(im(:))];
            
            % Generate an intensity histogram for the selected image
            if numel(im)~=sum(isnan(im),'all')
                h=histogram(app.histogramPlot,im,100);
            else
                h=histogram(app.histogramPlot,zeros(size(im)),100);
            end
            app.histogramPlot.Toolbar.Visible = 'off';
            
            if app.histLog.Value
                set(app.histogramPlot,'YScale','log');
            else
                set(app.histogramPlot,'YScale','linear');
            end
            
            % Set histogram plot axes
            try
                axis(app.histogramPlot,[min(im(:))-0.05*range(im(:)),...
                    max(im(:))+0.05*range(im(:)),...
                    1,...
                    max(h.BinCounts)]);
            catch
                if numel(im)~=sum(isnan(im),'all')
                    axis(app.histogramPlot,[mean(im(:))+[-1 1] 1 max(h.BinCounts)]);
                else
                    axis(app.histogramPlot,[-1 1 1 max(h.BinCounts)]);
                end
                
            end
            % To account for any negative values in the diffraction
            % pattern while in log scale
            if app.dpLog.Value
                app.diffPattern.ColorScale = 'log';
                if app.diffPattern.CLim(2)<1e-7 app.diffPattern.CLim(2)=1e-7;end
                if app.diffPattern.CLim(1)<=0 app.diffPattern.CLim(1)=1e-8; end
            end
            
            % Add annotations to the histogram plot for min and max values,
            % as well as a gamma curve. If the image is not currently being
            % displayed, this will not show AXIS limits, but rather default to
            % IMAGE limits, regardless of the constrast/brightness/gamma levels
            hold(app.histogramPlot,'on');
            try
                plot(app.histogramPlot,ax.CLim(1)*[1 1],app.histogramPlot.YLim,'LineWidth',2,'Color','g');
            catch
                plot(app.histogramPlot,min(im(:))*[1 1],app.histogramPlot.YLim,'LineWidth',2,'Color','g')
            end
            
            try
                plot(app.histogramPlot,ax.CLim(2)*[1 1],app.histogramPlot.YLim,'LineWidth',2,'Color','g');
            catch
                plot(app.histogramPlot,max(im(:))*[1 1],app.histogramPlot.YLim,'LineWidth',2,'Color','g');
            end
            
            try
                plot(app.histogramPlot,linspace(ax.CLim(1),ax.CLim(2),100),(linspace(0,app.histogramPlot.YLim(2),100).^app.gamma.Value)./app.histogramPlot.YLim(2)^app.gamma.Value*app.histogramPlot.YLim(2),'Color','k');
            catch
                plot(app.histogramPlot,linspace(min(im(:)),max(im(:)),100),(linspace(0,app.histogramPlot.YLim(2),100).^app.gamma.Value)./app.histogramPlot.YLim(2)^app.gamma.Value*app.histogramPlot.YLim(2),'Color','k');
            end
            
            app.histogramPlot.NextPlot='replace';
            app.histogramPlot.YTick = [];
            
            % display min, max, and gamma values on the histogram
            try delete(app.annotations.gamma_text);catch;end
            try
                app.annotations.gamma_text  = text(app.histogramPlot,0.98,0.98,...
                                                   sprintf('min: %0.2f\nmax: %0.2f\ngamma: %0.2f',ax.CLim(1),ax.CLim(2),app.gamma.Value),...
                                                   'FontSize',12,'HorizontalAlignment','right','VerticalAlignment','top',...
                                                   'BackgroundColor','w','Units','normalized');
            catch
                app.annotations.gamma_text  = text(app.histogramPlot,0.98,0.98,...
                                                   sprintf('min: %0.2f\nmax: %0.2f\ngamma: %0.2f',min(im(:)),max(im(:)),app.gamma.Value),...
                                                   'FontSize',12,'HorizontalAlignment','right','VerticalAlignment','top',...
                                                   'BackgroundColor','w','Units','normalized');
            end
            
        end
        
        
        % function to draw PACBED ROI of various shapes on real space image(s)
        function drawROI(app,event)
            % delete previous pacbedROI if it exists
            try delete(app.annotations.bfdfROI);catch;end
            try delete(app.annotations.comxROI);catch;end
            try delete(app.annotations.comyROI);catch;end
            try delete(app.annotations.comMagROI);catch;end
            try delete(app.annotations.comPhaseROI);catch;end
            delete(findall(app.bfdfPlot,'-not','Type','axes','-not','Type','Image'));
            
            % draw ROI based on the user selection for shape
            switch app.roiButtonGroup.SelectedObject
                case app.roiPoint
                    app.annotations.bfdfROI = drawpoint(app.bfdfPlot,"Deletable",false,"Position",[app.probeX.Value app.probeY.Value],"Color",[255 126 121]/255);
                    if app.com.Value || app.dpc.Value
                        app.annotations.comxROI = drawpoint(app.comx,"Deletable",false,"Position",[app.probeX.Value app.probeY.Value],"Color",[255 126 121]/255);
                        app.annotations.comyROI = drawpoint(app.comy,"Deletable",false,"Position",[app.probeX.Value app.probeY.Value],"Color",[255 126 121]/255);
                        app.annotations.comMagROI = drawpoint(app.comMag,"Deletable",false,"Position",[app.probeX.Value app.probeY.Value],"Color",[255 126 121]/255);
                        app.annotations.comPhaseROI = drawpoint(app.comPhase,"Deletable",false,"Position",[app.probeX.Value app.probeY.Value],"Color",[255 126 121]/255);
                    end
                case app.roiEllipse
                    app.annotations.bfdfROI = drawellipse(app.bfdfPlot,'Center',[app.probeX.Value app.probeY.Value],'Deletable',false,"Color",[255 126 121]/255,"SemiAxEs",min(0.05*range([app.bfdfPlot.XLim;app.bfdfPlot.YLim]'))*[1 1]);
                    if app.com.Value || app.dpc.Value
                        app.annotations.comxROI = drawellipse(app.comx,'Center',[app.probeX.Value app.probeY.Value],'Deletable',false,"Color",[255 126 121]/255,"SemiAxEs",min(0.05*range([app.bfdfPlot.XLim;app.bfdfPlot.YLim]'))*[1 1]);
                        app.annotations.comyROI = drawellipse(app.comy,'Center',[app.probeX.Value app.probeY.Value],'Deletable',false,"Color",[255 126 121]/255,"SemiAxEs",min(0.05*range([app.bfdfPlot.XLim;app.bfdfPlot.YLim]'))*[1 1]);
                        app.annotations.comMagROI = drawellipse(app.comMag,'Center',[app.probeX.Value app.probeY.Value],'Deletable',false,"Color",[255 126 121]/255,"SemiAxEs",min(0.05*range([app.bfdfPlot.XLim;app.bfdfPlot.YLim]'))*[1 1]);
                        app.annotations.comPhaseROI = drawellipse(app.comPhase,'Center',[app.probeX.Value app.probeY.Value],'Deletable',false,"Color",[255 126 121]/255,"SemiAxEs",min(0.05*range([app.bfdfPlot.XLim;app.bfdfPlot.YLim]'))*[1 1]);
                    end
                case app.roiRectangle
                    app.annotations.bfdfROI = drawrectangle(app.bfdfPlot,"Rotatable",true,"Deletable",false,"Color",[255 126 121]/255,"Position",[[app.probeX.Value app.probeY.Value]-0.05*range([app.bfdfPlot.XLim;app.bfdfPlot.YLim]') 0.1*range([app.bfdfPlot.XLim;app.bfdfPlot.YLim]')]);
                    if app.com.Value || app.dpc.Value
                        app.annotations.comxROI = drawrectangle(app.comx,"Rotatable",true,"Deletable",false,"Color",[255 126 121]/255,"Position",[[app.probeX.Value app.probeY.Value]-0.05*range([app.bfdfPlot.XLim;app.bfdfPlot.YLim]') 0.1*range([app.bfdfPlot.XLim;app.bfdfPlot.YLim]')]);
                        app.annotations.comyROI = drawrectangle(app.comy,"Rotatable",true,"Deletable",false,"Color",[255 126 121]/255,"Position",[[app.probeX.Value app.probeY.Value]-0.05*range([app.bfdfPlot.XLim;app.bfdfPlot.YLim]') 0.1*range([app.bfdfPlot.XLim;app.bfdfPlot.YLim]')]);
                        app.annotations.comMagROI = drawrectangle(app.comMag,"Rotatable",true,"Deletable",false,"Color",[255 126 121]/255,"Position",[[app.probeX.Value app.probeY.Value]-0.05*range([app.bfdfPlot.XLim;app.bfdfPlot.YLim]') 0.1*range([app.bfdfPlot.XLim;app.bfdfPlot.YLim]')]);
                        app.annotations.comPhaseROI = drawrectangle(app.comPhase,"Rotatable",true,"Deletable",false,"Color",[255 126 121]/255,"Position",[[app.probeX.Value app.probeY.Value]-0.05*range([app.bfdfPlot.XLim;app.bfdfPlot.YLim]') 0.1*range([app.bfdfPlot.XLim;app.bfdfPlot.YLim]')]);
                    end
                case app.roiPoly
                    % currently must be on bfdfTab to draw freeform polygon
                    app.outputPanel.SelectedTab = app.bfdfTab;
                    app.annotations.bfdfROI = drawpolygon(app.bfdfPlot,"Deletable",false,"Color",[255 126 121]/255);
                    
                    if app.com.Value || app.dpc.Value
                        app.annotations.comxROI = drawpolygon(app.comx,"Deletable",false,"Color",[255 126 121]/255,"Position",app.annotations.bfdfROI.Position);
                        app.annotations.comyROI = drawpolygon(app.comy,"Deletable",false,"Color",[255 126 121]/255,"Position",app.annotations.bfdfROI.Position);
                        app.annotations.comMagROI = drawpolygon(app.comMag,"Deletable",false,"Color",[255 126 121]/255,"Position",app.annotations.bfdfROI.Position);
                        app.annotations.comPhaseROI = drawpolygon(app.comPhase,"Deletable",false,"Color",[255 126 121]/255,"Position",app.annotations.bfdfROI.Position);
                    end
            end
            
            % add listening function for live updates while moving/resizing
            app.annotations.listeners.bfdfMoving = addlistener(app.annotations.bfdfROI,'MovingROI',@app.moveROI);
            app.annotations.listeners.bfdfMoved = addlistener(app.annotations.bfdfROI,'ROIMoved',@app.moveROI);
            if app.com.Value || app.dpc.Value
                app.annotations.listeners.comxMoving = addlistener(app.annotations.comxROI,'MovingROI',@app.moveROI);
                app.annotations.listeners.comxMoved = addlistener(app.annotations.comxROI,'ROIMoved',@app.moveROI);
                app.annotations.listeners.comyMoving = addlistener(app.annotations.comyROI,'MovingROI',@app.moveROI);
                app.annotations.listeners.comyMoved = addlistener(app.annotations.comyROI,'ROIMoved',@app.moveROI);
                app.annotations.listeners.comMagMoving = addlistener(app.annotations.comMagROI,'MovingROI',@app.moveROI);
                app.annotations.listeners.comMagMoved = addlistener(app.annotations.comMagROI,'ROIMoved',@app.moveROI);
                app.annotations.listeners.comPhaseMoving = addlistener(app.annotations.comPhaseROI,'MovingROI',@app.moveROI);
                app.annotations.listeners.comPhaseMoved = addlistener(app.annotations.comPhaseROI,'ROIMoved',@app.moveROI);
            end
            % run the listener to update any/all other ROIs and the PACBED pattern
            moveROI(app,app.annotations.bfdfROI,event)
        end
        
        % live update function for PACBED ROIs
        function moveROI(app,src,event)
            % update the probeX,probeY position spinners so that if the
            % users switches ROI type, it stays centered about the same
            % point; try to update all other versions of the ROI if in
            % DPC/CoM mode
            switch app.roiButtonGroup.SelectedObject
                case app.roiPoint
                    src.Position = round(src.Position);
                    app.mask.pacbed = false(size(app.images.adf));
                    app.mask.pacbed(round(src.Position(2)),round(src.Position(1)))=true;
                    app.probeX.Value = round(src.Position(1));
                    app.probeY.Value = round(src.Position(2));
                case app.roiEllipse
                    app.probeX.Value = round(src.Center(1));
                    app.probeY.Value = round(src.Center(2));
                case app.roiRectangle
                    app.probeX.Value = round(src.Position(1)+0.5*src.Position(3));
                    app.probeY.Value = round(src.Position(2)+0.5*src.Position(4));
                case app.roiPoly
                    [x,y]=centroid(polyshape(src.Position));
                    app.probeX.Value = round(x);
                    app.probeY.Value = round(y);
            end
            
            % carry shape descriptors through to all versions of each ROI  position
            try app.annotations.bfdfROI.Position = src.Position;catch;end
            try app.annotations.comxROI.Position = src.Position;catch;end
            try app.annotations.comyROI.Position = src.Position;catch;end
            try app.annotations.comMagROI.Position = src.Position;catch;end
            try app.annotations.comPhaseROI.Position = src.Position;catch;end
            % center
            try app.annotations.bfdfROI.Center = src.Center;catch;end
            try app.annotations.comxROI.Center = src.Center;catch;end
            try app.annotations.comyROI.Center = src.Center;catch;end
            try app.annotations.comMagROI.Center = src.Center;catch;end
            try app.annotations.comPhaseROI.Center = src.Center;catch;end
            % semiaxes
            try app.annotations.bfdfROI.SemiAxes = src.SemiAxes;catch;end
            try app.annotations.comxROI.SemiAxes = src.SemiAxes;catch;end
            try app.annotations.comyROI.SemiAxes = src.SemiAxes;catch;end
            try app.annotations.comMagROI.SemiAxes = src.SemiAxes;catch;end
            try app.annotations.comPhaseROI.SemiAxes = src.SemiAxes;catch;end
            % rotation angle
            try app.annotations.bfdfROI.RotationAngle = src.RotationAngle;catch;end
            try app.annotations.comxROI.RotationAngle = src.RotationAngle;catch;end
            try app.annotations.comyROI.RotationAngle = src.RotationAngle;catch;end
            try app.annotations.comMagROI.RotationAngle = src.RotationAngle;catch;end
            try app.annotations.comPhaseROI.RotationAngle = src.RotationAngle;catch;end
            
            % update stack slider for individual probe positions
            app.probePosition.Value = (app.probeY.Value-1)*app.params.framesx + app.probeX.Value;
            
            % generate a mask for displaying pacbed pattern
            if ~app.roiPoint.Value app.mask.pacbed = createMask(app.annotations.bfdfROI);end
            
            % negative mask?
            if app.negativeROI.Value app.mask.pacbed = 1 - app.mask.pacbed; end
            
            % update the ROI position on the screen. This call also
            % allows the callback to be interrupted, which skips the
            % lines below, if, for example, the user is moving/resizing
            % the ROI faster than the new image can be refreshed on the
            % plot
            drawnow
            
            % redefine pacbed pattern for the specified ROI
            % Matlab does not implement mtimes() for integer class arrays,
            % so check if it is an integer. If it is an integer class array
            % (i.e. Medipix data), check if it should be multiplied as
            % single or double precision float
            if isinteger(app.data) && app.params.bytesize<=4 % int32/uint32 (or less) data
                app.images.pacbed = gather(reshape(single(app.data)*app.mask.pacbed(:),[app.params.nopix app.params.nopiy]));
            elseif isinteger(app.data) && app.params.bytesize>4 % int64/uint64 data
                app.images.pacbed = gather(reshape(double(app.data)*app.mask.pacbed(:),[app.params.nopix app.params.nopiy]));
            else % floating point data
                app.images.pacbed = gather(reshape(app.data*app.mask.pacbed(:),[app.params.nopix app.params.nopiy]));
            end
            
            % should be averaged, not summed
            app.images.pacbed = app.images.pacbed/sum(app.mask.pacbed(:));
            
            % live update diffraction pattern images as the ROI moves
            plotImage(app,'pacbed');
            
            % replot detectors
            plotDetector(app,event);
        end
        
        % live update function for transmitted beam alignment
        function moveTransBeam(app,src,~)
            % grab the center and radius of the circle as the user changes
            % it, update their displays on the "Calibration" tab
            app.centerX.Value = src.Center(1);
            app.centerY.Value = src.Center(2);
            app.params.radius = src.Radius;
            
            % live update diffraction scaling factor based on radius of the
            % disk and convergence angle input from user in correct units
            app.params.mrad_per_pix = app.alpha.Value/app.params.radius;
            switch app.diffractionCalibration.SelectedObject
                case app.mradButton
                    app.transCal.Value = 1/app.params.mrad_per_pix;
                    app.pixelsmradEditFieldLabel.Text = 'pixels / mrad';
                case app.invAButton
                    app.transCal.Value = app.params.radius/mrad2invA(app,app.alpha.Value,'mrad');
                    app.pixelsmradEditFieldLabel.Text = 'pixels / invA';
            end
            
            % live update radius on "Calibration" tab in correct units
            switch app.transmittedDiskRadius.SelectedObject
                case app.transRadPix
                    app.transRad.Value = app.params.radius;
                case app.transRadMrad
                    app.transRad.Value = app.alpha.Value;
                case app.transRadInvA
                    app.transRad.Value = mrad2invA(app,app.alpha.Value,'mrad');
            end
            
            % live update sliders on "Alignment" tab
            app.transBeamX.Value = app.centerX.Value - app.params.center0(1);
            app.transBeamY.Value = app.centerY.Value - app.params.center0(2);
            app.transBeamRadius.Value = app.params.radius;
            
            drawnow
        end
        
        % function to draw virtual apertures
        function drawApertures(app,event)
            % try to delete any remnant detectos
            try delete(app.annotations.aperture);catch;end
            
            switch app.coordinatesButtonGroup.SelectedObject
                case app.polarRadio
                    theta = app.apY.Value;
                    dist = app.apX.Value;
                case app.cartesianRadio
                    theta = atan2(app.apY.Value,app.apX.Value) + [0:2*pi/app.apertureSymmetry.Value:2*pi*(1-1/app.apertureSymmetry.Value)]'; %#ok<*NBRAK> 
                    dist = sqrt(sum((app.params.apCenter - [app.centerX.Value app.centerY.Value]).^2));
            end
            
            theta = theta + [0:2*pi/app.apertureSymmetry.Value:2*pi*(1-1/app.apertureSymmetry.Value)]';
            center = dist*[cos(theta) sin(theta)];
            
            % mirrored?
            if app.apMirror.Value
                R_mirror = [cos(app.apMirrorAngle.Value-pi/2) -sin(app.apMirrorAngle.Value-pi/2); sin(app.apMirrorAngle.Value-pi/2) cos(app.apMirrorAngle.Value-pi/2)];
                center = [center;center*R_mirror.*[-1 1]*(R_mirror.*[1 -1;-1 1])];
            end
            
            center = center + [app.centerX.Value app.centerY.Value];
            
            % plot the apertures, and olny allow the first one to be interactable
            for ii=1:size(center,1)
                if ii==1
                    app.annotations.aperture(1) = drawcircle(app.diffPattern,"Center",center(ii,:),"Radius",app.params.apRadius,'Color','r','FaceAlpha',0,'Deletable',false,'InteractionsAllowed','all');
                    app.mask.bfdf = createMask(app.annotations.aperture(1));
                else
                    app.annotations.aperture(ii,1) = drawcircle(app.diffPattern,"Center",center(ii,:),"Radius",app.params.apRadius,'Color','r','FaceAlpha',0,'Deletable',false,'InteractionsAllowed','none');
                    app.mask.bfdf = app.mask.bfdf + createMask(app.annotations.aperture(ii));
                end
            end
            
            app.annotations.mirror_line = drawline(app.diffPattern,"Color","g","InteractionsAllowed","none","Visible","off","LineWidth",2,"Deletable",false,"Position",[[1;app.params.nopix],tan(app.apMirrorAngle.Value)*([1;app.params.nopix]-app.centerX.Value)+app.centerY.Value]);
            if app.apMirror.Value
                app.annotations.mirror_line.Visible = "on";
            end
            
            % always make sure the draggable aperture is at the front
            bringToFront(app.annotations.aperture(1));
            app.mask.bfdf = logical(app.mask.bfdf);
            
            app.annotations.listeners.apertureMoved = addlistener(app.annotations.aperture(1),'ROIMoved',@app.moveApertures);
            app.annotations.listeners.apertureMoving = addlistener(app.annotations.aperture(1),'MovingROI',@app.moveApertures);
            moveApertures(app,app.annotations.aperture(1),event)
        end
        
        % live update function for virtual aperture(2)
        function moveApertures(app,src,event)
            if app.vdf.Value
                % if app.annotations.aperture(1) has not yet been drawn, draw
                % it now
                if isstruct(app.annotations.aperture(1))
                    app.annotations = rmfield(app.annotations,'aperture');
                    drawApertures(app,event);
                end
                
                % if the source is the aperture being dragged/resized, update
                % all of teh sliders and fields in the "Virtual Aperture" tab
                switch src
                    case app.annotations.aperture(1)
                        if src.Radius <= app.apSize.Limits(2)
                            app.annotations.aperture(1).Radius = src.Radius;
                        else
                            app.annotations.aperture(1).Radius = app.apSize.Limits(2);
                        end
                        app.apSize.Value = app.annotations.aperture(1).Radius;
                        app.params.apRadius = app.apSize.Value;
                        app.apSizeField.Value = app.apSize.Value*app.params.mrad_per_pix;
                        app.params.apCenter = src.Center;
                        
                    case app.apMirrorAngle
                        % update the mirror line position
                        app.apMirrorAngle.Value = event.Value;
                end
                
                % make sure the disk is never fully out of view
                if all(app.params.apCenter<-0.95*app.params.apRadius)
                    app.params.apCenter = -0.95*app.params.apRadius*[1 1];
                elseif all(app.params.apCenter > ([app.params.nopix app.params.nopiy]+0.95*app.params.apRadius))
                    app.params.apCenter = 0.95*app.params.apRadius+[app.params.nopix apop.params.nopiy];
                elseif app.params.apCenter(1)<-0.95*app.params.apRadius
                    app.params.apCenter = [-0.95*app.params.apRadius app.params.apCenter(2)];
                elseif app.params.apCenter(2)<-0.95*app.params.apRadius
                    app.params.apCenter = [app.params.apCenter(1) -0.95*app.params.apRadius];
                elseif app.params.apCenter(1)>app.params.nopix+0.95*app.params.apRadius
                    app.params.apCenter = [app.params.nopix+0.95*app.params.apRadius app.params.apCenter(2)];
                elseif app.params.apCenter(2)>app.params.nopiy+0.95*app.params.apRadius
                    app.params.apCenter = [app.params.apCenter(1) app.params.nopix+0.95*app.params.apRadius];
                end
                app.annotations.aperture(1).Center = app.params.apCenter;
                
                switch app.coordinatesButtonGroup.SelectedObject
                    case app.cartesianRadio
                        app.apX.Value = app.params.apCenter(1)-app.centerX.Value;
                        app.apXField.Value = app.apX.Value*app.params.mrad_per_pix;
                        app.apY.Value = app.params.apCenter(2)-app.centerY.Value;
                        app.apYField.Value = app.apY.Value*app.params.mrad_per_pix;
                    case app.polarRadio
                        app.apX.Value=min(sqrt(sum((app.params.apCenter-[app.centerX.Value,app.centerY.Value]).^2)),app.apX.Limits(2));
                        app.apXField.Value=app.apX.Value*app.params.mrad_per_pix;
                        app.apY.Value=atan2(app.params.apCenter(2)-app.centerY.Value,app.params.apCenter(1)-app.centerX.Value);
                        app.apYField.Value=rad2deg(app.apY.Value);
                end
                % allow the user to drag the cirle up to 95% off the diffraction pattern
                % at the corners
                app.annotations.aperture(1).DrawingArea = (0.95*app.params.apRadius*(1+1/sqrt(2)))*[-1 -1 2 2]+[0 0 app.params.nopix app.params.nopiy];
                switch app.coordinatesButtonGroup.SelectedObject
                    case app.cartesianRadio
                        app.apX.Limits = [0 app.params.nopix] - app.centerX.Value + 0.95*app.params.apRadius*[-1 1];
                        app.apXField.Limits = app.apX.Limits*app.params.mrad_per_pix;
                        app.apY.Limits = [0 app.params.nopiy] - app.centerY.Value + 0.95*app.params.apRadius*[-1 1];
                        app.apYField.Limits = app.apY.Limits*app.params.mrad_per_pix;
                    case app.polarRadio
                        app.apX.Limits(1) = 0;
                        app.apX.Limits(2) = min([app.centerX.Value app.centerY.Value app.params.nopix-app.centerX.Value app.params.nopiy-app.centerY.Value]*sqrt(2))+0.95*app.params.apRadius;
                        app.apXField.Limits = app.apX.Limits*app.params.mrad_per_pix;
                        app.apY.Limits = [-pi pi];
                        app.apYField.Limits = [-180 180];
                end
                
                % rotate other circles as the first one moves/changes size
                dist = sqrt(sum((app.annotations.aperture(1).Center - [app.centerX.Value app.centerY.Value]).^2));
                center = atan2(app.annotations.aperture(1).Center(2)-app.centerY.Value,app.annotations.aperture(1).Center(1)-app.centerX.Value);
                center = center + [0:2*pi/app.apertureSymmetry.Value:2*pi*(1-1/app.apertureSymmetry.Value)]';
                center = dist*[cos(center) sin(center)];
                
                % update mirror line position, whether it is visible or not
                app.annotations.mirror_line.Position = [[1;app.params.nopix],tan(app.apMirrorAngle.Value)*([1;app.params.nopix]-app.centerX.Value)+app.centerY.Value];
                
                % mirrored?
                if app.apMirror.Value
                    R_mirror = [cos(app.apMirrorAngle.Value-pi/2) -sin(app.apMirrorAngle.Value-pi/2); sin(app.apMirrorAngle.Value-pi/2) cos(app.apMirrorAngle.Value-pi/2)];
                    center = [center;center*R_mirror.*[-1 1]*(R_mirror.*[1 -1;-1 1])];
                    app.annotations.mirror_line.Visible = 'on';
                else
                    app.annotations.mirror_line.Visible = 'off';
                end
                
                % shift back to the center of the diffraction pattern
                center = center + [app.centerX.Value app.centerY.Value];
                
                % clear the mask
                app.mask.bfdf = zeros(app.params.nopix,app.params.nopiy,'logical');
                
                % move all apertures and regenerate a logical bfdf mask
                for ii=1:max(size(app.annotations.aperture,1),2*app.apertureSymmetry.Value)
                    
                    if (~app.apMirror.Value && ii>app.apertureSymmetry.Value) || (app.apMirror.Value && ii>(2*app.apertureSymmetry.Value))
                        if ii<=size(app.annotations.aperture,1)
                            try app.annotations.aperture(ii,1).Visible = 'off';catch; end
                        end
                    elseif ii>size(app.annotations.aperture,1)
                        app.annotations.aperture(ii,1) = drawcircle(app.diffPattern,"Center",center(ii,:),"Radius",app.annotations.aperture(1).Radius,'Color','r','FaceAlpha',0,'Deletable',false,'InteractionsAllowed','none');
                        app.mask.aperture(:,:,ii) = createMask(app.annotations.aperture(ii,1));
                    else
                        try
                            app.annotations.aperture(ii,1).Radius = app.annotations.aperture(1).Radius;
                            app.annotations.aperture(ii,1).Center = center(ii,:);
                            app.annotations.aperture(ii,1).Visible = 'on';
                        catch
                            app.annotations.aperture(ii,1) = drawcircle(app.diffPattern,"Center",center(ii,:),"Radius",app.annotations.aperture(1).Radius,'Color','r','FaceAlpha',0,'Deletable',false,'InteractionsAllowed','none');
                        end
                        app.mask.aperture(:,:,ii) = createMask(app.annotations.aperture(ii,1));
                    end
                    
                end
                
                app.mask.bfdf = logical(sum(app.mask.aperture,3));
                app.mask.bfdf=app.mask.bfdf(:);
                
                % Negative mask checkbox?
                if app.apNegative.Value==1
                    app.mask.bfdf = 1 - app.mask.bfdf;
                end
                
                % update the circle position on the screen. This call also
                % allows the callback to be interrupted, which skips the
                % lines below, if, for example, the user is moving/resizing
                % the ROI faster than the new image can be refreshed on the
                % plot
                drawnow 
                
                % plot new image if the user has "Live Update" enabled
                if app.liveUpdate.Value
                    % Integrate wihtin the mask
                    % Matlab does not implement mtimes() for integer class arrays,
                    % so check if it is an integer. If it is an integer class array
                    % (i.e. Medipix data), check if it should be multiplied as
                    % single or double precision float
                    if isinteger(app.data) && app.params.bytesize<=4 % int32/uint32 (or less) data
                        app.images.adf = reshape(app.mask.bfdf'*single(app.data),[app.params.framesx app.params.framesy]);
                    elseif isinteger(app.data) && app.params.bytesize>4 % int64/uint64 data
                        app.images.adf = reshape(app.mask.bfdf'*double(app.data),[app.params.framesx app.params.framesy]);
                    else % floating point data
                        app.images.adf = reshape(app.mask.bfdf'*app.data,[app.params.framesx app.params.framesy]);
                    end

                    plotImage(app,'adf');
                end
                
                % always make sure the draggable aperture is at the front
                bringToFront(app.annotations.aperture(1));
            else
                try app.annotations.aperture(1,1).Visible = 'off';catch; end
                for ii=2:size(app.annotations.aperture,1)
                    try app.annotations.aperture(ii,1).Visible = 'off';catch; end
                end
            end
        end
        
        % function to draw annular/round/segmented detectors
        function drawDetectors(app)
            % make sure there are no remnant detectors displayed
            try delete(app.annotations.adfInner);catch;end
            try delete(app.annotations.adfOuter);catch;end
            try delete(app.annotations.rung);catch;end
            try delete(app.annotations.segment);catch;end
            
            
            % draw inner and outer circles
            app.annotations.adfInner = drawcircle(app.diffPattern,"Color","g","Deletable",false,"Center",[app.centerX.Value app.centerY.Value],"FaceAlpha",0,"InteractionsAllowed","reshape","LineWidth",4,"Radius",app.adfInner.Value,"Visible","on","FaceSelectable",false);
            app.annotations.adfOuter = drawcircle(app.diffPattern,"Color","r","Deletable",false,"Center",[app.centerX.Value app.centerY.Value],"FaceAlpha",0,"InteractionsAllowed","reshape","LineWidth",4,"Radius",app.adfOuter.Value,"Visible","on","FaceSelectable",false);
            
            % update the drawing area so that the disks can go out to the
            % limits of the detector range, which is larger than the pattern
            app.annotations.adfInner.DrawingArea = [[app.centerX.Value app.centerY.Value] - app.adfOuter.Limits(2) 2*app.adfOuter.Limits(2)*[1 1]];
            app.annotations.adfOuter.DrawingArea = [[app.centerX.Value app.centerY.Value] - app.adfOuter.Limits(2) 2*app.adfOuter.Limits(2)*[1 1]];
            
            if app.dpc.Value
                % plot the circles between rungs
                if app.nrung.Value>1
                    if (isfield(app.annotations,'rung')&&isstruct(app.annotations.rung)) app.annotations.rung=[];end
                    for jj=1:app.nrung.Value-1
                        app.annotations.rung(jj,1) = drawcircle(app.diffPattern,"Radius",jj/app.nrung.Value*(app.adfOuter.Value-app.adfInner.Value)+app.adfInner.Value,"Center",[app.centerX.Value,app.centerY.Value],"InteractionsAllowed","none",'Color',"w",'LineWidth',2,"FaceAlpha",0,"FaceSelectable",false,"Visible",true);
                    end
                end
                
                % plot the lines between segments
                for ii=1:app.nseg.Value
                    x = [app.adfInner.Value;app.adfOuter.Value]*cos(app.detAngle.Value+2*pi*(ii-1)/app.nseg.Value)+app.centerX.Value;
                    y = [app.adfInner.Value;app.adfOuter.Value]*sin(app.detAngle.Value+2*pi*(ii-1)/app.nseg.Value)+app.centerY.Value;
                    app.annotations.segment(ii,1) = drawline(app.diffPattern,"Position",[x y],"InteractionsAllowed","none","LineWidth",2,"Color","b","Visible",true);
                end
            end
            
            % add listenr for live update during user interaction
            app.annotations.listeners.adfInnerMoved = addlistener(app.annotations.adfInner,'ROIMoved',@app.moveDetectors);
            app.annotations.listeners.adfInnerMoving = addlistener(app.annotations.adfInner,'MovingROI',@app.moveDetectors);
            app.annotations.listeners.adfOuterMoved = addlistener(app.annotations.adfOuter,'ROIMoved',@app.moveDetectors);
            app.annotations.listeners.adfOuterMoving = addlistener(app.annotations.adfOuter,'MovingROI',@app.moveDetectors);
        end
        
        % function to live update annular/round/segmented detectors
        function moveDetectors(app, src, event)
            % update values based on who is triggering the event
            switch src
                case app.annotations.adfInner
                    % check to see if inner/outer detector ranges are
                    % linked, and if they cause either to go out of bounds
                    if app.linkADF.Value && (app.adfInner.Value+app.params.detWidth)<=app.adfOuter.Limits(2) && strcmp(event.EventName,'MovingROI')
                        app.annotations.adfInner.Radius = max(event.CurrentRadius,0);
                        app.adfInner.Value = app.annotations.adfInner.Radius;
                        app.annotations.adfOuter.Radius = app.annotations.adfInner.Radius + app.params.detWidth;
                        app.adfOuter.Value = app.annotations.adfOuter.Radius;
                    elseif app.linkADF.Value && (app.adfInner.Value+app.params.detWidth)>app.adfOuter.Limits(2) && strcmp(event.EventName,'MovingROI')
                        app.adfInner.Value = app.params.rmax-app.params.detWidth;
                        app.annotations.adfInner.Radius = app.adfInner.Value;
                        app.annotations.adfOuter.Radius = app.params.rmax;
                        app.adfOuter.Value = app.annotations.adfOuter.Radius;
                    elseif event.CurrentRadius >= app.annotations.adfOuter.Radius
                        app.adfInner.Value = app.adfOuter.Value;
                        app.annotations.adfInner.Radius = app.annotations.adfOuter.Radius;
                    else
                        app.adfInner.Value = event.CurrentRadius;
                    end
                    
                case app.annotations.adfOuter
                    % check to see if inner/outer detector ranges are
                    % linked, and if they cause either to go out of bounds
                    if app.linkADF.Value && app.adfOuter.Value>=app.params.detWidth && strcmp(event.EventName,'MovingROI')
                        app.annotations.adfOuter.Radius = max(event.CurrentRadius,app.params.detWidth);
                        app.adfOuter.Value = app.annotations.adfOuter.Radius;
                        app.annotations.adfInner.Radius = app.annotations.adfOuter.Radius - app.params.detWidth;
                        app.adfInner.Value = app.annotations.adfInner.Radius;
                    elseif app.linkADF.Value && app.adfOuter.Value<app.params.detWidth && strcmp(event.EventName,'MovingROI')
                        app.adfOuter.Value = app.params.detWidth;
                        app.annotations.adfOuter.Radius = app.adfOuter.Value;
                        app.annotations.adfInner.Radius = 0;
                        app.adfInner.Value = app.annotations.adfInner.Radius;
                    elseif event.CurrentRadius <= app.annotations.adfInner.Radius
                        app.adfOuter.Value = app.adfInner.Value;
                        app.annotations.adfOuter.Radius = app.annotations.adfInner.Radius;
                    else
                        app.adfOuter.Value = event.CurrentRadius;
                    end
                    
                otherwise
                    % if the event is triggered by a slider/button/field
                    % (i.e "annularDetector" callback funciton) update the
                    % size of the circles on display
                    app.annotations.adfInner.Radius = app.adfInner.Value;
                    app.annotations.adfOuter.Radius = app.adfOuter.Value;
            end
            
            % update numeric field boxes
            app.adfInnerField.Value = app.adfInner.Value*app.params.mrad_per_pix;
            app.adfOuterField.Value = app.adfOuter.Value*app.params.mrad_per_pix;
            
            % if in DPC mode, redraw segments/rungs
            if app.dpc.Value
                % plot the circles between rungs
                if app.nrung.Value>1
                    for jj=1:app.nrung.Value-1
                        app.annotations.rung(jj,1).Radius = jj/app.nrung.Value*(app.adfOuter.Value-app.adfInner.Value)+app.adfInner.Value;
                        app.annotations.rung(jj,1).Center = [app.centerX.Value,app.centerY.Value];
                    end
                end
                
                % plot the lines between segments
                for ii=1:app.nseg.Value
                    x = [app.adfInner.Value;app.adfOuter.Value]*cos(app.detAngle.Value+2*pi*(ii-1)/app.nseg.Value)+app.centerX.Value;
                    y = [app.adfInner.Value;app.adfOuter.Value]*sin(app.detAngle.Value+2*pi*(ii-1)/app.nseg.Value)+app.centerY.Value;
                    app.annotations.segment(ii,1).Position = [x y];
                end
            end
            
            % Display BF/ADF images **NOTE** the factors of 2 here are
            % because the radial integration was done on a 1/2 pixel step.
            % The plus 1 is because the array begins at 0, but is 1-indexed.
            start  = round(min(app.adfInner.Value,max(app.adfOuter.Value,app.adfInner.Value))*2)+1;
            finish = round(max(app.adfOuter.Value,app.adfInner.Value)*2)+1;
                        
            app.images.adf = sum(app.images.annular(:,:,start:finish),3);
            app.mask.bfdf = reshape(sum(app.mask.adf(start:finish,:),1),[app.params.nopix app.params.nopiy]);
            
            % update the ROI position on the screen. This call also
            % allows the callback to be interrupted, which skips the
            % lines below, if, for example, the user is moving/resizing
            % the ROI faster than the new image can be refreshed on the
            % plot
            drawnow
            
            % update images
            if app.liveUpdate.Value
                switch app.detectorTypeButtonGroup.SelectedObject
                    case {app.com,app.dpc}
                        integrateMasks(app)
                        displayCoM(app)
                end
            end
            
            % replot BF/DF image
            plotImage(app,'adf');
            
            % as soon as the user stops changing things, update the image histogram
            % (too time consuming for smooth image updates)
            if ~(isprop(event,'EventName') && any(strcmp(event.EventName,{'MovingROI';'ValueChanging'}))) && ~(isprop(event,'Name') && strcmp(event.EventName,'ValueChanging'))
                updateImStats(app);
            end
                        
            % save tmp values for current adf_inner and adf_out values
            % in case they are set to move together
            app.params.detWidth = app.adfOuter.Value - app.adfInner.Value; 
            
        end
    
        function scanRotation(app)
            % Rotation matrix based on the scan rotation angle
            R = [cos(app.scanRot.Value) sin(app.scanRot.Value); -sin(app.scanRot.Value) cos(app.scanRot.Value)];
            
            scanx_vect=[app.params.rmax/2 0]*R;
            scanx_pos=0.6*app.params.rmax*[cos(app.scanRot.Value) sin(app.scanRot.Value)]+[app.centerX.Value app.centerY.Value];
            
            switch app.scanRotMirror.Value
                case 0 % not mirrored
                    scany_vect=[0 app.params.rmax/2]*R;
                    scany_pos=0.6*app.params.rmax*[cos(app.scanRot.Value+pi/2) sin(app.scanRot.Value+pi/2)]+[app.centerX.Value app.centerY.Value];
                case 1 % mirrored
                    scany_vect=[0 -app.params.rmax/2]*R;
                    scany_pos=0.6*app.params.rmax*[cos(app.scanRot.Value-pi/2) sin(app.scanRot.Value-pi/2)]+[app.centerX.Value app.centerY.Value];
            end
            
            clearDetectors(app)
            
            app.annotations.scanx_arrow=quiver(app.diffPattern,app.centerX.Value,app.centerY.Value,scanx_vect(1),scanx_vect(2),'LineWidth',4,'Color',[252 99 94]/255);
            app.annotations.scany_arrow=quiver(app.diffPattern,app.centerX.Value,app.centerY.Value,scany_vect(1),scany_vect(2),'LineWidth',4,'Color',[252 99 94]/255);
            
            app.annotations.scanx_text=text(app.diffPattern,scanx_pos(1),scanx_pos(2),'scan_x','Color',[252 99 94]/255,'FontWeight','bold','FontSize',16,'HorizontalAlignment','center');
            app.annotations.scany_text=text(app.diffPattern,scany_pos(1),scany_pos(2),'scan_y','Color',[252 99 94]/255,'FontWeight','bold','FontSize',16,'HorizontalAlignment','center');
        end
        
        function restoreView(app,~,event)
            % this function makes up for the terrible default axis controls
            % from matlab. This ensures that "restoreview" goes back to the
            % limits of the actual image, nothing more/less.
            switch event.Axes
                case app.diffPattern
                    axis(app.diffPattern,app.params.limits.dp);
                otherwise
                    axis(event.Axes,app.params.limits.im);
            end
        end
    end
    

    % Callbacks that handle component events
    methods (Access = private)

        % Code that executes after component creation
        function startupFcn(app)
            movegui(app.Quant4D_Fig,"center");
            resetGui(app)
            figure(app.Quant4D_Fig);
        end

        % Button pushed function: importDataButton
        function importData(app, event)
            % Allow for importing binary files with extensions:
            %   .mib	-  Medipix
            %   .raw	-  EMPAD, ImageJ, Fiji, Matlab, etc.
            %   .mrc    - Fast CETA data
            %   .dm4    - Gatan K2/K3
            app.Quant4D_Fig.Interruptible = "off";
            startupFcn(app)
            cla(app.diffPattern);
            [app.params.filename,pathname]=uigetfile('*.raw;*.mib;*.mrc;*.dm4;*.npy','Select 4DSTEM Dataset');
            figure(app.Quant4D_Fig);
            app.controlPanel.SelectedTab=app.detectorsTab;
            if app.params.filename==0
                resetGui(app)
            else
                cd(pathname)
                
                % Ask the user for some basic parameters of the 4D data set and save them
                % to the GUI structure (app)
                
                % Import the 4D dataset
                appImport=import4Dstem(app,app.params.filename);
                uiwait(appImport.import_4d)
                
                % If the user clicks cancel, return to the initial GUI state
                if ~any(isfield(app.params,{'nopix','nopiy','framesy','framesy','header','footer','ordering','bitdepth','gpu','mem','convertFloat'})) || app.params.nopiy==0 || app.params.nopix==0 || app.params.framesy==0 || app.params.framesx==0
                    resetGui(app)
                else % User has clicked "Import" in the import GUI
                    app.Quant4D_Fig.Name = strcat(pathname,app.params.filename);
                    
                    % Set some initial values as guess, update later in function
                    app.centerX.Value = app.params.nopix/2; app.centerY.Value = app.params.nopiy/2; app.params.center0=[app.centerX.Value,app.centerY.Value];
                    app.params.radius = 20;
                    app.params.max_dist = floor(sqrt(sum((0.5*[app.params.nopiy app.params.nopix]).^2)));
                    
                    % Calculate the total number of frames; update the stack slider for later use
                    app.params.frames=app.params.framesx*app.params.framesy;
                    app.probePosition.Limits=[1 app.params.frames];
                    
                    % Start import timer
                    app.params.timer = tic;
                    import_bar = uiprogressdlg(app.Quant4D_Fig,'Title','Importing Data...','Message','Starting...','Indeterminate',"on");
                    import_bar = readFile(app,import_bar);
                    
                    
                    import_bar.Title = 'Processing Data...';
                    import_bar.Indeterminate = 'on';
                    import_bar.Message = sprintf('Forming PACBED\nPlease Wait...');
                    
                    % Create a summed image of all diffraction patterns simply for display
                    % purposes and alignment and calibration
                    app.params.limits.im=[1 app.params.framesy 1 app.params.framesx];
                    app.params.limits.dp=[1 app.params.nopiy 1 app.params.nopix];
                    app.images.pacbed=gather(reshape(mean(app.data,2),[app.params.nopix app.params.nopiy]));
                    axis(app.diffPattern,app.params.limits.dp);
                    plotImage(app,'pacbed');
                    
                    % Set initial axis limits
                    axis(app.bfdfPlot,app.params.limits.im);
                    axis(app.comx,app.params.limits.im);
                    axis(app.comy,app.params.limits.im);
                    axis(app.comMag,app.params.limits.im);
                    axis(app.comPhase,app.params.limits.im);
                    axis(app.vectorField,app.params.limits.im);
                    
                    % Try to autoAlign the transmitted beam
                    import_bar = autoAlign(app,event,import_bar);
                    
                    % Form BF/ADF images
                    import_bar.Value = 1;
                    import_bar.Message = sprintf('100%% Complete!\nForming Images... Please Wait');
                    app.images.adf = sum(app.images.annular(:,:,round(app.params.radius*2):round(app.params.max_dist)),3);
                    app.mask.bfdf = reshape(sum(app.mask.adf(round(app.params.radius*2):round(app.params.max_dist),:),1),[app.params.nopix app.params.nopiy]);
                    plotImage(app,'adf');
                    
                    import_bar.Message = sprintf('Setting up GUI\nPlease Wait');
                    import_bar.Indeterminate = 'on';
                    
                    % Setup some default starting values
                    app.params.center0=[app.centerX.Value,app.centerY.Value];
                    app.params.apCenter=app.params.center0;
                    app.params.apRadius=app.params.radius;
                    app.params.rmax=app.params.max_dist;
                    app.transRad.Value = app.params.radius;
                    app.params.mrad_per_pix=app.alpha.Value/app.params.radius; app.transCal.Value = 1/app.params.mrad_per_pix;
                    app.apX.Limits=[0 app.params.rmax];
                    app.apY.Limits=[-pi pi];
                    app.scanRot.Limits=[-pi pi];
                    app.probeX.Value=round(app.params.framesx/2);app.probeY.Value=round(app.params.framesy/2);
                    app.probePosition.Value = (app.probeY.Value-1)*app.params.framesx + app.probeX.Value;
                    
                    
                    % Enable GUI options and set limits/values for things like
                    % slider bars, numeric fields, etc.
                    set(app.transBeamX,'Limits',[-app.params.rmax,app.params.rmax],'Value',0);
                    set(app.transBeamY,'Limits',[-app.params.rmax,app.params.rmax],'Value',0);
                    set(app.transBeamRadius,'Limits',[0,app.params.rmax],'Value',app.params.radius);
                    set(app.probePosition,'Limits',[1,app.params.frames]);
                    set(app.adfInner,'Limits',[0,app.params.rmax],'Value',app.params.radius);app.adfInnerField.Value=app.adfInner.Value*app.params.mrad_per_pix;
                    set(app.adfOuter,'Limits',[0,app.params.rmax],'Value',app.params.rmax/2);app.adfOuterField.Value=app.adfOuter.Value*app.params.mrad_per_pix;
                    set(app.detAngle,'Limits',[-pi,pi],'Value',app.detAngleField.Value*pi/180);app.detAngleField.Value=app.detAngle.Value*180/pi;
                    set(app.diffControlGrid.Children,'Enable','on');
                    set(app.detectorPanel.Children,'Enable','on');
                    set(app.detectorTypeButtonGroup.Children,'Enable','on')
                    app.liveUpdate.Enable='on';
                    app.transBeamAlign.Enable='on';
                    app.alignScanRot.Enable='on';
                    app.alpha.Enable='on';app.conv_angle_label.Enable='on';
                    app.displayImagesButton.Enable='on';
                    app.saveImagesButton.Enable='on';
                    app.pacbedRadio.Enable='on';
                    app.roiRadio.Enable='on';
                    set(app.brightnessPanel.Children,'Enable','on');
                    app.ImageDropDown.Enable='on';
                    app.imColormap.Enable='on';
                    app.invertColors.Enable='on';
                    
                    % draw annular detectors
                    drawDetectors(app)
                    
                    % Make colorwheel for DPC/COM imaging - this color scheme will
                    % stay constant for all DPC/COM images regardless of their
                    % individual parameters like scan or detector rotation for
                    % consistency
                    width=app.params.nopix;cw_radius=width/2;
                    [xgrid, ygrid] = meshgrid(1:width, 1:width);
                    a=atan2(ygrid-app.centerY.Value,xgrid-app.centerX.Value);       % Get atan from -pi to pi
                    a = a .* (a >= 0) + (a + 2 * pi) .* (a < 0);        % shift the negative values of atan up by 2pi
                    app.images.colorWheel=a;
                    angles=0:pi/100:2*pi;
                    imagesc(app.colorwheelPlot,app.images.colorWheel);
                    colormap(app.colorwheelPlot,hsv(512));
                    set(app.colorwheelPlot,'NextPlot','add');
                    fill(app.colorwheelPlot,[cos(angles)*cw_radius+cw_radius,width,width,0,0,width],[sin(angles)*cw_radius+cw_radius,cw_radius,0,0,width,width],'k');
                    set(app.colorwheelPlot,'DataAspectRatio',[1 1 1],'XTick',[],'Ytick',[],'XLim',[0 width],'YLim',[0 width],'YDir','reverse');
                    set(app.colorwheelPlot,'NextPlot','replace');
                    colorbar(app.colorwheelPlot,'off')
                    app.colorwheelPlot.Toolbar.Visible = 'off';
                    
                    % Bring brightness/contrast/gamma and calibration tabs
                    % back to the GUI
                    app.calibrationTab.Parent = app.alignmentPanel;
                    app.brightnessContrastTab.Parent = app.controlPanel;
                    app.controlPanel.SelectedTab = app.detectorsTab;
                    
                    % Setup the initial brightness/contrast/gamma values
                    imageControls(app, event)
                    
                    % Set up the initial detector (default to Annular/Round)
                    detectorType(app,event)
                    
                    % Close status bar
                    close(import_bar)
                end
            end
            app.Quant4D_Fig.Interruptible = "on";
        end

        % Callback function: alignScanRot, alpha, autoAlignButton, 
        % scanRot, scanRot, scanRotInput, scanRotMinus, 
        % scanRotMirror, scanRotPlus, scanRotReset, transBeamAlign, 
        % transBeamRadius, transBeamRadius, transBeamRadiusMinus, 
        % transBeamRadiusPlus, transBeamX, transBeamX, 
        % transBeamXminus, transBeamXplus, transBeamY, transBeamY, 
        % transBeamYminus, transBeamYplus
        function alignment(app, event)
            
            switch event.Source
                case app.transBeamAlign % "Align Transmitted Beam" button
                    switch app.transBeamAlign.Value
                        case 0 % Finish alignment
                            set(app.detectorPanel.Children,'Enable','on');
                            set(app.transBeamPanel.Children,'Enable','off');
                            set(app.diffControlGrid.Children,'Enable','on');
                            set(app.detectorTypeButtonGroup.Children,'Enable','on');
                            app.autoAlignButton.Visible='off';
                            app.manualCalButton.Visible='off';
                            app.transBeamAlign.Text='Align Transmitted Beam';
                            app.displayImagesButton.Enable='on';
                            app.alpha.Enable='on';app.conv_angle_label.Enable='on';
                            app.alignScanRot.Enable='on';
                            app.importDataButton.Enable='on';
                            app.transBeamAlign.Enable='on';
                            set(app.adfInner,'Limits',[0,app.params.rmax]);app.adfInnerField.Value=app.adfInner.Value*app.params.mrad_per_pix;
                            set(app.adfOuter,'Limits',[0,app.params.rmax]);app.adfOuterField.Value=app.adfOuter.Value*app.params.mrad_per_pix;
                            set(app.detAngle,'Limits',[-pi,pi],'Value',deg2rad(app.detAngleField.Value));
                            
                            if isempty([app.centerX.Value,app.centerY.Value])
                                app.centerX.Value = app.params.nopix / 2;
                                app.centerY.Value = app.params.nopiy / 2;
                            end
                            
                            % Rerun the ADF integration based on the newly aligned
                            % location of the transmitted disk
                            if ~all((app.params.prev_center-[app.centerX.Value,app.centerY.Value])==0)
                                import_bar = uiprogressdlg(app.Quant4D_Fig,'Title','','Message',sprintf('Performing radial integration... Please Wait\n'),'Indeterminate',"on");
                                import_bar = integrateADF(app,import_bar);
                                close(import_bar)
                            end
                            
                            detectorType(app,event);
                            
                            % hide the transmitted disk circle
                            try app.annotations.disk_edge.Visible=false;catch;end
                        case 1 % Start alignment
                            app.autoAlignButton.Visible='on';
                            %app.manualCalButton.Visible='on';
                            app.transBeamAlign.Text='Finish Alignment';
                            try app.annotations.disk_edge.Visible = false;catch;end
                            
                            set(app.detectorTypeButtonGroup.Children,'Enable','off');
                            set(app.detectorPanel.Children,'Enable','off')
                            set(app.transBeamPanel.Children,'Enable','on')
                            app.transBeamAlign.Enable='on';
                            app.importDataButton.Enable='off';
                            app.pacbedRadio.Enable='on';
                            app.roiRadio.Enable='on';
                            app.alpha.Enable='on';app.conv_angle_label.Enable='on';
                            app.displayImagesButton.Enable='off';
                            app.alignScanRot.Enable='off';
                            app.importDataButton.Enable='off';
                            
                            % Record previous transmitted disk location to see if
                            % the ADF integration needs to be performed again
                            app.params.prev_center = [app.centerX.Value,app.centerY.Value];
                            
                            % show transmitted disk
                            try app.annotations.disk_edge.Visible = true;catch;end
                    end
                
                case app.alignScanRot
                    % Align scan rotation on the diffraction pattern
                    switch app.alignScanRot.Value
                        case 0 % Button off
                            % Change button text
                            app.alignScanRot.Text='Align Scan Direction';
                            
                            % Delete any annotations on the diffraction pattern
                            clearDetectors(app)
                            
                            % Re-enable most GUI options
                            app.displayImagesButton.Enable='on';
                            set(app.detectorPanel.Children,'Enable','on')
                            set(app.transBeamPanel.Children,'Enable','off')
                            set(app.scanRotPanel.Children,'Enable','off')
                            app.alpha.Enable='on';app.conv_angle_label.Enable='on';
                            set(app.detectorTypeButtonGroup.Children,'Enable','on');
                            app.transBeamAlign.Enable='on';
                            app.importDataButton.Enable='on';
                            
                            % Check which type of detector is currently selected
                            detectorType(app,event);
                        case 1 % Button on
                            % Disable most options in the GUI, enable the few that
                            % may be useful for aligning scan rotation
                            set(app.detectorPanel.Children,'Enable','off')
                            set(app.transBeamPanel.Children,'Enable','off')
                            set(app.scanRotPanel.Children,'Enable','on')
                            set(app.detectorTypeButtonGroup.Children,'Enable','off');
                            app.transBeamAlign.Enable='off';
                            app.importDataButton.Enable='off';
                            app.pacbedRadio.Enable='on';
                            app.roiRadio.Enable='on';
                            app.alpha.Enable='on';app.conv_angle_label.Enable='on';
                            app.displayImagesButton.Enable='off';
                            
                            % Change button text
                            app.alignScanRot.Text='Finish Alignment';
                            
                            clearDetectors(app);
                            app.diffPattern.NextPlot='add';
                            %scan_rot_Callback(app,event);
                    end
                    
                case app.alpha
                    % Reset the scaling factor in mrad/pix and the max
                    % radius size allowed
                    app.params.mrad_per_pix=app.alpha.Value/app.params.radius;
                    app.params.rmax=floor(sqrt((app.params.nopiy-app.centerX.Value).^2+(app.params.nopix-app.centerY.Value).^2));
                    
                    % Modify inner/outer limits for ADF
                    app.adfInner.Limits=[0,app.params.rmax]; app.adfInnerField.Value=app.adfInner.Value*app.params.mrad_per_pix;
                    app.adfOuter.Limits=[0,app.params.rmax]; app.adfOuterField.Value=app.adfOuter.Value*app.params.mrad_per_pix;
                    
                    % update "transmitted disk radius" field on "Calibration" tab
                    switch app.transmittedDiskRadius.SelectedObject
                        case app.transRadInvA
                            app.transRad.Value = mrad2invA(app,app.alpha.Value,'mrad'); 
                        case app.transRadMrad
                            app.transRad.Value = app.alpha.Value; 
                    end
                    
                    % update "diffraction calibration" field on "Calibration" tab
                    switch app.diffractionCalibration.SelectedObject
                        case app.invAButton
                            app.transCal.Value = app.params.radius/mrad2invA(app,app.alpha.Value,'mrad');
                        case app.mradButton
                            app.transCal.Value = app.params.radius/app.alpha.Value;
                    end
                    
                case app.transBeamX % x translate slider
                    app.centerX.Value = app.params.center0(1) + event.Value;
                    
                case app.transBeamY % y translate slider
                    app.centerY.Value = app.params.center0(2) - event.Value;
                    
                case app.transBeamRadius % radius size slider
                    app.params.radius=event.Value;
                    app.params.mrad_per_pix=app.alpha.Value/app.params.radius;
                    
                case app.transBeamXplus % x plus button
                    app.centerX.Value = app.centerX.Value + 0.25;
                    app.transBeamX.Value=app.transBeamX.Value+0.25;
                    
                case app.transBeamXminus % x minus button
                    app.centerX.Value = app.centerX.Value - 0.25;
                    app.transBeamX.Value=app.transBeamX.Value-0.25;
                    
                case app.transBeamYplus % y plus button
                    app.centerY.Value = app.centerY.Value - 0.25;
                    app.transBeamY.Value=app.transBeamY.Value+0.25;
                    
                case app.transBeamYminus % y minus button
                    app.centerY.Value = app.centerY.Value + 0.25;
                    app.transBeamY.Value=app.transBeamY.Value-0.25;
                    
                case app.transBeamRadiusPlus % radius plus button
                    app.params.radius=app.params.radius+0.25;
                    app.transBeamRadius.Value=app.transBeamRadius.Value+0.25;
                    
                case app.transBeamRadiusMinus % radius minus button
                    app.params.radius=app.params.radius-0.25;
                    app.transBeamRadius.Value=app.transBeamRadius.Value-0.25;
                    
                case app.autoAlignButton
                    import_bar = uiprogressdlg(app.Quant4D_Fig,'Title','Auto Align Transmitted Beam...','Message','Preparing','Indeterminate','on');
                    import_bar = autoAlign(app,event,import_bar); %#ok<*NASGU>
                    app.transBeamAlign.Value = 0;
                    tmp.Source = app.transBeamAlign;
                    alignment(app,tmp);

                case app.scanRot % scan rotation slider
                    app.scanRot.Value=event.Value;
                    app.scanRotInput.Value=rad2deg(app.scanRot.Value);
                
                case app.scanRotPlus % scan rotation plus button - 4 degree increments
                    app.scanRot.Value=(app.scanRot.Value+deg2rad(4))-2*pi.*((app.scanRot.Value+deg2rad(4))>180);
                    app.scanRotInput.Value=rad2deg(app.scanRot.Value);
                
                case app.scanRotMinus % scan rotation minus button 4 degree increments
                    app.scanRot.Value=(app.scanRot.Value-deg2rad(4))+2*pi.*((app.scanRot.Value-deg2rad(4))<-180);
                    app.scanRotInput.Value=rad2deg(app.scanRot.Value);
                
                case app.scanRotInput % scan rotation numerical field
                    app.scanRot.Value=deg2rad(event.Value);
                    
                case app.scanRotReset
                    app.scanRot.Value = 0;
                    app.scanRotInput.Value = 0;

            end
            
            % update the circle object properties
            try app.annotations.disk_edge.Center = [app.centerX.Value app.centerY.Value];catch;end
            try app.annotations.disk_edge.Radius = app.params.radius;catch;end
            
            
            if app.alignScanRot.Value % only replot scan direction vectors if in scan rotation alignment mode
               scanRotation(app);
            else
                % set a maximum radius to the nearest corner of the diffraction pattern
                app.params.rmax=floor(sqrt((app.params.nopiy-app.centerX.Value).^2+(app.params.nopix-app.centerY.Value).^2));

                % set initial virtual aperture size to that of the condenser aperture
                app.params.apRadius=app.params.radius;
                
                % delete any old disk outlines, plot new/updated one if in alignment mode
                if app.transBeamAlign.Value
                    clearDetectors(app);
                    app.annotations.disk_edge.Visible = true;
                else
                    app.annotations.disk_edge.Visible = false;
                end
            end
            
        end

        % Callback function: diffPatternGroup, dpLog, negativeROI, 
        % probePosition, probePosition, probeX, probeX, probeY, 
        % probeY, roiButtonGroup
        function patternViewer(app, event)
            XLim_temp=app.diffPattern.XLim;
            YLim_temp=app.diffPattern.YLim;
            switch event.Source
                case {app.diffPatternGroup;app.roiButtonGroup}
                    try delete(app.annotations.bfdfROI);catch;end
                    try delete(app.annotations.comxROI);catch;end
                    try delete(app.annotations.comyROI);catch;end
                    try delete(app.annotations.comMagROI);catch;end
                    try delete(app.annotations.comPhaseROI);catch;end
                    switch app.diffPatternGroup.SelectedObject
                        case app.pacbedRadio % PACBED
                            app.probePosition.Visible='off';app.probePositionLabel.Visible='off';
                            app.probeX.Visible='off';app.probeY.Visible='off';
                            app.params.markerStatus = 0;
                            set(app.roiButtonGroup.Children,'Enable','off');
                            % delete everything but the axis and the BF/DF image
                            delete(findall(app.bfdfPlot,'-not','Type','axes','-not','Type','Image'));
                        case app.roiRadio % user-defined ROI
                            switch app.roiButtonGroup.SelectedObject
                                case app.roiPoint
                                    app.probeX.Visible='on';app.probeY.Visible='on';
                                    app.probePosition.Visible='on';app.probePositionLabel.Visible='on';
                                    app.probeX.Limits=[1 app.params.framesx];app.probeY.Limits=[1 app.params.framesy];
                                otherwise
                                    app.probeX.Visible='off';app.probeY.Visible='off';
                                    app.probePosition.Visible='off';app.probePositionLabel.Visible='off';
                            end
                            app.params.markerStatus = 0;
                            set(app.roiButtonGroup.Children,'Enable','on');
                            drawROI(app,event);
                    end
                    
                case app.probePosition % Slider bar
                    app.probeX.Value=mod(round(event.Value),app.params.framesy)+app.params.framesy.*(mod(round(event.Value),app.params.framesy)==0);
                    app.probeY.Value=floor(round(event.Value)/app.params.framesy)+1.*(mod(round(event.Value),app.params.framesy)~=0);
                    app.probePosition.Value=event.Value;
                    
                case app.probeX % Up/down arrows for x
                    app.probePosition.Value = (app.probeY.Value-1)*app.params.framesx + event.Value;
                    app.probeX.Value = event.Value;
                    
                case app.probeY % Up/down arrows for y
                    app.probePosition.Value = (event.Value-1)*app.params.framesx + app.probeX.Value;
                    app.probeY.Value = event.Value;
                    
                case app.negativeROI
                    % generate a mask for displaying pacbed pattern
                    app.mask.pacbed = 1-app.mask.pacbed;
                    
                    % redefine pacbed pattern for the specified ROI
                    app.images.pacbed = gather(reshape(app.data*app.mask.pacbed(:),[app.params.nopix app.params.nopiy]))/(sum(app.mask.pacbed(:)));
            end
            
            % See whether the user has selected to view the PACBED pattern
            % or to see each diffraction pattern individually
            if app.roiRadio.Value && app.roiPoint.Value
                % redefine pacbed image as individual cbed pattern from the
                % given probe position
                app.annotations.bfdfROI.Position = [app.probeX.Value,app.probeY.Value];
                
                % negative ROI?
                if app.negativeROI.Value
                    app.images.pacbed = double(gather(reshape(sum(app.data,2),[app.params.nopix app.params.nopiy])-reshape(app.data(:,round(app.probePosition.Value)),[app.params.nopix app.params.nopiy])))/(numel(app.mask.pacbed)-1);
                else
                    app.images.pacbed = double(gather(reshape(app.data(:,round(app.probePosition.Value)),[app.params.nopix app.params.nopiy])));
                end

            elseif app.pacbedRadio.Value
                % define pacbed image as sum of all cbed patterns
                app.images.pacbed = double(gather(reshape(sum(app.data,2),[app.params.nopix app.params.nopiy])));
            end
            
            % plot pacbed pattern
            plotImage(app,'pacbed');
                
            % Plot detector or transmitted disk outline on diffraction pattern
                switch app.transBeamAlign.Value
                    case 0 % Alignment off
                        plotDetector(app,event);
                    case 1 % Alignment on
                        try app.annotations.disk_edge.Visible = true;catch;end
                end
        end

        % Selection changed function: detectorTypeButtonGroup
        function detectorType(app, event)
            clearPlots(app);
            app.displayImagesButton.Enable='on';

            switch event.Source
                case app.detectorTypeButtonGroup
                    switch app.detectorTypeButtonGroup.SelectedObject
                        case app.dpc
                            app.comTab.Title = 'Differential Phase Contrast';
                            buttons = findall(app.comTab,'Type','uiToggleButton');
                            for ii=1:size(buttons,1)
                                buttons(ii).Text = strrep(buttons(ii).Text,'CoM','DPC');
                            end
                            app.comTab.Parent=app.outputPanel;
                            app.vectorFieldTab.Parent=app.outputPanel;
                            app.virtualApertureTab.Parent=[];
                            app.colorwheelTab.Parent=app.alignmentPanel;
                            app.outputPanel.SelectedTab=app.comTab;
                            set(app.virtualAperturePanel.Children,'Enable','off');
                            set(app.detectorPanel.Children,'Enable','on');
                            set(app.detRotPanel.Children,'Enable','on');
                            app.alignmentPanel.SelectedTab=app.colorwheelTab;
                            app.cartesianRadio.Enable='off';app.polarRadio.Enable='off';
                            app.apertureSymmetry.Enable='off';
                            set(app.virtualAperturePanel.Children,'Enable','off');
                            set(app.mirrorPanel.Children,'Enable','off');
                            app.ImageDropDown.Items={'Diffraction Pattern';
                                                     'BF/DF';
                                                     'DPC X';
                                                     'DPC Y';
                                                     'DPC Magnitude';
                                                     'dDPC';
                                                     'iDPC'};
                            app.ImageDropDown.ItemsData={'pacbed';
                                                         'adf';
                                                         'comx';
                                                         'comy';
                                                         'comMag';
                                                         'dcom';
                                                         'icom'};
                        case app.adf
                            app.displayImagesButton.Enable='off';
                            set(app.detectorPanel.Children,'Enable','on');
                            set(app.mirrorPanel.Children,'Enable','off');
                            set(app.detRotPanel.Children,'Enable','off');
                            app.outputPanel.SelectedTab=app.bfdfTab;
                            app.cartesianRadio.Enable='off';app.polarRadio.Enable='off';
                            app.apertureSymmetry.Enable='off';
                            set(app.virtualAperturePanel.Children,'Enable','off');
                            app.outputPanel.SelectedTab=app.bfdfTab;
                            app.alignmentPanel.SelectedTab=app.alignmentTab;
                            app.ImageDropDown.Items={'Diffraction Pattern';
                                                     'BF/DF'};
                            app.ImageDropDown.ItemsData={'pacbed';
                                                         'adf'};
                            app.comTab.Parent=[];
                            app.vectorFieldTab.Parent=[];
                            app.virtualApertureTab.Parent=[];
                            app.colorwheelTab.Parent=[];
                        case app.vdf
                            if isempty(app.params.apRadius) app.params.apRadius = app.params.radius; end
                            app.virtualApertureTab.Parent=app.alignmentPanel;
                            set(app.detectorPanel.Children,'Enable','off');
                            set(app.detRotPanel.Children,'Enable','off');
                            set(app.mirrorPanel.Children,'Enable','off');
                            set(app.coordinatesButtonGroup.Children,'Enable','on');
                            app.apertureSymmetry.Enable='on';
                            app.apMirror.Enable='on';
                            app.outputPanel.SelectedTab=app.bfdfTab;
                            app.alignmentPanel.SelectedTab=app.virtualApertureTab;
                            set(app.virtualAperturePanel.Children,'Enable','on');
                            set(app.apSize,'Limits',[0 app.params.rmax],'Value',app.params.radius)
                            set(app.apSizeField,'Limits',app.apSize.Limits*app.params.mrad_per_pix,'Value',app.apSize.Value*app.params.mrad_per_pix);
                            app.ImageDropDown.Items={'Diffraction Pattern';
                                                     'BF/DF'};
                            app.ImageDropDown.ItemsData={'pacbed';
                                                         'adf'};
                            app.comTab.Parent=[];
                            app.vectorFieldTab.Parent=[];
                            app.colorwheelTab.Parent=[];
                        case app.com
                            app.comTab.Title = 'Center of Mass';
                            buttons = findall(app.comTab,'Type','uiToggleButton');
                            for ii=1:size(buttons,1)
                                buttons(ii).Text = strrep(buttons(ii).Text,'DPC','CoM');
                            end
                            app.comTab.Parent=app.outputPanel;
                            app.vectorFieldTab.Parent=app.outputPanel;
                            app.virtualApertureTab.Parent=[];
                            app.colorwheelTab.Parent=app.alignmentPanel;
                            app.outputPanel.SelectedTab=app.comTab;
                            set(app.detectorPanel.Children,'Enable','on');
                            set(app.detRotPanel.Children,'Enable','off');
                            app.alignmentPanel.SelectedTab=app.colorwheelTab;
                            app.ImageDropDown.Items={'Diffraction Pattern';
                                                     'BF/DF';
                                                     'COM X';
                                                     'COM Y';
                                                     'COM Magnitude';
                                                     'dCoM';
                                                     'iCoM'};
                            app.ImageDropDown.ItemsData={'pacbed';
                                                         'adf';
                                                         'comx';
                                                         'comy';
                                                         'comMag';
                                                         'dcom';
                                                         'icom'};
                    end
            end
            % replot new set of detectors            
            plotDetector(app, event);
            
            % 
            if app.dpc.Value || app.com.Value
                integrateMasks(app);
                displayCoM(app);
            end
            
            % Plot ADF image
            plotImage(app,'adf');
            
            imageControls(app, event);
            
        end

        % Callback function: adfInner, adfInner, adfInnerField, 
        % adfInnerMinus, adfInnerPlus, adfOuter, adfOuter, 
        % adfOuterField, adfOuterMinus, adfOuterPlus, detAngle, 
        % detAngle, detAngleField, detAngleReset, detRotMinus, 
        % detRotPlus, linkADF, nrung, nseg
        function annularDetector(app, event)
            switch event.Source
                case app.adfInnerMinus % adf inner angle minus button
                    if app.adfInner.Value-0.25<0
                        app.adfInner.Value=0;
                        app.adfInnerField.Value=0;
                    else
                        app.adfInner.Value=app.adfInner.Value-0.25;
                        app.adfInnerField.Value=app.adfInnerField.Value-0.25*app.params.mrad_per_pix;
                    end
                case app.adfInnerPlus % adf inner angle plus button
                    if app.adfInner.Value+0.25<app.adfOuter.Value
                        app.adfInner.Value=app.adfInner.Value+0.25;
                        app.adfInnerField.Value=app.adfInnerField.Value+0.25*app.params.mrad_per_pix;
                    else
                        app.adfInner.Value=app.adfOuter.Value;
                        app.adfInnerField.Value=app.adfOuterField.Value;
                    end
                case app.adfInner % adf inner angle slider
                    if event.Value>app.adfOuter.Value && ~app.linkADF.Value
                        app.adfInner.Value=app.adfOuter.Value;
                    else
                        app.adfInner.Value = event.Value;
                    end
                    app.adfInnerField.Value=app.adfInner.Value*app.params.mrad_per_pix;
                case app.adfInnerField % adf inner angle numerical field
                    if event.Value>app.adfOuterField.Value && ~app.linkADF.Value
                        app.adfInnerField.Value=app.adfOuterField.Value;
                        app.adfInner.Value=app.adfOuter.Value;
                    elseif app.linkADF.Value && event.Value>app.adfOuter.Limits(2)-app.params.detWidth
                        app.adfInner.Value = app.adfOuter.Limits(2)-app.params.detWidth;
                        app.adfInnerField.Value = app.adfInner.Value*app.params.mrad_per_pix;
                    elseif event.Value<0
                        app.adfInnerField.Value=0;
                        app.adfInner.Value=0;
                    else
                        app.adfInnerField.Value = event.Value;
                        app.adfInner.Value=event.Value/app.params.mrad_per_pix;
                    end
                case app.adfOuterMinus % adf outer angle minus button
                    if app.adfOuter.Value-0.25>=app.adfInner.Value
                        app.adfOuter.Value=app.adfOuter.Value-0.25;
                        app.adfOuterField.Value=app.adfOuterField.Value-0.25*app.params.mrad_per_pix;
                    else
                        app.adfOuter.Value=app.adfInner.Value;
                        app.adfOuterField.Value=app.adfInnerField.Value;
                    end
                case app.adfOuterPlus % adf outer angle plut button
                    if app.adfOuter.Value+0.25<app.params.rmax
                        app.adfOuter.Value=app.adfOuter.Value+0.25;
                        app.adfOuterField.Value=app.adfOuterField.Value+0.25*app.params.mrad_per_pix;
                    else
                        app.adfOuter.Value=app.params.rmax;
                        app.adfOuterField.Value=app.params.rmax*app.params.mrad_per_pix;
                    end
                case app.adfOuter % adf outer angle slider
                    if event.Value<app.adfInner.Value && ~app.linkADF.Value
                        app.adfOuter.Value=app.adfInner.Value;
                    else
                        app.adfOuter.Value = event.Value;
                    end
                    app.adfOuterField.Value=app.adfOuter.Value*app.params.mrad_per_pix;
                case app.adfOuterField % adf outer angle numerical field
                    if event.Value>app.params.rmax*app.params.mrad_per_pix
                        app.adfOuterField.Value=app.adfOuter.Value*app.params.mrad_per_pix;
                        app.adfOuter.Value=app.params.rmax;
                    elseif app.linkADF.Value && event.Value<app.adfInner.Limits(1)+app.params.detWidth
                        app.adfOuter.Value = app.adfInner.Limits(1)+app.params.detWidth;
                        app.adfOuterField.Value = app.adfOuter.Value*app.params.mrad_per_pix;
                    elseif event.Value<app.adfInnerField.Value && ~app.linkADF.Value
                        app.adfOuter.Value=app.adfInner.Value;
                        app.adfOuterField.Value=app.adfInner.Value*app.params.mrad_per_pix;
                    else
                        app.adfOuter.Value=event.Value/app.params.mrad_per_pix;
                    end
                case app.detAngle
                    app.detAngle.Value=event.Value;
                    app.detAngleField.Value=rad2deg(app.detAngle.Value);
                case app.detAngleField
                    app.detAngleField.Value=app.detAngleField.Value+...
                        360.*(app.detAngleField.Value<-180)-...
                        360.*(app.detAngleField.Value>180);
                    app.detAngle.Value=deg2rad(event.Value);
                case app.detRotMinus
                    app.detAngleField.Value=app.detAngleField.Value-0.25+...
                        360.*(app.detAngleField.Value-0.25<-180);
                    app.detAngle.Value=deg2rad(app.detAngleField.Value);
                case app.detRotPlus
                    app.detAngleField.Value=app.detAngleField.Value+0.25+...
                        360.*(app.detAngleField.Value+0.25>180);
                    app.detAngle.Value=deg2rad(app.detAngleField.Value);
                case app.detAngleReset
                    app.detAngle.Value = 0;
                    app.detAngleField.Value = 0;
                case app.nseg
                    app.nseg.Value=round(event.Value);
                    drawDetectors(app);
                case app.nrung
                    app.nrung.Value = round(event.Value);
                    drawDetectors(app);
            end
            
            if app.linkADF.Value
                switch event.Source
                    case {app.adfInner,app.adfInnerField,app.adfInnerPlus,app.adfInnerMinus}
                        if app.adfInner.Value+app.params.detWidth <= app.adfOuter.Limits(2)
                            app.adfOuter.Value = app.adfInner.Value+app.params.detWidth;
                            app.adfOuterField.Value = app.adfOuter.Value * app.params.mrad_per_pix;
                        else
                            app.adfOuter.Value = app.adfOuter.Limits(2);
                            app.adfOuterField.Value = app.adfOuter.Value * app.params.mrad_per_pix;
                            app.adfInner.Value = app.adfOuter.Limits(2)-app.params.detWidth;
                            app.adfInnerField.Value = app.adfInner.Value * app.params.mrad_per_pix;
                        end
                    case {app.adfOuter,app.adfOuterField,app.adfOuterPlus,app.adfOuterMinus}
                        if app.adfOuter.Value-app.params.detWidth >= app.adfInner.Limits(1)
                            app.adfInner.Value = app.adfOuter.Value-app.params.detWidth;
                            app.adfInnerField.Value = app.adfInner.Value * app.params.mrad_per_pix;
                        else
                            app.adfInner.Value = app.adfOuter.Limits(1);
                            app.adfInnerField.Value = app.adfInner.Value * app.params.mrad_per_pix;
                            app.adfOuter.Value = app.adfInner.Limits(1)+app.params.detWidth;
                            app.adfOuterField.Value = app.adfOuter.Value * app.params.mrad_per_pix;
                        end
                end
            end
            
            % update detectors and plot image
            moveDetectors(app,event.Source,event);
        end

        % Callback function: apMirror, apMirrorAngle, apMirrorAngle, 
        % apMirrorInput, apMirrorMinus, apMirrorPlus, 
        % apMirrorReset, apNegative, apRotAngle, apRotLeft, 
        % apRotRight, apSize, apSize, apSizeField, apSizeMinus, 
        % apSizePlus, apX, apX, apXField, apXMinus, apXPlus, 
        % apXReset, apY, apY, apYField, apYMinus, apYPlus, 
        % apYReset, apertureSymmetry, coordinatesButtonGroup
        function virtualAperture(app, event)
            % Drop down value
            rot_value=deg2rad(str2double(app.apRotAngle.Value));
            
            switch event.Source
                case app.coordinatesButtonGroup % radio button group to swtich between polar and cartesian coordinates
                    switch app.coordinatesButtonGroup.SelectedObject
                        case app.cartesianRadio
                            app.DistanceLabel.Text='X';
                            app.RotationLabel.Text='Y';
                            app.aperture_y_Label.Text='mrad';
                            
                            app.apX.Limits=[-app.params.nopix/2 app.params.nopix/2];
                            app.apXField.Limits=app.apX.Limits*app.params.mrad_per_pix;
                            app.apX.Value=app.apX.Value*cos(app.apY.Value);
                            app.apXField.Value=app.apX.Value*app.params.mrad_per_pix;
                            
                            app.apY.Limits=[-app.params.nopiy/2 app.params.nopiy/2];
                            app.apYField.Limits=app.apY.Limits*app.params.mrad_per_pix;
                            app.apY.Value=app.apX.Value*sin(app.apY.Value);
                            app.apYField.Value=app.apY.Value*app.params.mrad_per_pix;
                            
                        case app.polarRadio
                            app.DistanceLabel.Text='Distance';
                            app.RotationLabel.Text='Rotation';
                            app.aperture_y_Label.Text='°';
                            
                            app.apX.Limits=[0 app.params.nopix/2];
                            app.apXField.Limits=app.apX.Limits*app.params.mrad_per_pix;
                            app.apX.Value=min(sqrt(sum((app.params.apCenter-[app.centerX.Value,app.centerY.Value]).^2)),app.apX.Limits(2));
                            app.apXField.Value=app.apX.Value*app.params.mrad_per_pix;
                            
                            app.apY.Limits=[-pi pi];
                            app.apYField.Limits=rad2deg(app.apY.Limits);
                            app.apY.Value=atan2(app.params.apCenter(2)-app.centerY.Value,app.params.apCenter(1)-app.centerX.Value);
                            app.apYField.Value=rad2deg(app.apY.Value);
                    end
                    
                case app.apSize % aperture size slider
                    app.params.apRadius=event.Value;
                    app.apSizeField.Value=event.Value*app.params.mrad_per_pix;
                    
                case app.apSizeField % aperture size numerical field
                    if (app.apSizeField.Value/app.params.mrad_per_pix>=app.apSize.Limits(1)) && (app.apSizeField.Value/app.params.mrad_per_pix<=app.apSize.Limits(2))
                        app.apSize.Value=event.Value/app.params.mrad_per_pix;
                        app.params.apRadius=app.apSize.Value;
                    else % out of bounds, move to nearest bound
                        [~,indexOf]=min(sqrt((app.ap_size_input.Value/app.params.mrad_per_pix-app.apSize.Limits).^2));
                        app.apSize.Value=app.apSize.Limits(indexOf);
                        app.ap_size_input.Value=app.apSize.Limits(indexOf);
                    end
                    
                case app.apSizePlus % apperture size+ button
                    app.params.apRadius=app.params.apRadius+0.25.*(app.apSize.Value+0.25<=app.apSize.Limits(2));
                    app.apSize.Value=app.apSize.Value+0.25.*(app.apSize.Value+0.25<=app.apSize.Limits(2));
                    
                case app.apSizeMinus % aperture size- button
                    app.params.apRadius=app.params.apRadius-0.25.*(app.apSize.Value-0.25>=0);
                    app.apSize.Value=app.apSize.Value-0.25.*(app.apSize.Value-0.25>0);
                    
                case app.apertureSymmetry % aperture symmetry number spinner
                    % On symmetry # change (ignore symmetry value of 5)
                    clearDetectors(app);
                    if event.Value==5 && event.PreviousValue<5
                        app.apertureSymmetry.Value=6;
                    elseif event.Value==5 && event.PreviousValue==6
                        app.apertureSymmetry.Value=4;
                    end
                    
                case app.apMirror% mirror aperture(s) checkbox
                    switch app.apMirror.Value
                        case 0 % Unchecked
                            set(app.mirrorPanel.Children,'Enable','off');
                            %try delete(app.annotations.mirror_line);catch;end
                        case 1 % Checked
                            set(app.mirrorPanel.Children,'Enable','on');
                    end
                    
                case app.apMirrorAngle % mirror plane angle slider
                    app.apMirrorInput.Value=rad2deg(event.Value);
                    %try delete(app.annotations.mirror_line);catch;end
                    %app.diffPattern.NextPlot='add';
                    %app.annotations.mirror_line = plot(app.diffPattern,[1 app.params.nopix],tan(event.Value)*([1 app.params.nopix]-app.centerX.Value)+app.centerY.Value,'g--','LineWidth',2);
                    
                case app.apMirrorInput % mirror plan angle numerical input field
                    app.apMirrorAngle.Value=deg2rad(rem(event.Value,180)+180.*(event.Value<=-180)-180.*(event.Value>180));
                    %try delete(app.annotations.mirror_line);catch;end
                    %app.diffPattern.NextPlot='add';
                    %app.annotations.mirror_line = plot(app.diffPattern,[1 app.params.nopix],tan(app.apMirrorAngle.Value)*([1 app.params.nopix]-app.centerX.Value)+app.centerY.Value,'g--','LineWidth',2);
                    
                case app.apMirrorPlus % mirror plane right rotation button
                    app.apMirrorAngle.Value=app.apMirrorAngle.Value+deg2rad(0.5);
                    app.apMirrorInput.Value=app.apMirrorInput.Value+0.5;
                    
                case app.apMirrorMinus % mirror plane left rotation
                    app.apMirrorAngle.Value=app.apMirrorAngle.Value-deg2rad(0.5);
                    app.apMirrorInput.Value=app.apMirrorInput.Value-0.5;
                    
                case app.apMirrorReset % mirror plane reset button
                    app.apMirrorAngle.Value=0;
                    app.apMirrorInput.Value=0;
                    
                case app.apXField
                    if (event.Value/app.params.mrad_per_pix>=app.apX.Limits(1)) && (event.Value/app.params.mrad_per_pix<=app.apX.Limits(2))
                        app.apX.Value=app.apXField.Value/app.params.mrad_per_pix;
                    else %out of bounds, move to nearest bound
                        [~,indexOf] = min(sqrt((event.Value - app.apX.Limits/app.params.mrad_per_pix).^2));
                        app.apX.Value = app.apX.Limits(indexOf);
                        app.apXField.Value=app.apX.Limits(indexOf)*app.params.mrad_per_pix;
                    end
                    
                    
                otherwise % all of the buttons, sliders, numerical fields that change based on polar/cartesian selection
                    switch app.coordinatesButtonGroup.SelectedObject
                        case app.cartesianRadio
                            switch event.Source
                                case app.apX % x location slider
                                    app.params.apCenter=[app.centerX.Value,app.centerY.Value]+[event.Value app.apY.Value];
                                    app.apXField.Value=event.Value*app.params.mrad_per_pix;
                                    
                                case app.apY % y location slider
                                    app.params.apCenter=[app.centerX.Value,app.centerY.Value]+[app.apX.Value event.Value];
                                    app.apYField.Value=event.Value*app.params.mrad_per_pix;
                                    
                                case app.apXPlus % x+ button
                                    app.params.apCenter=app.params.apCenter+[0.25 0].*(app.apX.Value+0.25<=app.apX.Limits(2)); % && sqrt((app.apX.Value+0.2)^2+()^2)<=min(app.apX.Limit()
                                    app.apX.Value=app.apX.Value+0.25.*(app.apX.Value+0.25<=app.apX.Limits(2));
                                    
                                case app.apXMinus % x- button
                                    app.params.apCenter=app.params.apCenter-[0.25 0].*(app.apX.Value-0.25>=app.apX.Limits(1));
                                    app.apX.Value=app.apX.Value-0.25.*(app.apX.Value-0.25>=app.apX.Limits(1));
                                    
                                case app.apXReset % x0 button
                                    app.params.apCenter=[app.centerX.Value app.params.apCenter(2)];
                                    app.apX.Value=0;
                                    
                                case app.apYPlus % y+ button
                                    app.params.apCenter=app.params.apCenter+[0 0.25].*(app.apY.Value+0.25<=app.apY.Limits(2));
                                    app.apY.Value=app.apY.Value+0.25.*(app.apY.Value+0.25<=app.apY.Limits(2));
                                    
                                case app.apYMinus % y- button
                                    app.params.apCenter=app.params.apCenter-[0 0.25].*(app.apY.Value-0.25>=app.apY.Limits(1));
                                    app.apY.Value=app.apY.Value-0.25.*(app.apY.Value-0.25>=app.apY.Limits(1));
                                    
                                case app.apYReset % y0 button
                                    app.params.apCenter=[app.params.apCenter(1) app.centerY.Value];
                                    app.apY.Value=0;
                                    
                                case app.apRotLeft % left rotation button
                                    temp_rad=sqrt(sum((app.params.apCenter-[app.centerX.Value,app.centerY.Value]).^2)).*(sqrt(sum((app.params.apCenter-[app.centerX.Value,app.centerY.Value]).^2))<=min(app.apX.Limits(2),app.apY.Limits(2)))+...
                                        min(app.apX.Limits(2),app.apY.Limits(2)).*(sqrt(sum((app.params.apCenter-[app.centerX.Value,app.centerY.Value]).^2))>min(app.apX.Limits(2),app.apY.Limits(2)));
                                    temp_ang=atan2(app.params.apCenter(2)-app.centerY.Value,app.params.apCenter(1)-app.centerX.Value)-rot_value;
                                    app.apX.Value=temp_rad*cos(temp_ang);
                                    app.apY.Value=temp_rad*sin(temp_ang);
                                    app.params.apCenter=[app.centerX.Value,app.centerY.Value]+[app.apX.Value app.apY.Value];
                                    
                                case app.apRotRight % right rotation button
                                    temp_rad=sqrt(sum((app.params.apCenter-[app.centerX.Value,app.centerY.Value]).^2)).*(sqrt(sum((app.params.apCenter-[app.centerX.Value,app.centerY.Value]).^2))<=min(app.apX.Limits(2),app.apY.Limits(2)))+...
                                        min(app.apX.Limits(2),app.apY.Limits(2)).*(sqrt(sum((app.params.apCenter-[app.centerX.Value,app.centerY.Value]).^2))>min(app.apX.Limits(2),app.apY.Limits(2)));
                                    temp_ang=atan2(app.params.apCenter(2)-app.centerY.Value,app.params.apCenter(1)-app.centerX.Value)+rot_value;
                                    app.apX.Value=temp_rad*cos(temp_ang);
                                    app.apY.Value=temp_rad*sin(temp_ang);
                                    app.params.apCenter=[app.centerX.Value,app.centerY.Value]+[app.apX.Value app.apY.Value];
                                    
                                case app.apYField
                                    if (app.apYField.Value/app.params.mrad_per_pix>=app.apY.Limits(1)) && (app.apYField.Value/app.params.mrad_per_pix<=app.apY.Limits(2))
                                        app.apY.Value=app.apYField.Value/app.params.mrad_per_pix;
                                    else % out of bounds, move to nearest bound
                                        [~,indexOf]=min(sqrt((app.apY.Value/app.params.mrad_per_pix-app.apY.Limits).^2));
                                        app.apY.Value=app.apY.Limits(indexOf);
                                        app.apYField.Value=app.apY.Limits(indexOf)*app.params.mrad_per_pix;
                                    end
                            end
                        case app.polarRadio
                            switch event.Source
                                case app.apX % distance slider
                                    app.params.apCenter=[app.centerX.Value,app.centerY.Value]+event.Value*[cos(app.apY.Value) sin(app.apY.Value)];
                                    app.apXField.Value=event.Value*app.params.mrad_per_pix;
                                    
                                case app.apY % rotation slider
                                    app.params.apCenter=[app.centerX.Value,app.centerY.Value]+app.apX.Value*[cos(event.Value) sin(event.Value)];
                                    app.apYField.Value=rad2deg(event.Value);
                                    
                                case app.apXPlus % distance+ button
                                    app.apX.Value=app.apX.Value+0.25.*(app.apX.Value+0.25<=app.apX.Limits(2));
                                    app.params.apCenter=[app.centerX.Value,app.centerY.Value]+app.apX.Value*[cos(app.apY.Value) sin(app.apY.Value)];
                                    
                                case app.apXMinus % distance- button
                                    app.apX.Value=app.apX.Value-0.25.*(app.apX.Value-0.25>=0);
                                    app.params.apCenter=[app.centerX.Value,app.centerY.Value]+app.apX.Value*[cos(app.apY.Value) sin(app.apY.Value)];
                                    
                                case app.apXReset % distance0 button
                                    app.params.apCenter=[app.centerX.Value,app.centerY.Value];
                                    app.apX.Value=0;
                                    
                                case app.apYPlus % rotation+ button
                                    app.apY.Value=app.apY.Value+deg2rad(0.25)-range(app.apY.Limits).*(app.apY.Value+deg2rad(0.25)>app.apY.Limits(2));
                                    app.params.apCenter=[app.centerX.Value,app.centerY.Value]+app.apX.Value*[cos(app.apY.Value) sin(app.apY.Value)];
                                    
                                case app.apYMinus % rotation- button
                                    app.apY.Value=app.apY.Value-deg2rad(0.25)+range(app.apY.Limits).*(app.apY.Value-deg2rad(0.25)<app.apY.Limits(1));
                                    app.params.apCenter=[app.centerX.Value,app.centerY.Value]+app.apX.Value*[cos(app.apY.Value) sin(app.apY.Value)];
                                    
                                case app.apYReset % rotation0 button
                                    app.params.apCenter=[app.centerX.Value,app.centerY.Value]+[app.apX.Value 0];
                                    app.apY.Value=0;
                                    
                                case app.apRotLeft % left rotation button
                                    app.apY.Value=app.apY.Value-rot_value+2*pi.*(app.apY.Value-rot_value<-pi);
                                    app.params.apCenter=[app.centerX.Value,app.centerY.Value]+app.apX.Value*[cos(app.apY.Value) sin(app.apY.Value)];
                                    
                                case app.apRotRight % right rotation button
                                    app.apY.Value=app.apY.Value+rot_value-2*pi.*(app.apY.Value+rot_value>pi);
                                    app.params.apCenter=[app.centerX.Value,app.centerY.Value]+app.apX.Value*[cos(app.apY.Value) sin(app.apY.Value)];
                                    
                                case app.apYField
                                    if (deg2rad(app.apYField.Value)>=app.apY.Limits(1) && deg2rad(app.apYField.Value)<=app.apY.Limits(2))
                                        app.apY.Value=deg2rad(app.apYField.Value);
                                    else % out of bounds (-pi,pi] , move mod(input,360) to within bounds
                                        app.apY.Value=deg2rad(mod(app.apYField.Value,360))+2*pi.*(deg2rad(mod(app.apYField.Value,360))<-pi)-2*pi.*(deg2rad(mod(app.apYField.Value,360))>pi);
                                        app.apYField.Value=rad2deg(app.apY.Value);
                                    end
                            end
                    end
            end
            
            % update other fields based on the event that took place
            % (could go in each case above, but this is more compact)
            switch event.Source.Type
                case 'uibutton'
                    if app.cartesianRadio.Value
                        app.apXField.Value=app.apX.Value*app.params.mrad_per_pix;
                        app.apYField.Value=app.apY.Value*app.params.mrad_per_pix;
                        app.apSizeField.Value=app.apSize.Value*app.params.mrad_per_pix;
                    elseif app.polarRadio.Value
                        app.apXField.Value=app.apX.Value*app.params.mrad_per_pix;
                        app.apYField.Value=rad2deg(app.apY.Value);
                        app.apSizeField.Value=app.apSize.Value*app.params.mrad_per_pix;
                    end
                case 'uinumericeditfield'
                    if app.cartesianRadio.Value
                        app.params.apCenter = [app.centerX.Value,app.centerY.Value] + [app.apX.Value app.apY.Value];
                    elseif app.polarRadio.Value
                        app.params.apCenter = [app.centerX.Value,app.centerY.Value] + app.apX.Value*[cos(app.apY.Value) sin(app.apY.Value)];
                    end
            end
            
            %plotDetector(app,event);
            app.annotations.aperture(1).Radius = app.params.apRadius;
            app.annotations.aperture(1).Center = app.params.apCenter;
            moveApertures(app,event.Source,event);
            
            %if app.apMirror.Value && (event.Source ~= app.apMirrorAngle) % mirror plane enabled
            %    try delete(app.annotations.mirror_line);catch;end
            %    app.diffPattern.NextPlot='add';
            %    app.annotations.mirror_line = plot(app.diffPattern,[1 app.params.nopix],tan(app.apMirrorAngle.Value)*([1 app.params.nopix]-app.centerX.Value)+app.centerY.Value,'g--','LineWidth',2);
            %end
            
            % don't update image statistics until the user stops changing
            % values (i.e. moving a detector or moving an ROI)
            if ~(isprop(event,'EventName') && any(strcmp(event.EventName,{'MovingROI';'ValueChanging'}))) && ~(isprop(event,'Name') && strcmp(event.EventName,'ValueChanging'))
                updateImStats(app)
            end
        end

        % Callback function: comMagButtonGroup, comPhaseButtonGroup, 
        % comxButtonGroup, comyButtonGroup, vectButtonGroup, 
        % vectSubsample
        function firstMoment(app, event)
            app.vectorField.NextPlot='replace';
            
            switch event.Source
                case app.vectSubsample % subsample the vector field map
                    app.params.subsample=find(ismember(app.vectSubsample.Items,app.vectSubsample.Value));
                    if find(ismember(app.vectSubsample.Items,app.vectSubsample.Value))>2
                        app.params.subsample=2^(app.params.subsample-2);
                    else
                        app.params.subsample=1;
                    end
                    plotVectorField(app)
                case app.vectButtonGroup % change image on vector field tab
                    plotVectorField(app)
                otherwise % change button group item on main CoM tab to change which image is displayed
                    displayCoM(app)
            end
            updateImStats(app);
        end

        % Callback function: ImageDropDown, autoSaveButton, 
        % brightness, brightness, brightnessReset, contrast, 
        % contrast, contrastReset, controlPanel, 
        % displayImagesButton, dpPan, dpReset, dpZoom, gamma, 
        % gamma, gammaReset, histLog, imColormap, invertColors, 
        % liveUpdate, saveButton, saveImagesButton, saveVecField, 
        % vectPan, vectReset, vectZoom
        function imageControls(app, event)
            switch event.Source
                case app.displayImagesButton
                    app.saveImagesButton.Enable='on';
                    tmp_msg = uiprogressdlg(app.Quant4D_Fig,'Title','Forming Images...','Message','Please Wait...','Indeterminate','on');
                    switch app.detectorTypeButtonGroup.SelectedObject
                        case app.dpc
                            integrateMasks(app)
                            displayCoM(app)
                        case app.com
                            integrateMasks(app)
                            displayCoM(app)
                        case app.vdf
                            plotImage(app,'adf');
                    end
                    close(tmp_msg)
                case app.vectPan % pan vector field image
                    if app.vectPan.Value
                        pan(app.vectorField,'on');
                        zoom(app.vectorField,'off');
                        app.vectZoom.Value=0;
                    else
                        pan(app.vectorField,'off');
                    end
                    
                case app.dpPan % pan on the diffraction pattern
                    if app.dpPan.Value
                        pan(app.diffPattern,'on');
                        zoom(app.diffPattern,'off');
                        app.dpZoom.Value=0;
                    else
                        pan(app.diffPattern,'off');
                    end
                    
                case app.vectZoom % zoom vector field image
                    if app.vectZoom.Value
                        zoom(app.vectorField,'on');
                        pan(app.vectorField,'off');
                        app.vectPan.Value=0;
                    else
                        zoom(app.vectorField,'off');
                    end
                    
                case app.dpZoom % zoom diffraction pattern
                    if app.dpZoom.Value
                        zoom(app.diffPattern,'on');
                        pan(app.diffPattern,'off');
                        app.dpPan.Value=0;
                    else
                        zoom(app.diffPattern,'off');
                    end
                    
                case app.vectReset % reset vector field image axes
                    app.params.limits.im=[1 app.params.framesy 1 app.params.framesx];
                    axis(app.vectorField,app.params.limits.im);
                    app.vectPan.Value=0;
                    app.vectZoom.Value=0;
                    zoom(app.vectorField,'off');
                    pan(app.vectorField,'off');
                    
                case app.dpReset % reset diffraction pattern axes
                    app.params.limits.dp=[1 app.params.nopiy 1 app.params.nopix];
                    axis(app.diffPattern,app.params.limits.dp);
                    app.dpPan.Value=0;
                    app.dpZoom.Value=0;
                    zoom(app.diffPattern,'off');
                    pan(app.diffPattern,'off');
                    
                case app.saveVecField % save vector field as image and figure
                    saveVect(app);
                    figure(app.Quant4D_Fig);
                    
                case {app.saveImagesButton,app.saveButton,app.autoSaveButton} % regular image save modes
                    % Try to close any previous 'Save Images' windows
                    if ~isempty(findall(0,'Name','Save Images'))
                        close(findall(0,'Name','Save Images'))
                    end
                    
                    % switch from "save images" to the save/autosave buttons
                    if app.saveImagesButton.Visible
                        app.saveImagesButton.Visible=0;
                        app.saveButton.Visible=1;app.saveButton.Enable=1;
                        app.autoSaveButton.Visible=1;app.autoSaveButton.Enable=1;
                    end
                    
                    switch event.Source
                        case app.autoSaveButton
                            app.params.savePrefs.autosave=1;
                        otherwise
                            app.params.savePrefs.autosave=0;
                    end
                    
                    save4Dimages(app,app.params.savePrefs);
                    figure(app.Quant4D_Fig);
               
                otherwise % Brightness/contrast/gamma/colormap settings:
                    % Initial contrast will be set as the total range of min:max
                    % A change in contrast will expand or contract the width of the range
                    % Initial brightness will be also set as the total range of min:max
                    % A change in brightness will result in shift of the range up or down
                    % Initial gamma is set to 1
                    % A change in gamma will result in a powerlaw change in contrast I=I0^gamma
                                        
                    switch event.Source
                        case app.brightness
                            app.brightness.Value=event.Value;
                            app.imageProperties(app.ImageDropDown.Value,:).brightness = app.brightness.Value;
                        case app.brightnessReset
                            app.brightness.Value=0;
                            app.imageProperties(app.ImageDropDown.Value,:).brightness = 0;
                        case app.contrast
                            app.contrast.Value=event.Value;
                            app.imageProperties(app.ImageDropDown.Value,:).contrast   = app.contrast.Value;
                        case app.contrastReset
                            app.contrast.Value=0;
                            app.imageProperties(app.ImageDropDown.Value,:).contrast   = 0;
                        case {app.gamma,app.gammaReset} %gamma and gamma_reset
                            if event.Source == app.gammaReset
                                app.gamma.Value=1;
                                app.imageProperties(app.ImageDropDown.Value,:).gamma      = 1;
                            elseif event.Source == app.gamma
                                app.gamma.Value=event.Value;
                                app.imageProperties(app.ImageDropDown.Value,:).gamma      = app.gamma.Value;
                            end
                        case app.imColormap
                            app.imageProperties(app.ImageDropDown.Value,:).colormap{:}   = app.imColormap.Value;
                        case app.invertColors
                            app.imageProperties(app.ImageDropDown.Value,:).inverted   = app.invertColors.Value;
                        case app.ImageDropDown
                            % Define the currently selected image from the dropdown
                            % and its associated brightness, contrast, and gamma values
                            % to update slider bars
                            app.brightness.Value    = app.imageProperties(app.ImageDropDown.Value,:).brightness;
                            app.contrast.Value      = app.imageProperties(app.ImageDropDown.Value,:).contrast;
                            app.gamma.Value         = app.imageProperties(app.ImageDropDown.Value,:).gamma;
                            app.imColormap.Value    = app.imageProperties(app.ImageDropDown.Value,:).colormap{:};
                            app.invertColors.Value  = app.imageProperties(app.ImageDropDown.Value,:).inverted;
                    end
                    
                    % replot images and update stats and histogram for the given image
                    if app.vdf.Value
                        moveApertures(app,event.Source,event);
                    else
                        moveDetectors(app,event.Source,event);
                    end
                    plotImage(app,app.ImageDropDown.Value)
                    updateImStats(app);
            end
            
            if app.alignScanRot.Value scanRotation(app);end
        end

        % Callback function: centerX, centerY, 
        % diffractionCalibration, editManualCalButton, keV, 
        % transCal, transRad, transmittedDiskRadius
        function calibration_TODO(app, event)
            switch event.Source
                case app.manualCalButton % Push the "Auto Align" button in the Alignment Tab
                    app.editManualCalButton.Value=1;
                    app.alignmentPanel.SelectedTab = app.calibrationTab;
                    app.editManualCalButton.Text = 'Finish';
                    app.transCal.Editable = 'on';
                    app.transRad.Editable = 'on';
                    app.centerX.Editable = 'on';
                    app.centerY.Editable = 'on';
                case app.editManualCalButton % Push the "edit/finish" button in the "Calibration" Tab
                    switch app.editManualCalButton.Value
                        case 0 % Edit off, turn off all features
                            app.editManualCalButton.Text = 'Edit';
                            app.transCal.Editable = 'off';
                            app.transRad.Editable = 'off';
                            app.centerX.Editable = 'off';
                            app.centerY.Editable = 'off';
                            app.alignmentPanel.SelectedTab = app.alignmentTab;
                            app.transBeamAlign.Value = 0;
                            clearDetectors(app);
                            alignment(app, event); % send back to main alignment routine and end
                            
                        case 1 % Edit on, allow user to change values
                            app.editManualCalButton.Text = 'Finish';
                            app.transCal.Editable = 'on';
                            app.transRad.Editable = 'on';
                            app.centerX.Editable = 'on';
                            app.centerY.Editable = 'on';
                    end
                case app.diffractionCalibration % Diffraction Calibration units
                    switch app.diffractionCalibration.SelectedObject
                        case app.mradButton
                            app.transCal.Value = 1/app.params.mrad_per_pix;
                            app.pixelsmradEditFieldLabel.Text = 'pixels / mrad';
                        case app.invAButton
                            app.transCal.Value = app.params.radius/mrad2invA(app,app.alpha.Value,'mrad');
                            app.pixelsmradEditFieldLabel.Text = 'pixels / invA';
                    end
                case app.transmittedDiskRadius % Transmitted Disk Radius units
                    switch app.transmittedDiskRadius.SelectedObject
                        case app.transRadPix
                            app.transRad.Value = app.params.radius;
                        case app.transRadMrad
                            app.transRad.Value = app.alpha.Value;
                        case app.transRadInvA
                            app.transRad.Value = mrad2invA(app,app.alpha.Value,'mrad');
                    end
                case app.transCal % Manually changing the calibration in pixles/mrad or pixels/invA
                    switch app.diffractionCalibration.SelectedObject
                        case app.mradButton
                            app.params.mrad_per_pix = 1/app.transCal.Value;
                        case app.invAButton
                            app.params.mrad_per_pix = 1/mrad2invA(app,app.params.mrad_per_pix,'mrad');
                    end
                case app.transRad % Manually changing the transmitted disk radius size in pixels, mrad, or invA
                    switch app.transmittedDiskRadius.SelectedObject
                        case app.transRadPix
                            app.params.radius = app.transRad.Value;
                        case app.transRadMrad
                            app.alpha.Value = app.transRad.Value;
                        case app.transRadInvA
                            app.alpha.Value = mrad2invA(app,app.transRad.Value,'invA');
                    end
                case app.keV % Changing accelerating voltage changes mrad:invA conversion
                    if app.transRadInvA.Value 
                        app.transRad.Value = mrad2invA(app,app.alpha.Value,'mrad'); 
                    end
                    if app.invAButton.Value
                        app.transCal.Value = app.params.radius/mrad2invA(app,app.alpha.Value,'mrad');
                    end
            end
            
            % if the 'edit' button is 'on':
            if app.editManualCalButton.Value
                % update the diffraction pattern center with the user-defined values
                app.params.prev_center = [app.centerX.Value,app.centerY.Value];
                
                % replot the transmitted disk outline
                clearDetectors(app);
                try app.annotations.disk_edge.Visible = true;catch;end
            end

        end
    end

    % Component initialization
    methods (Access = private)

        % Create UIFigure and components
        function createComponents(app)

            % Create Quant4D_Fig and hide until all components are created
            app.Quant4D_Fig = uifigure('Visible', 'off');
            app.Quant4D_Fig.Colormap = [0 0 0;0.0158730158730159 0.0158730158730159 0.0158730158730159;0.0317460317460317 0.0317460317460317 0.0317460317460317;0.0476190476190476 0.0476190476190476 0.0476190476190476;0.0634920634920635 0.0634920634920635 0.0634920634920635;0.0793650793650794 0.0793650793650794 0.0793650793650794;0.0952380952380952 0.0952380952380952 0.0952380952380952;0.111111111111111 0.111111111111111 0.111111111111111;0.126984126984127 0.126984126984127 0.126984126984127;0.142857142857143 0.142857142857143 0.142857142857143;0.158730158730159 0.158730158730159 0.158730158730159;0.174603174603175 0.174603174603175 0.174603174603175;0.19047619047619 0.19047619047619 0.19047619047619;0.206349206349206 0.206349206349206 0.206349206349206;0.222222222222222 0.222222222222222 0.222222222222222;0.238095238095238 0.238095238095238 0.238095238095238;0.253968253968254 0.253968253968254 0.253968253968254;0.26984126984127 0.26984126984127 0.26984126984127;0.285714285714286 0.285714285714286 0.285714285714286;0.301587301587302 0.301587301587302 0.301587301587302;0.317460317460317 0.317460317460317 0.317460317460317;0.333333333333333 0.333333333333333 0.333333333333333;0.349206349206349 0.349206349206349 0.349206349206349;0.365079365079365 0.365079365079365 0.365079365079365;0.380952380952381 0.380952380952381 0.380952380952381;0.396825396825397 0.396825396825397 0.396825396825397;0.412698412698413 0.412698412698413 0.412698412698413;0.428571428571429 0.428571428571429 0.428571428571429;0.444444444444444 0.444444444444444 0.444444444444444;0.46031746031746 0.46031746031746 0.46031746031746;0.476190476190476 0.476190476190476 0.476190476190476;0.492063492063492 0.492063492063492 0.492063492063492;0.507936507936508 0.507936507936508 0.507936507936508;0.523809523809524 0.523809523809524 0.523809523809524;0.53968253968254 0.53968253968254 0.53968253968254;0.555555555555556 0.555555555555556 0.555555555555556;0.571428571428571 0.571428571428571 0.571428571428571;0.587301587301587 0.587301587301587 0.587301587301587;0.603174603174603 0.603174603174603 0.603174603174603;0.619047619047619 0.619047619047619 0.619047619047619;0.634920634920635 0.634920634920635 0.634920634920635;0.650793650793651 0.650793650793651 0.650793650793651;0.666666666666667 0.666666666666667 0.666666666666667;0.682539682539683 0.682539682539683 0.682539682539683;0.698412698412698 0.698412698412698 0.698412698412698;0.714285714285714 0.714285714285714 0.714285714285714;0.73015873015873 0.73015873015873 0.73015873015873;0.746031746031746 0.746031746031746 0.746031746031746;0.761904761904762 0.761904761904762 0.761904761904762;0.777777777777778 0.777777777777778 0.777777777777778;0.793650793650794 0.793650793650794 0.793650793650794;0.80952380952381 0.80952380952381 0.80952380952381;0.825396825396825 0.825396825396825 0.825396825396825;0.841269841269841 0.841269841269841 0.841269841269841;0.857142857142857 0.857142857142857 0.857142857142857;0.873015873015873 0.873015873015873 0.873015873015873;0.888888888888889 0.888888888888889 0.888888888888889;0.904761904761905 0.904761904761905 0.904761904761905;0.920634920634921 0.920634920634921 0.920634920634921;0.936507936507937 0.936507936507937 0.936507936507937;0.952380952380952 0.952380952380952 0.952380952380952;0.968253968253968 0.968253968253968 0.968253968253968;0.984126984126984 0.984126984126984 0.984126984126984;1 1 1];
            app.Quant4D_Fig.Position = [0 0 1600 900];
            app.Quant4D_Fig.Name = 'Quant4D';

            % Create guiLayout
            app.guiLayout = uigridlayout(app.Quant4D_Fig);
            app.guiLayout.ColumnWidth = {260, '13x', '24x'};
            app.guiLayout.RowHeight = {100, '1x', 410};

            % Create inputPanel
            app.inputPanel = uipanel(app.guiLayout);
            app.inputPanel.AutoResizeChildren = 'off';
            app.inputPanel.Layout.Row = 1;
            app.inputPanel.Layout.Column = 1;

            % Create displayImagesButton
            app.displayImagesButton = uibutton(app.inputPanel, 'push');
            app.displayImagesButton.ButtonPushedFcn = createCallbackFcn(app, @imageControls, true);
            app.displayImagesButton.Enable = 'off';
            app.displayImagesButton.Position = [28 35 100 22];
            app.displayImagesButton.Text = 'Update Images';

            % Create saveImagesButton
            app.saveImagesButton = uibutton(app.inputPanel, 'push');
            app.saveImagesButton.ButtonPushedFcn = createCallbackFcn(app, @imageControls, true);
            app.saveImagesButton.Enable = 'off';
            app.saveImagesButton.Position = [135 35 100 22];
            app.saveImagesButton.Text = 'Save Images';

            % Create importDataButton
            app.importDataButton = uibutton(app.inputPanel, 'push');
            app.importDataButton.ButtonPushedFcn = createCallbackFcn(app, @importData, true);
            app.importDataButton.FontWeight = 'bold';
            app.importDataButton.Position = [81 66 100 22];
            app.importDataButton.Text = 'Import';

            % Create liveUpdate
            app.liveUpdate = uicheckbox(app.inputPanel);
            app.liveUpdate.ValueChangedFcn = createCallbackFcn(app, @imageControls, true);
            app.liveUpdate.Enable = 'off';
            app.liveUpdate.Tooltip = {'Update images as detectors are changed.'; ''; 'If this is too slow, uncheck and use the Update Images button above after setting up the detectors '};
            app.liveUpdate.Text = 'Update Images Live';
            app.liveUpdate.Position = [67 8 129 22];
            app.liveUpdate.Value = true;

            % Create saveButton
            app.saveButton = uibutton(app.inputPanel, 'push');
            app.saveButton.ButtonPushedFcn = createCallbackFcn(app, @imageControls, true);
            app.saveButton.Icon = 'save.png';
            app.saveButton.Enable = 'off';
            app.saveButton.Visible = 'off';
            app.saveButton.Tooltip = {'Open save dialog'};
            app.saveButton.Position = [135 35 45 22];
            app.saveButton.Text = '';

            % Create autoSaveButton
            app.autoSaveButton = uibutton(app.inputPanel, 'push');
            app.autoSaveButton.ButtonPushedFcn = createCallbackFcn(app, @imageControls, true);
            app.autoSaveButton.Icon = 'autoSave.png';
            app.autoSaveButton.Enable = 'off';
            app.autoSaveButton.Visible = 'off';
            app.autoSaveButton.Tooltip = {'Autosave images using the same preferences as the last time the "Save Dialog" was used.'};
            app.autoSaveButton.Position = [188 35 45 22];
            app.autoSaveButton.Text = '';

            % Create controlPanel
            app.controlPanel = uitabgroup(app.guiLayout);
            app.controlPanel.SelectionChangedFcn = createCallbackFcn(app, @imageControls, true);
            app.controlPanel.Layout.Row = [2 3];
            app.controlPanel.Layout.Column = 1;

            % Create detectorsTab
            app.detectorsTab = uitab(app.controlPanel);
            app.detectorsTab.Title = 'Detectors';

            % Create detectorPanel
            app.detectorPanel = uipanel(app.detectorsTab);
            app.detectorPanel.BorderType = 'none';
            app.detectorPanel.Position = [14 223 232 505];

            % Create adf_inner_mrad
            app.adf_inner_mrad = uilabel(app.detectorPanel);
            app.adf_inner_mrad.HorizontalAlignment = 'center';
            app.adf_inner_mrad.Enable = 'off';
            app.adf_inner_mrad.Position = [147 293 33 22];
            app.adf_inner_mrad.Text = 'mrad';

            % Create adfInnerField
            app.adfInnerField = uieditfield(app.detectorPanel, 'numeric');
            app.adfInnerField.ValueDisplayFormat = '%.2f';
            app.adfInnerField.ValueChangedFcn = createCallbackFcn(app, @annularDetector, true);
            app.adfInnerField.Enable = 'off';
            app.adfInnerField.Position = [85 293 60 22];

            % Create adf_outer_mrad
            app.adf_outer_mrad = uilabel(app.detectorPanel);
            app.adf_outer_mrad.HorizontalAlignment = 'center';
            app.adf_outer_mrad.Enable = 'off';
            app.adf_outer_mrad.Position = [147 200 33 22];
            app.adf_outer_mrad.Text = 'mrad';

            % Create adfOuterField
            app.adfOuterField = uieditfield(app.detectorPanel, 'numeric');
            app.adfOuterField.ValueDisplayFormat = '%.2f';
            app.adfOuterField.ValueChangedFcn = createCallbackFcn(app, @annularDetector, true);
            app.adfOuterField.Enable = 'off';
            app.adfOuterField.Position = [85 200 60 22];

            % Create adf_inner_label
            app.adf_inner_label = uilabel(app.detectorPanel);
            app.adf_inner_label.HorizontalAlignment = 'center';
            app.adf_inner_label.Enable = 'off';
            app.adf_inner_label.Position = [44 322 150 22];
            app.adf_inner_label.Text = 'Detector Inner Angle';

            % Create adfInner
            app.adfInner = uislider(app.detectorPanel);
            app.adfInner.Limits = [0 1000];
            app.adfInner.MajorTicks = [];
            app.adfInner.ValueChangedFcn = createCallbackFcn(app, @annularDetector, true);
            app.adfInner.ValueChangingFcn = createCallbackFcn(app, @annularDetector, true);
            app.adfInner.MinorTicks = [];
            app.adfInner.Enable = 'off';
            app.adfInner.Position = [44 349 150 3];

            % Create adf_outer_label
            app.adf_outer_label = uilabel(app.detectorPanel);
            app.adf_outer_label.HorizontalAlignment = 'center';
            app.adf_outer_label.Enable = 'off';
            app.adf_outer_label.Position = [44 232 150 22];
            app.adf_outer_label.Text = 'Detector Outer Angle';

            % Create adfOuter
            app.adfOuter = uislider(app.detectorPanel);
            app.adfOuter.Limits = [0 1000];
            app.adfOuter.MajorTicks = [];
            app.adfOuter.ValueChangedFcn = createCallbackFcn(app, @annularDetector, true);
            app.adfOuter.ValueChangingFcn = createCallbackFcn(app, @annularDetector, true);
            app.adfOuter.MinorTicks = [];
            app.adfOuter.Enable = 'off';
            app.adfOuter.Position = [44 258 150 3];

            % Create adfInnerPlus
            app.adfInnerPlus = uibutton(app.detectorPanel, 'push');
            app.adfInnerPlus.ButtonPushedFcn = createCallbackFcn(app, @annularDetector, true);
            app.adfInnerPlus.Icon = 'plus_icon.png';
            app.adfInnerPlus.Enable = 'off';
            app.adfInnerPlus.Position = [208 339 25 22];
            app.adfInnerPlus.Text = '';

            % Create adfInnerMinus
            app.adfInnerMinus = uibutton(app.detectorPanel, 'push');
            app.adfInnerMinus.ButtonPushedFcn = createCallbackFcn(app, @annularDetector, true);
            app.adfInnerMinus.Icon = 'minus_icon.png';
            app.adfInnerMinus.Enable = 'off';
            app.adfInnerMinus.Position = [1 339 25 22];
            app.adfInnerMinus.Text = '';

            % Create adfOuterPlus
            app.adfOuterPlus = uibutton(app.detectorPanel, 'push');
            app.adfOuterPlus.ButtonPushedFcn = createCallbackFcn(app, @annularDetector, true);
            app.adfOuterPlus.Icon = 'plus_icon.png';
            app.adfOuterPlus.Enable = 'off';
            app.adfOuterPlus.Position = [208 248 25 22];
            app.adfOuterPlus.Text = '';

            % Create adfOuterMinus
            app.adfOuterMinus = uibutton(app.detectorPanel, 'push');
            app.adfOuterMinus.ButtonPushedFcn = createCallbackFcn(app, @annularDetector, true);
            app.adfOuterMinus.Icon = 'minus_icon.png';
            app.adfOuterMinus.Enable = 'off';
            app.adfOuterMinus.Position = [1 248 25 22];
            app.adfOuterMinus.Text = '';

            % Create linkADF
            app.linkADF = uibutton(app.detectorPanel, 'state');
            app.linkADF.ValueChangedFcn = createCallbackFcn(app, @annularDetector, true);
            app.linkADF.Enable = 'off';
            app.linkADF.Tooltip = {'Move inner/outer ADF sliders together'};
            app.linkADF.Icon = 'link.png';
            app.linkADF.Text = '';
            app.linkADF.Position = [208 293 25 22];

            % Create detectorTypeButtonGroup
            app.detectorTypeButtonGroup = uibuttongroup(app.detectorsTab);
            app.detectorTypeButtonGroup.SelectionChangedFcn = createCallbackFcn(app, @detectorType, true);
            app.detectorTypeButtonGroup.Title = 'Detector Type:';
            app.detectorTypeButtonGroup.FontWeight = 'bold';
            app.detectorTypeButtonGroup.Position = [30 600 200 127];

            % Create dpc
            app.dpc = uiradiobutton(app.detectorTypeButtonGroup);
            app.dpc.Enable = 'off';
            app.dpc.Text = 'Segmented';
            app.dpc.Position = [11 4 84 22];

            % Create adf
            app.adf = uiradiobutton(app.detectorTypeButtonGroup);
            app.adf.Enable = 'off';
            app.adf.Text = 'Annular/Round';
            app.adf.Position = [11 79 102 22];
            app.adf.Value = true;

            % Create vdf
            app.vdf = uiradiobutton(app.detectorTypeButtonGroup);
            app.vdf.Enable = 'off';
            app.vdf.Text = 'Virtual Aperture';
            app.vdf.Position = [11 54 105 22];

            % Create com
            app.com = uiradiobutton(app.detectorTypeButtonGroup);
            app.com.Enable = 'off';
            app.com.Text = 'Center of Mass';
            app.com.Position = [11 29 104 22];

            % Create detRotPanel
            app.detRotPanel = uipanel(app.detectorsTab);
            app.detRotPanel.BorderType = 'none';
            app.detRotPanel.Position = [1 221 250 188];

            % Create detRotMinus
            app.detRotMinus = uibutton(app.detRotPanel, 'push');
            app.detRotMinus.ButtonPushedFcn = createCallbackFcn(app, @annularDetector, true);
            app.detRotMinus.Icon = 'left_rotate.png';
            app.detRotMinus.Enable = 'off';
            app.detRotMinus.Position = [14 152 25 22];
            app.detRotMinus.Text = '';

            % Create det_angle_deg_3
            app.det_angle_deg_3 = uilabel(app.detRotPanel);
            app.det_angle_deg_3.Enable = 'off';
            app.det_angle_deg_3.Position = [161 100 25 22];
            app.det_angle_deg_3.Text = '°';

            % Create detAngleField
            app.detAngleField = uieditfield(app.detRotPanel, 'numeric');
            app.detAngleField.Limits = [-180 180];
            app.detAngleField.ValueDisplayFormat = '%.2f';
            app.detAngleField.ValueChangedFcn = createCallbackFcn(app, @annularDetector, true);
            app.detAngleField.Enable = 'off';
            app.detAngleField.Position = [98 100 60 22];

            % Create det_angle_label
            app.det_angle_label = uilabel(app.detRotPanel);
            app.det_angle_label.HorizontalAlignment = 'center';
            app.det_angle_label.Enable = 'off';
            app.det_angle_label.Position = [57 139 150 22];
            app.det_angle_label.Text = 'Detector Rotation';

            % Create detAngle
            app.detAngle = uislider(app.detRotPanel);
            app.detAngle.Limits = [-3.14159265358979 3.14159265358979];
            app.detAngle.MajorTicks = [];
            app.detAngle.ValueChangedFcn = createCallbackFcn(app, @annularDetector, true);
            app.detAngle.ValueChangingFcn = createCallbackFcn(app, @annularDetector, true);
            app.detAngle.MinorTicks = [];
            app.detAngle.Enable = 'off';
            app.detAngle.Position = [57 165 150 3];

            % Create nseg_label
            app.nseg_label = uilabel(app.detRotPanel);
            app.nseg_label.HorizontalAlignment = 'right';
            app.nseg_label.Enable = 'off';
            app.nseg_label.Position = [59 55 87 22];
            app.nseg_label.Text = '# of Segments:';

            % Create nseg
            app.nseg = uieditfield(app.detRotPanel, 'numeric');
            app.nseg.Limits = [2 16];
            app.nseg.RoundFractionalValues = 'on';
            app.nseg.ValueDisplayFormat = '%d';
            app.nseg.ValueChangedFcn = createCallbackFcn(app, @annularDetector, true);
            app.nseg.Enable = 'off';
            app.nseg.Position = [161 55 50 22];
            app.nseg.Value = 4;

            % Create nrung_label
            app.nrung_label = uilabel(app.detRotPanel);
            app.nrung_label.HorizontalAlignment = 'right';
            app.nrung_label.Enable = 'off';
            app.nrung_label.Position = [79 16 67 22];
            app.nrung_label.Text = '# of Rungs:';

            % Create nrung
            app.nrung = uieditfield(app.detRotPanel, 'numeric');
            app.nrung.Limits = [1 8];
            app.nrung.RoundFractionalValues = 'on';
            app.nrung.ValueDisplayFormat = '%d';
            app.nrung.ValueChangedFcn = createCallbackFcn(app, @annularDetector, true);
            app.nrung.Enable = 'off';
            app.nrung.Position = [161 16 50 22];
            app.nrung.Value = 1;

            % Create detRotPlus
            app.detRotPlus = uibutton(app.detRotPanel, 'push');
            app.detRotPlus.ButtonPushedFcn = createCallbackFcn(app, @annularDetector, true);
            app.detRotPlus.Icon = 'right_rotate.png';
            app.detRotPlus.Enable = 'off';
            app.detRotPlus.Position = [221 152 25 22];
            app.detRotPlus.Text = '';

            % Create detAngleReset
            app.detAngleReset = uibutton(app.detRotPanel, 'push');
            app.detAngleReset.ButtonPushedFcn = createCallbackFcn(app, @annularDetector, true);
            app.detAngleReset.Enable = 'off';
            app.detAngleReset.Position = [14 100 25 22];
            app.detAngleReset.Text = '0';

            % Create scanRotPanel
            app.scanRotPanel = uipanel(app.detectorsTab);
            app.scanRotPanel.BorderType = 'none';
            app.scanRotPanel.TitlePosition = 'centertop';
            app.scanRotPanel.Title = 'Scan Rotation';
            app.scanRotPanel.FontWeight = 'bold';
            app.scanRotPanel.Position = [14 62 232 123];

            % Create scanRotMinus
            app.scanRotMinus = uibutton(app.scanRotPanel, 'push');
            app.scanRotMinus.ButtonPushedFcn = createCallbackFcn(app, @alignment, true);
            app.scanRotMinus.Icon = 'minus_icon.png';
            app.scanRotMinus.Enable = 'off';
            app.scanRotMinus.Position = [1 65 25 22];
            app.scanRotMinus.Text = '';

            % Create scanRotInput
            app.scanRotInput = uieditfield(app.scanRotPanel, 'numeric');
            app.scanRotInput.Limits = [-180 180];
            app.scanRotInput.ValueDisplayFormat = '%.2f';
            app.scanRotInput.ValueChangedFcn = createCallbackFcn(app, @alignment, true);
            app.scanRotInput.Enable = 'off';
            app.scanRotInput.Position = [85 16 60 22];

            % Create scanRotLabel
            app.scanRotLabel = uilabel(app.scanRotPanel);
            app.scanRotLabel.HorizontalAlignment = 'center';
            app.scanRotLabel.Enable = 'off';
            app.scanRotLabel.Position = [146 16 10 22];
            app.scanRotLabel.Text = '°';

            % Create scanRotPlus
            app.scanRotPlus = uibutton(app.scanRotPanel, 'push');
            app.scanRotPlus.ButtonPushedFcn = createCallbackFcn(app, @alignment, true);
            app.scanRotPlus.Icon = 'plus_icon.png';
            app.scanRotPlus.Enable = 'off';
            app.scanRotPlus.Position = [202 62 25 22];
            app.scanRotPlus.Text = '';

            % Create scanRotMirror
            app.scanRotMirror = uicheckbox(app.scanRotPanel);
            app.scanRotMirror.ValueChangedFcn = createCallbackFcn(app, @alignment, true);
            app.scanRotMirror.Enable = 'off';
            app.scanRotMirror.Text = 'Mirror';
            app.scanRotMirror.Position = [177 16 55 22];

            % Create ScanRotationLabel
            app.ScanRotationLabel = uilabel(app.scanRotPanel);
            app.ScanRotationLabel.HorizontalAlignment = 'center';
            app.ScanRotationLabel.Enable = 'off';
            app.ScanRotationLabel.Position = [47 41 150 22];
            app.ScanRotationLabel.Text = 'Scan Rotation';

            % Create scanRot
            app.scanRot = uislider(app.scanRotPanel);
            app.scanRot.Limits = [-3.14159 3.14159];
            app.scanRot.MajorTicks = [];
            app.scanRot.MajorTickLabels = {};
            app.scanRot.ValueChangedFcn = createCallbackFcn(app, @alignment, true);
            app.scanRot.ValueChangingFcn = createCallbackFcn(app, @alignment, true);
            app.scanRot.MinorTicks = [];
            app.scanRot.Enable = 'off';
            app.scanRot.Position = [47 75 150 3];

            % Create scanRotReset
            app.scanRotReset = uibutton(app.scanRotPanel, 'push');
            app.scanRotReset.ButtonPushedFcn = createCallbackFcn(app, @alignment, true);
            app.scanRotReset.Enable = 'off';
            app.scanRotReset.Position = [1 20 25 22];
            app.scanRotReset.Text = '0';

            % Create alignScanRot
            app.alignScanRot = uibutton(app.detectorsTab, 'state');
            app.alignScanRot.ValueChangedFcn = createCallbackFcn(app, @alignment, true);
            app.alignScanRot.Enable = 'off';
            app.alignScanRot.Text = 'Align Scan Direction';
            app.alignScanRot.Position = [69 38 124 22];

            % Create brightnessContrastTab
            app.brightnessContrastTab = uitab(app.controlPanel);
            app.brightnessContrastTab.Title = 'Brightness/Contrast';

            % Create brightnessContrastGrid
            app.brightnessContrastGrid = uigridlayout(app.brightnessContrastTab);
            app.brightnessContrastGrid.ColumnWidth = {62, 94, 25, 27};
            app.brightnessContrastGrid.RowHeight = {22, 22, 198, 134, 226, 22};

            % Create brightnessPanel
            app.brightnessPanel = uipanel(app.brightnessContrastGrid);
            app.brightnessPanel.BorderType = 'none';
            app.brightnessPanel.Layout.Row = 3;
            app.brightnessPanel.Layout.Column = [1 4];

            % Create BrightnessLabel
            app.BrightnessLabel = uilabel(app.brightnessPanel);
            app.BrightnessLabel.HorizontalAlignment = 'center';
            app.BrightnessLabel.Enable = 'off';
            app.BrightnessLabel.Position = [51 138 150 22];
            app.BrightnessLabel.Text = 'Brightness';

            % Create brightness
            app.brightness = uislider(app.brightnessPanel);
            app.brightness.Limits = [-0.49999 0.49999];
            app.brightness.MajorTicks = [];
            app.brightness.MajorTickLabels = {};
            app.brightness.ValueChangedFcn = createCallbackFcn(app, @imageControls, true);
            app.brightness.ValueChangingFcn = createCallbackFcn(app, @imageControls, true);
            app.brightness.MinorTicks = [];
            app.brightness.Enable = 'off';
            app.brightness.Position = [51 170 150 3];

            % Create ContrastLabel
            app.ContrastLabel = uilabel(app.brightnessPanel);
            app.ContrastLabel.HorizontalAlignment = 'center';
            app.ContrastLabel.Enable = 'off';
            app.ContrastLabel.Position = [51 80 150 22];
            app.ContrastLabel.Text = 'Contrast';

            % Create contrast
            app.contrast = uislider(app.brightnessPanel);
            app.contrast.Limits = [-0.49999 0.49999];
            app.contrast.MajorTicks = [];
            app.contrast.MajorTickLabels = {};
            app.contrast.ValueChangedFcn = createCallbackFcn(app, @imageControls, true);
            app.contrast.ValueChangingFcn = createCallbackFcn(app, @imageControls, true);
            app.contrast.MinorTicks = [];
            app.contrast.Enable = 'off';
            app.contrast.Position = [51 112 150 3];

            % Create GammaLabel
            app.GammaLabel = uilabel(app.brightnessPanel);
            app.GammaLabel.HorizontalAlignment = 'center';
            app.GammaLabel.Enable = 'off';
            app.GammaLabel.Position = [51 18 150 22];
            app.GammaLabel.Text = 'Gamma';

            % Create gamma
            app.gamma = uislider(app.brightnessPanel);
            app.gamma.Limits = [0 5];
            app.gamma.MajorTicks = [];
            app.gamma.MajorTickLabels = {};
            app.gamma.ValueChangedFcn = createCallbackFcn(app, @imageControls, true);
            app.gamma.ValueChangingFcn = createCallbackFcn(app, @imageControls, true);
            app.gamma.MinorTicks = [];
            app.gamma.Enable = 'off';
            app.gamma.Position = [51 50 150 3];
            app.gamma.Value = 1;

            % Create brightnessReset
            app.brightnessReset = uibutton(app.brightnessPanel, 'push');
            app.brightnessReset.ButtonPushedFcn = createCallbackFcn(app, @imageControls, true);
            app.brightnessReset.Enable = 'off';
            app.brightnessReset.Position = [5 160 41 22];
            app.brightnessReset.Text = '50%';

            % Create contrastReset
            app.contrastReset = uibutton(app.brightnessPanel, 'push');
            app.contrastReset.ButtonPushedFcn = createCallbackFcn(app, @imageControls, true);
            app.contrastReset.Enable = 'off';
            app.contrastReset.Position = [5 102 41 22];
            app.contrastReset.Text = '50%';

            % Create gammaReset
            app.gammaReset = uibutton(app.brightnessPanel, 'push');
            app.gammaReset.ButtonPushedFcn = createCallbackFcn(app, @imageControls, true);
            app.gammaReset.Enable = 'off';
            app.gammaReset.Position = [13 40 25 22];
            app.gammaReset.Text = '1';

            % Create invertColors
            app.invertColors = uibutton(app.brightnessContrastGrid, 'state');
            app.invertColors.ValueChangedFcn = createCallbackFcn(app, @imageControls, true);
            app.invertColors.Enable = 'off';
            app.invertColors.Tooltip = {'Invert colormap'};
            app.invertColors.Icon = 'invertColors.png';
            app.invertColors.Text = '';
            app.invertColors.Layout.Row = 2;
            app.invertColors.Layout.Column = 4;

            % Create histLog
            app.histLog = uibutton(app.brightnessContrastGrid, 'state');
            app.histLog.ValueChangedFcn = createCallbackFcn(app, @imageControls, true);
            app.histLog.Text = 'log[ counts ]';
            app.histLog.Layout.Row = 6;
            app.histLog.Layout.Column = 2;

            % Create ImageLabel
            app.ImageLabel = uilabel(app.brightnessContrastGrid);
            app.ImageLabel.FontWeight = 'bold';
            app.ImageLabel.Enable = 'off';
            app.ImageLabel.Layout.Row = 1;
            app.ImageLabel.Layout.Column = 1;
            app.ImageLabel.Text = 'Image:';

            % Create ImageDropDown
            app.ImageDropDown = uidropdown(app.brightnessContrastGrid);
            app.ImageDropDown.Items = {'Diffraction Pattern'};
            app.ImageDropDown.ItemsData = {'pacbed'};
            app.ImageDropDown.ValueChangedFcn = createCallbackFcn(app, @imageControls, true);
            app.ImageDropDown.Enable = 'off';
            app.ImageDropDown.Layout.Row = 1;
            app.ImageDropDown.Layout.Column = [2 4];
            app.ImageDropDown.Value = 'pacbed';

            % Create ColormapLabel
            app.ColormapLabel = uilabel(app.brightnessContrastGrid);
            app.ColormapLabel.FontWeight = 'bold';
            app.ColormapLabel.Enable = 'off';
            app.ColormapLabel.Layout.Row = 2;
            app.ColormapLabel.Layout.Column = 1;
            app.ColormapLabel.Text = 'Colormap:';

            % Create imColormap
            app.imColormap = uidropdown(app.brightnessContrastGrid);
            app.imColormap.Items = {'gray', 'hot', 'cool', 'jet', 'parula', 'hsv', 'spring', 'summer', 'autumn', 'winter', 'bone', 'copper', 'pink', 'lines', 'colorcube', 'prism', 'flag'};
            app.imColormap.ItemsData = {'gray', 'hot', 'cool', 'jet', 'parula', 'hsv', 'spring', 'summer', 'autumn', 'winter', 'bone', 'copper', 'pink', 'lines', 'colorcube', 'prism', 'flag'};
            app.imColormap.ValueChangedFcn = createCallbackFcn(app, @imageControls, true);
            app.imColormap.Enable = 'off';
            app.imColormap.Layout.Row = 2;
            app.imColormap.Layout.Column = [2 3];
            app.imColormap.Value = 'gray';

            % Create imStats
            app.imStats = uitable(app.brightnessContrastGrid);
            app.imStats.ColumnName = {'Image stats'};
            app.imStats.RowName = {'min'; 'max'; 'mean'; 'std'; 'sum'};
            app.imStats.Layout.Row = 4;
            app.imStats.Layout.Column = [1 4];

            % Create histogramPlot
            app.histogramPlot = uiaxes(app.brightnessContrastGrid);
            app.histogramPlot.Box = 'on';
            app.histogramPlot.XTick = [];
            app.histogramPlot.XTickLabel = {'[ ]'};
            app.histogramPlot.YTick = [];
            app.histogramPlot.YTickLabel = {'[ ]'};
            app.histogramPlot.Color = [0.9412 0.9412 0.9412];
            app.histogramPlot.Layout.Row = 5;
            app.histogramPlot.Layout.Column = [1 4];

            % Create diffractionPanel
            app.diffractionPanel = uipanel(app.guiLayout);
            app.diffractionPanel.BorderType = 'none';
            app.diffractionPanel.Layout.Row = [1 2];
            app.diffractionPanel.Layout.Column = 2;

            % Create diffractionPanelGrid
            app.diffractionPanelGrid = uigridlayout(app.diffractionPanel);
            app.diffractionPanelGrid.ColumnWidth = {'1x'};
            app.diffractionPanelGrid.RowHeight = {25, '50x'};

            % Create diffControlPanel
            app.diffControlPanel = uipanel(app.diffractionPanelGrid);
            app.diffControlPanel.BorderType = 'none';
            app.diffControlPanel.Layout.Row = 1;
            app.diffControlPanel.Layout.Column = 1;

            % Create diffControlGrid
            app.diffControlGrid = uigridlayout(app.diffControlPanel);
            app.diffControlGrid.ColumnWidth = {'1x', 85, 28, 28, 85, '1x'};
            app.diffControlGrid.RowHeight = {22};
            app.diffControlGrid.Padding = [0 0 0 0];

            % Create dpLog
            app.dpLog = uibutton(app.diffControlGrid, 'state');
            app.dpLog.ValueChangedFcn = createCallbackFcn(app, @patternViewer, true);
            app.dpLog.Enable = 'off';
            app.dpLog.Text = 'log[ ]';
            app.dpLog.Layout.Row = 1;
            app.dpLog.Layout.Column = 2;

            % Create dpReset
            app.dpReset = uibutton(app.diffControlGrid, 'push');
            app.dpReset.ButtonPushedFcn = createCallbackFcn(app, @imageControls, true);
            app.dpReset.Enable = 'off';
            app.dpReset.Layout.Row = 1;
            app.dpReset.Layout.Column = 5;
            app.dpReset.Text = 'Reset Zoom';

            % Create dpPan
            app.dpPan = uibutton(app.diffControlGrid, 'state');
            app.dpPan.ValueChangedFcn = createCallbackFcn(app, @imageControls, true);
            app.dpPan.Enable = 'off';
            app.dpPan.Icon = 'pan.png';
            app.dpPan.Text = '';
            app.dpPan.Layout.Row = 1;
            app.dpPan.Layout.Column = 4;

            % Create dpZoom
            app.dpZoom = uibutton(app.diffControlGrid, 'state');
            app.dpZoom.ValueChangedFcn = createCallbackFcn(app, @imageControls, true);
            app.dpZoom.Enable = 'off';
            app.dpZoom.Icon = 'zoom.png';
            app.dpZoom.Text = '';
            app.dpZoom.Layout.Row = 1;
            app.dpZoom.Layout.Column = 3;

            % Create diffPattern
            app.diffPattern = uiaxes(app.diffractionPanelGrid);
            app.diffPattern.FontWeight = 'bold';
            app.diffPattern.GridLineStyle = 'none';
            app.diffPattern.Box = 'on';
            app.diffPattern.XTick = [];
            app.diffPattern.YTick = [];
            app.diffPattern.YTickLabel = {'[ ]'};
            app.diffPattern.Color = 'none';
            app.diffPattern.Layout.Row = 2;
            app.diffPattern.Layout.Column = 1;

            % Create alignmentPanel
            app.alignmentPanel = uitabgroup(app.guiLayout);
            app.alignmentPanel.Layout.Row = 3;
            app.alignmentPanel.Layout.Column = 2;

            % Create alignmentTab
            app.alignmentTab = uitab(app.alignmentPanel);
            app.alignmentTab.Title = 'Alignment';

            % Create alignmentTabGrid
            app.alignmentTabGrid = uigridlayout(app.alignmentTab);
            app.alignmentTabGrid.ColumnWidth = {'1x', 435, '1x'};
            app.alignmentTabGrid.RowHeight = {180, '1x'};

            % Create transBeamPanel
            app.transBeamPanel = uipanel(app.alignmentTabGrid);
            app.transBeamPanel.BorderType = 'none';
            app.transBeamPanel.Layout.Row = 1;
            app.transBeamPanel.Layout.Column = 2;

            % Create trans_beam_x_label
            app.trans_beam_x_label = uilabel(app.transBeamPanel);
            app.trans_beam_x_label.HorizontalAlignment = 'center';
            app.trans_beam_x_label.Enable = 'off';
            app.trans_beam_x_label.Position = [44 125 150 22];
            app.trans_beam_x_label.Text = 'Transmitted Beam X';

            % Create transBeamX
            app.transBeamX = uislider(app.transBeamPanel);
            app.transBeamX.MajorTicks = [];
            app.transBeamX.ValueChangedFcn = createCallbackFcn(app, @alignment, true);
            app.transBeamX.ValueChangingFcn = createCallbackFcn(app, @alignment, true);
            app.transBeamX.MinorTicks = [];
            app.transBeamX.Enable = 'off';
            app.transBeamX.Position = [44 157 150 3];

            % Create trans_beam_y_label
            app.trans_beam_y_label = uilabel(app.transBeamPanel);
            app.trans_beam_y_label.HorizontalAlignment = 'center';
            app.trans_beam_y_label.Enable = 'off';
            app.trans_beam_y_label.Position = [44 67 150 22];
            app.trans_beam_y_label.Text = 'Transmitted Beam Y';

            % Create transBeamY
            app.transBeamY = uislider(app.transBeamPanel);
            app.transBeamY.MajorTicks = [];
            app.transBeamY.ValueChangedFcn = createCallbackFcn(app, @alignment, true);
            app.transBeamY.ValueChangingFcn = createCallbackFcn(app, @alignment, true);
            app.transBeamY.MinorTicks = [];
            app.transBeamY.Enable = 'off';
            app.transBeamY.Position = [44 99 150 3];

            % Create trans_beam_radius_label
            app.trans_beam_radius_label = uilabel(app.transBeamPanel);
            app.trans_beam_radius_label.HorizontalAlignment = 'center';
            app.trans_beam_radius_label.Enable = 'off';
            app.trans_beam_radius_label.Position = [44 9 150 22];
            app.trans_beam_radius_label.Text = 'Transmitted Beam Radius';

            % Create transBeamRadius
            app.transBeamRadius = uislider(app.transBeamPanel);
            app.transBeamRadius.MajorTicks = [];
            app.transBeamRadius.ValueChangedFcn = createCallbackFcn(app, @alignment, true);
            app.transBeamRadius.ValueChangingFcn = createCallbackFcn(app, @alignment, true);
            app.transBeamRadius.MinorTicks = [];
            app.transBeamRadius.Enable = 'off';
            app.transBeamRadius.Position = [44 41 150 3];

            % Create conv_angle_label
            app.conv_angle_label = uilabel(app.transBeamPanel);
            app.conv_angle_label.HorizontalAlignment = 'right';
            app.conv_angle_label.Enable = 'off';
            app.conv_angle_label.Position = [245 39 148 22];
            app.conv_angle_label.Text = 'Convergence Angle (mrad)';

            % Create alpha
            app.alpha = uieditfield(app.transBeamPanel, 'numeric');
            app.alpha.ValueDisplayFormat = '%.1f';
            app.alpha.ValueChangedFcn = createCallbackFcn(app, @alignment, true);
            app.alpha.Enable = 'off';
            app.alpha.Position = [297 10 45 22];
            app.alpha.Value = 12;

            % Create transBeamXplus
            app.transBeamXplus = uibutton(app.transBeamPanel, 'push');
            app.transBeamXplus.ButtonPushedFcn = createCallbackFcn(app, @alignment, true);
            app.transBeamXplus.Icon = 'right_arrow.jpg';
            app.transBeamXplus.Enable = 'off';
            app.transBeamXplus.Position = [204 147 25 22];
            app.transBeamXplus.Text = '';

            % Create transBeamXminus
            app.transBeamXminus = uibutton(app.transBeamPanel, 'push');
            app.transBeamXminus.ButtonPushedFcn = createCallbackFcn(app, @alignment, true);
            app.transBeamXminus.Icon = 'left_arrow.png';
            app.transBeamXminus.Enable = 'off';
            app.transBeamXminus.Position = [7 147 25 22];
            app.transBeamXminus.Text = '';

            % Create transBeamYplus
            app.transBeamYplus = uibutton(app.transBeamPanel, 'push');
            app.transBeamYplus.ButtonPushedFcn = createCallbackFcn(app, @alignment, true);
            app.transBeamYplus.Icon = 'up_arrow.png';
            app.transBeamYplus.Enable = 'off';
            app.transBeamYplus.Position = [205 89 25 22];
            app.transBeamYplus.Text = '';

            % Create transBeamYminus
            app.transBeamYminus = uibutton(app.transBeamPanel, 'push');
            app.transBeamYminus.ButtonPushedFcn = createCallbackFcn(app, @alignment, true);
            app.transBeamYminus.Icon = 'down_arrow.png';
            app.transBeamYminus.Enable = 'off';
            app.transBeamYminus.Position = [8 89 25 22];
            app.transBeamYminus.Text = '';

            % Create transBeamRadiusPlus
            app.transBeamRadiusPlus = uibutton(app.transBeamPanel, 'push');
            app.transBeamRadiusPlus.ButtonPushedFcn = createCallbackFcn(app, @alignment, true);
            app.transBeamRadiusPlus.Icon = 'plus_icon.png';
            app.transBeamRadiusPlus.Enable = 'off';
            app.transBeamRadiusPlus.Position = [204 31 25 22];
            app.transBeamRadiusPlus.Text = '';

            % Create transBeamRadiusMinus
            app.transBeamRadiusMinus = uibutton(app.transBeamPanel, 'push');
            app.transBeamRadiusMinus.ButtonPushedFcn = createCallbackFcn(app, @alignment, true);
            app.transBeamRadiusMinus.Icon = 'minus_icon.png';
            app.transBeamRadiusMinus.Enable = 'off';
            app.transBeamRadiusMinus.Position = [7 31 25 22];
            app.transBeamRadiusMinus.Text = '';

            % Create transBeamAlign
            app.transBeamAlign = uibutton(app.transBeamPanel, 'state');
            app.transBeamAlign.ValueChangedFcn = createCallbackFcn(app, @alignment, true);
            app.transBeamAlign.Enable = 'off';
            app.transBeamAlign.Text = 'Align Transmitted Beam';
            app.transBeamAlign.Position = [248 139 143 22];

            % Create autoAlignButton
            app.autoAlignButton = uibutton(app.transBeamPanel, 'push');
            app.autoAlignButton.ButtonPushedFcn = createCallbackFcn(app, @alignment, true);
            app.autoAlignButton.Visible = 'off';
            app.autoAlignButton.Position = [270 76 100 22];
            app.autoAlignButton.Text = 'Auto Align';

            % Create manualCalButton
            app.manualCalButton = uibutton(app.transBeamPanel, 'push');
            app.manualCalButton.Enable = 'off';
            app.manualCalButton.Visible = 'off';
            app.manualCalButton.Position = [262 107 116 22];
            app.manualCalButton.Text = 'Manual Calibration';

            % Create diffPatternGroup
            app.diffPatternGroup = uibuttongroup(app.alignmentTabGrid);
            app.diffPatternGroup.AutoResizeChildren = 'off';
            app.diffPatternGroup.SelectionChangedFcn = createCallbackFcn(app, @patternViewer, true);
            app.diffPatternGroup.BorderType = 'none';
            app.diffPatternGroup.TitlePosition = 'centertop';
            app.diffPatternGroup.Title = 'Diffraction Patterns';
            app.diffPatternGroup.Layout.Row = 2;
            app.diffPatternGroup.Layout.Column = 2;
            app.diffPatternGroup.FontWeight = 'bold';

            % Create pacbedRadio
            app.pacbedRadio = uiradiobutton(app.diffPatternGroup);
            app.pacbedRadio.Enable = 'off';
            app.pacbedRadio.Text = 'PACBED';
            app.pacbedRadio.Position = [11 129 167 22];
            app.pacbedRadio.Value = true;

            % Create roiRadio
            app.roiRadio = uiradiobutton(app.diffPatternGroup);
            app.roiRadio.Enable = 'off';
            app.roiRadio.Text = 'Draw ROI:';
            app.roiRadio.Position = [11 107 78 22];

            % Create roiButtonGroup
            app.roiButtonGroup = uibuttongroup(app.diffPatternGroup);
            app.roiButtonGroup.AutoResizeChildren = 'off';
            app.roiButtonGroup.SelectionChangedFcn = createCallbackFcn(app, @patternViewer, true);
            app.roiButtonGroup.BorderType = 'none';
            app.roiButtonGroup.Position = [1 3 225 92];

            % Create roiEllipse
            app.roiEllipse = uitogglebutton(app.roiButtonGroup);
            app.roiEllipse.Enable = 'off';
            app.roiEllipse.Tooltip = {'Rotate by clicking near vertex and dragging'; ''; 'Maintain aspect ratio by holding shift while resizing'};
            app.roiEllipse.Text = 'Ellipse';
            app.roiEllipse.Position = [11 48 100 22];

            % Create roiRectangle
            app.roiRectangle = uitogglebutton(app.roiButtonGroup);
            app.roiRectangle.Enable = 'off';
            app.roiRectangle.Tooltip = {'Rotate by clicking near the corner of teh box and dragging'; ''; 'Maintain aspect ratio by holding shift while resizing'};
            app.roiRectangle.Text = 'Rectangle';
            app.roiRectangle.Position = [11 27 100 22];
            app.roiRectangle.Value = true;

            % Create roiPoly
            app.roiPoly = uitogglebutton(app.roiButtonGroup);
            app.roiPoly.Enable = 'off';
            app.roiPoly.Tooltip = {'Double click on line after drawing to add new vertex'; ''; 'Backspace while drawing to delete previous point'};
            app.roiPoly.Text = 'Free form';
            app.roiPoly.Position = [11 6 100 22];

            % Create roiPoint
            app.roiPoint = uitogglebutton(app.roiButtonGroup);
            app.roiPoint.Enable = 'off';
            app.roiPoint.Text = 'Point';
            app.roiPoint.Position = [11 69 100 22];

            % Create negativeROI
            app.negativeROI = uicheckbox(app.roiButtonGroup);
            app.negativeROI.ValueChangedFcn = createCallbackFcn(app, @patternViewer, true);
            app.negativeROI.Enable = 'off';
            app.negativeROI.Text = 'Negative ROI';
            app.negativeROI.Position = [121 6 94 22];

            % Create probeX
            app.probeX = uispinner(app.diffPatternGroup);
            app.probeX.ValueChangingFcn = createCallbackFcn(app, @patternViewer, true);
            app.probeX.Limits = [1 Inf];
            app.probeX.RoundFractionalValues = 'on';
            app.probeX.ValueDisplayFormat = 'x:%8.0f';
            app.probeX.ValueChangedFcn = createCallbackFcn(app, @patternViewer, true);
            app.probeX.HorizontalAlignment = 'left';
            app.probeX.Position = [203 67 80 22];
            app.probeX.Value = 256;

            % Create probeY
            app.probeY = uispinner(app.diffPatternGroup);
            app.probeY.ValueChangingFcn = createCallbackFcn(app, @patternViewer, true);
            app.probeY.Limits = [1 Inf];
            app.probeY.RoundFractionalValues = 'on';
            app.probeY.ValueDisplayFormat = 'y:%8.0f';
            app.probeY.ValueChangedFcn = createCallbackFcn(app, @patternViewer, true);
            app.probeY.HorizontalAlignment = 'left';
            app.probeY.Position = [298 67 80 22];
            app.probeY.Value = 256;

            % Create probePosition
            app.probePosition = uislider(app.diffPatternGroup);
            app.probePosition.MajorTicks = [];
            app.probePosition.MajorTickLabels = {};
            app.probePosition.ValueChangedFcn = createCallbackFcn(app, @patternViewer, true);
            app.probePosition.ValueChangingFcn = createCallbackFcn(app, @patternViewer, true);
            app.probePosition.MinorTicks = [];
            app.probePosition.Position = [161 125 260 3];

            % Create probePositionLabel
            app.probePositionLabel = uilabel(app.diffPatternGroup);
            app.probePositionLabel.Position = [248 93 86 22];
            app.probePositionLabel.Text = 'Probe position:';

            % Create calibrationTab
            app.calibrationTab = uitab(app.alignmentPanel);
            app.calibrationTab.Title = 'Calibration';

            % Create calibrationTabGrid
            app.calibrationTabGrid = uigridlayout(app.calibrationTab);
            app.calibrationTabGrid.ColumnWidth = {'1x', 100, 320, '1x'};
            app.calibrationTabGrid.RowHeight = {22, 62, 115, 100, '1x'};

            % Create diffractionCalibration
            app.diffractionCalibration = uibuttongroup(app.calibrationTabGrid);
            app.diffractionCalibration.AutoResizeChildren = 'off';
            app.diffractionCalibration.SelectionChangedFcn = createCallbackFcn(app, @calibration_TODO, true);
            app.diffractionCalibration.TitlePosition = 'centertop';
            app.diffractionCalibration.Title = 'Diffraction Calibration';
            app.diffractionCalibration.Layout.Row = [1 2];
            app.diffractionCalibration.Layout.Column = 3;
            app.diffractionCalibration.FontWeight = 'bold';

            % Create mradButton
            app.mradButton = uitogglebutton(app.diffractionCalibration);
            app.mradButton.Text = 'mrad';
            app.mradButton.Position = [11 41 100 22];
            app.mradButton.Value = true;

            % Create invAButton
            app.invAButton = uitogglebutton(app.diffractionCalibration);
            app.invAButton.Text = 'invA';
            app.invAButton.Position = [11 20 100 22];

            % Create pixelsmradEditFieldLabel
            app.pixelsmradEditFieldLabel = uilabel(app.diffractionCalibration);
            app.pixelsmradEditFieldLabel.Position = [198 17 74 22];
            app.pixelsmradEditFieldLabel.Text = 'pixels / mrad';

            % Create transCal
            app.transCal = uieditfield(app.diffractionCalibration, 'numeric');
            app.transCal.ValueChangedFcn = createCallbackFcn(app, @calibration_TODO, true);
            app.transCal.Editable = 'off';
            app.transCal.Position = [138 17 51 22];

            % Create keVLabel
            app.keVLabel = uilabel(app.diffractionCalibration);
            app.keVLabel.Position = [198 45 26 22];
            app.keVLabel.Text = 'keV';

            % Create keV
            app.keV = uieditfield(app.diffractionCalibration, 'numeric');
            app.keV.Limits = [0 1500];
            app.keV.ValueChangedFcn = createCallbackFcn(app, @calibration_TODO, true);
            app.keV.Position = [138 45 51 22];
            app.keV.Value = 300;

            % Create transmittedDiskPosition
            app.transmittedDiskPosition = uipanel(app.calibrationTabGrid);
            app.transmittedDiskPosition.AutoResizeChildren = 'off';
            app.transmittedDiskPosition.TitlePosition = 'centertop';
            app.transmittedDiskPosition.Title = 'Transmitted Disk Position';
            app.transmittedDiskPosition.Layout.Row = 4;
            app.transmittedDiskPosition.Layout.Column = 3;
            app.transmittedDiskPosition.FontWeight = 'bold';

            % Create XEditFieldLabel
            app.XEditFieldLabel = uilabel(app.transmittedDiskPosition);
            app.XEditFieldLabel.HorizontalAlignment = 'right';
            app.XEditFieldLabel.Position = [72 44 25 22];
            app.XEditFieldLabel.Text = 'X';

            % Create centerX
            app.centerX = uieditfield(app.transmittedDiskPosition, 'numeric');
            app.centerX.ValueChangedFcn = createCallbackFcn(app, @calibration_TODO, true);
            app.centerX.Editable = 'off';
            app.centerX.HorizontalAlignment = 'center';
            app.centerX.Position = [105 44 100 22];
            app.centerX.Value = 64;

            % Create centerXLabel
            app.centerXLabel = uilabel(app.transmittedDiskPosition);
            app.centerXLabel.HorizontalAlignment = 'center';
            app.centerXLabel.FontAngle = 'italic';
            app.centerXLabel.Position = [211 44 36 22];
            app.centerXLabel.Text = 'pixels';

            % Create YEditFieldLabel
            app.YEditFieldLabel = uilabel(app.transmittedDiskPosition);
            app.YEditFieldLabel.HorizontalAlignment = 'right';
            app.YEditFieldLabel.Position = [72 14 25 22];
            app.YEditFieldLabel.Text = 'Y';

            % Create centerY
            app.centerY = uieditfield(app.transmittedDiskPosition, 'numeric');
            app.centerY.ValueChangedFcn = createCallbackFcn(app, @calibration_TODO, true);
            app.centerY.Editable = 'off';
            app.centerY.HorizontalAlignment = 'center';
            app.centerY.Position = [105 14 100 22];
            app.centerY.Value = 64;

            % Create centerYLabel
            app.centerYLabel = uilabel(app.transmittedDiskPosition);
            app.centerYLabel.HorizontalAlignment = 'center';
            app.centerYLabel.FontAngle = 'italic';
            app.centerYLabel.Position = [211 14 36 22];
            app.centerYLabel.Text = 'pixels';

            % Create transmittedDiskRadius
            app.transmittedDiskRadius = uibuttongroup(app.calibrationTabGrid);
            app.transmittedDiskRadius.AutoResizeChildren = 'off';
            app.transmittedDiskRadius.SelectionChangedFcn = createCallbackFcn(app, @calibration_TODO, true);
            app.transmittedDiskRadius.TitlePosition = 'centertop';
            app.transmittedDiskRadius.Title = 'Transmitted Disk Radius';
            app.transmittedDiskRadius.Layout.Row = 3;
            app.transmittedDiskRadius.Layout.Column = 3;
            app.transmittedDiskRadius.FontWeight = 'bold';

            % Create transRadPix
            app.transRadPix = uitogglebutton(app.transmittedDiskRadius);
            app.transRadPix.Text = 'pixels';
            app.transRadPix.Position = [11 62 100 22];
            app.transRadPix.Value = true;

            % Create transRadMrad
            app.transRadMrad = uitogglebutton(app.transmittedDiskRadius);
            app.transRadMrad.Text = 'mrad';
            app.transRadMrad.Position = [11 41 100 22];

            % Create transRad
            app.transRad = uieditfield(app.transmittedDiskRadius, 'numeric');
            app.transRad.ValueChangedFcn = createCallbackFcn(app, @calibration_TODO, true);
            app.transRad.Editable = 'off';
            app.transRad.Position = [138 41 51 22];

            % Create transRadInvA
            app.transRadInvA = uitogglebutton(app.transmittedDiskRadius);
            app.transRadInvA.Text = 'invA';
            app.transRadInvA.Position = [11 20 100 22];

            % Create editManualCalButton
            app.editManualCalButton = uibutton(app.calibrationTabGrid, 'state');
            app.editManualCalButton.ValueChangedFcn = createCallbackFcn(app, @calibration_TODO, true);
            app.editManualCalButton.Enable = 'off';
            app.editManualCalButton.Tooltip = {'Coming Soon: manually set calibration scales, disk center, disk radius. '};
            app.editManualCalButton.Text = 'Edit';
            app.editManualCalButton.FontWeight = 'bold';
            app.editManualCalButton.Layout.Row = 1;
            app.editManualCalButton.Layout.Column = 2;

            % Create colorwheelTab
            app.colorwheelTab = uitab(app.alignmentPanel);
            app.colorwheelTab.Title = 'Colorwheel';

            % Create GridLayout
            app.GridLayout = uigridlayout(app.colorwheelTab);
            app.GridLayout.ColumnWidth = {'1x', '10.94x', '1x'};
            app.GridLayout.RowHeight = {'1x'};

            % Create colorwheelPlot
            app.colorwheelPlot = uiaxes(app.GridLayout);
            app.colorwheelPlot.Box = 'on';
            app.colorwheelPlot.XTick = [];
            app.colorwheelPlot.YTick = [];
            app.colorwheelPlot.YTickLabel = {'[ ]'};
            app.colorwheelPlot.ZTick = [];
            app.colorwheelPlot.Color = [0.9412 0.9412 0.9412];
            app.colorwheelPlot.Layout.Row = 1;
            app.colorwheelPlot.Layout.Column = 2;

            % Create virtualApertureTab
            app.virtualApertureTab = uitab(app.alignmentPanel);
            app.virtualApertureTab.Title = 'Virtual Aperture';

            % Create virtualApertureGrid
            app.virtualApertureGrid = uigridlayout(app.virtualApertureTab);
            app.virtualApertureGrid.ColumnWidth = {'1x', 435, '1x'};
            app.virtualApertureGrid.RowHeight = {195, 157};

            % Create symmetryOperationsPanel
            app.symmetryOperationsPanel = uipanel(app.virtualApertureGrid);
            app.symmetryOperationsPanel.Title = 'Symmetry operations:';
            app.symmetryOperationsPanel.Layout.Row = 2;
            app.symmetryOperationsPanel.Layout.Column = 2;
            app.symmetryOperationsPanel.FontWeight = 'bold';

            % Create mirrorPanel
            app.mirrorPanel = uipanel(app.symmetryOperationsPanel);
            app.mirrorPanel.BorderType = 'none';
            app.mirrorPanel.Position = [1 65 406 67];

            % Create apMirrorMinus
            app.apMirrorMinus = uibutton(app.mirrorPanel, 'push');
            app.apMirrorMinus.ButtonPushedFcn = createCallbackFcn(app, @virtualAperture, true);
            app.apMirrorMinus.Icon = 'left_rotate.png';
            app.apMirrorMinus.Enable = 'off';
            app.apMirrorMinus.Position = [170 43 28 22];
            app.apMirrorMinus.Text = '';

            % Create MirrorPlaneRotationLabel
            app.MirrorPlaneRotationLabel = uilabel(app.mirrorPanel);
            app.MirrorPlaneRotationLabel.HorizontalAlignment = 'center';
            app.MirrorPlaneRotationLabel.Enable = 'off';
            app.MirrorPlaneRotationLabel.Position = [203 23 150 22];
            app.MirrorPlaneRotationLabel.Text = 'Mirror Plane Rotation';

            % Create apMirrorAngle
            app.apMirrorAngle = uislider(app.mirrorPanel);
            app.apMirrorAngle.Limits = [-3.14159265358979 3.14159265358979];
            app.apMirrorAngle.MajorTicks = [];
            app.apMirrorAngle.ValueChangedFcn = createCallbackFcn(app, @virtualAperture, true);
            app.apMirrorAngle.ValueChangingFcn = createCallbackFcn(app, @virtualAperture, true);
            app.apMirrorAngle.MinorTicks = [];
            app.apMirrorAngle.Enable = 'off';
            app.apMirrorAngle.Position = [203 54 150 3];

            % Create aperture_y_Label_2
            app.aperture_y_Label_2 = uilabel(app.mirrorPanel);
            app.aperture_y_Label_2.Enable = 'off';
            app.aperture_y_Label_2.Position = [311 1 28 22];
            app.aperture_y_Label_2.Text = '°';

            % Create apMirrorInput
            app.apMirrorInput = uieditfield(app.mirrorPanel, 'numeric');
            app.apMirrorInput.Limits = [-180 180];
            app.apMirrorInput.ValueDisplayFormat = '%.1f';
            app.apMirrorInput.ValueChangedFcn = createCallbackFcn(app, @virtualAperture, true);
            app.apMirrorInput.HorizontalAlignment = 'center';
            app.apMirrorInput.Enable = 'off';
            app.apMirrorInput.Position = [248 1 60 22];

            % Create apMirrorPlus
            app.apMirrorPlus = uibutton(app.mirrorPanel, 'push');
            app.apMirrorPlus.ButtonPushedFcn = createCallbackFcn(app, @virtualAperture, true);
            app.apMirrorPlus.Icon = 'right_rotate.png';
            app.apMirrorPlus.Enable = 'off';
            app.apMirrorPlus.Position = [365 43 28 22];
            app.apMirrorPlus.Text = '';

            % Create apMirrorReset
            app.apMirrorReset = uibutton(app.mirrorPanel, 'push');
            app.apMirrorReset.ButtonPushedFcn = createCallbackFcn(app, @virtualAperture, true);
            app.apMirrorReset.Enable = 'off';
            app.apMirrorReset.Position = [172 1 28 22];
            app.apMirrorReset.Text = '0';

            % Create apMirror
            app.apMirror = uicheckbox(app.symmetryOperationsPanel);
            app.apMirror.ValueChangedFcn = createCallbackFcn(app, @virtualAperture, true);
            app.apMirror.Enable = 'off';
            app.apMirror.Text = 'Mirror plane';
            app.apMirror.Position = [18 44 86 22];

            % Create apertureSymmetrySpinnerLabel
            app.apertureSymmetrySpinnerLabel = uilabel(app.symmetryOperationsPanel);
            app.apertureSymmetrySpinnerLabel.HorizontalAlignment = 'center';
            app.apertureSymmetrySpinnerLabel.Enable = 'off';
            app.apertureSymmetrySpinnerLabel.Position = [5 100 117 22];
            app.apertureSymmetrySpinnerLabel.Text = 'Rotational Symmetry';

            % Create apertureSymmetry
            app.apertureSymmetry = uispinner(app.symmetryOperationsPanel);
            app.apertureSymmetry.Limits = [1 6];
            app.apertureSymmetry.RoundFractionalValues = 'on';
            app.apertureSymmetry.ValueDisplayFormat = '%.0f';
            app.apertureSymmetry.ValueChangedFcn = createCallbackFcn(app, @virtualAperture, true);
            app.apertureSymmetry.HorizontalAlignment = 'center';
            app.apertureSymmetry.Enable = 'off';
            app.apertureSymmetry.Position = [18 76 50 22];
            app.apertureSymmetry.Value = 1;

            % Create apNegative
            app.apNegative = uicheckbox(app.symmetryOperationsPanel);
            app.apNegative.ValueChangedFcn = createCallbackFcn(app, @virtualAperture, true);
            app.apNegative.Text = 'Negative mask';
            app.apNegative.Position = [18 2 101 22];

            % Create apLattice
            app.apLattice = uicheckbox(app.symmetryOperationsPanel);
            app.apLattice.Enable = 'off';
            app.apLattice.Tooltip = {'coming soon'};
            app.apLattice.Text = 'Aperture lattice';
            app.apLattice.Position = [18 23 103 22];

            % Create virtualAperturePanelParent
            app.virtualAperturePanelParent = uipanel(app.virtualApertureGrid);
            app.virtualAperturePanelParent.BorderType = 'none';
            app.virtualAperturePanelParent.Layout.Row = 1;
            app.virtualAperturePanelParent.Layout.Column = 2;

            % Create coordinatesButtonGroup
            app.coordinatesButtonGroup = uibuttongroup(app.virtualAperturePanelParent);
            app.coordinatesButtonGroup.SelectionChangedFcn = createCallbackFcn(app, @virtualAperture, true);
            app.coordinatesButtonGroup.Title = 'Coordinates:';
            app.coordinatesButtonGroup.Position = [3 120 102 70];

            % Create cartesianRadio
            app.cartesianRadio = uiradiobutton(app.coordinatesButtonGroup);
            app.cartesianRadio.Enable = 'off';
            app.cartesianRadio.Text = 'Cartesian';
            app.cartesianRadio.Position = [11 23 73 22];

            % Create polarRadio
            app.polarRadio = uiradiobutton(app.coordinatesButtonGroup);
            app.polarRadio.Enable = 'off';
            app.polarRadio.Text = 'Polar';
            app.polarRadio.Position = [11 1 50 22];
            app.polarRadio.Value = true;

            % Create virtualAperturePanel
            app.virtualAperturePanel = uipanel(app.virtualAperturePanelParent);
            app.virtualAperturePanel.BorderType = 'none';
            app.virtualAperturePanel.Position = [145 1 270 195];

            % Create DistanceLabel
            app.DistanceLabel = uilabel(app.virtualAperturePanel);
            app.DistanceLabel.Enable = 'off';
            app.DistanceLabel.Position = [84 93 150 22];
            app.DistanceLabel.Text = 'Distance';

            % Create apX
            app.apX = uislider(app.virtualAperturePanel);
            app.apX.MajorTicks = [];
            app.apX.ValueChangedFcn = createCallbackFcn(app, @virtualAperture, true);
            app.apX.ValueChangingFcn = createCallbackFcn(app, @virtualAperture, true);
            app.apX.MinorTicks = [];
            app.apX.Enable = 'off';
            app.apX.Position = [74 124 150 3];

            % Create RotationLabel
            app.RotationLabel = uilabel(app.virtualAperturePanel);
            app.RotationLabel.Enable = 'off';
            app.RotationLabel.Position = [84 34 60 22];
            app.RotationLabel.Text = 'Rotation';

            % Create apY
            app.apY = uislider(app.virtualAperturePanel);
            app.apY.Limits = [-100 100];
            app.apY.MajorTicks = [];
            app.apY.ValueChangedFcn = createCallbackFcn(app, @virtualAperture, true);
            app.apY.ValueChangingFcn = createCallbackFcn(app, @virtualAperture, true);
            app.apY.MinorTicks = [];
            app.apY.Enable = 'off';
            app.apY.Position = [74 66 150 3];

            % Create apXPlus
            app.apXPlus = uibutton(app.virtualAperturePanel, 'push');
            app.apXPlus.ButtonPushedFcn = createCallbackFcn(app, @virtualAperture, true);
            app.apXPlus.Icon = 'plus_icon.png';
            app.apXPlus.Enable = 'off';
            app.apXPlus.Position = [234 114 28 22];
            app.apXPlus.Text = '';

            % Create apXMinus
            app.apXMinus = uibutton(app.virtualAperturePanel, 'push');
            app.apXMinus.ButtonPushedFcn = createCallbackFcn(app, @virtualAperture, true);
            app.apXMinus.Icon = 'minus_icon.png';
            app.apXMinus.Enable = 'off';
            app.apXMinus.Position = [39 114 28 22];
            app.apXMinus.Text = '';

            % Create apYPlus
            app.apYPlus = uibutton(app.virtualAperturePanel, 'push');
            app.apYPlus.ButtonPushedFcn = createCallbackFcn(app, @virtualAperture, true);
            app.apYPlus.Icon = 'plus_icon.png';
            app.apYPlus.Enable = 'off';
            app.apYPlus.Position = [234 54 28 22];
            app.apYPlus.Text = '';

            % Create apYMinus
            app.apYMinus = uibutton(app.virtualAperturePanel, 'push');
            app.apYMinus.ButtonPushedFcn = createCallbackFcn(app, @virtualAperture, true);
            app.apYMinus.Icon = 'minus_icon.png';
            app.apYMinus.Enable = 'off';
            app.apYMinus.Position = [39 54 28 22];
            app.apYMinus.Text = '';

            % Create apXReset
            app.apXReset = uibutton(app.virtualAperturePanel, 'push');
            app.apXReset.ButtonPushedFcn = createCallbackFcn(app, @virtualAperture, true);
            app.apXReset.Enable = 'off';
            app.apXReset.Position = [7 114 28 22];
            app.apXReset.Text = '0';

            % Create apYReset
            app.apYReset = uibutton(app.virtualAperturePanel, 'push');
            app.apYReset.ButtonPushedFcn = createCallbackFcn(app, @virtualAperture, true);
            app.apYReset.Enable = 'off';
            app.apYReset.Position = [7 54 28 22];
            app.apYReset.Text = '0';

            % Create adf_inner_mrad_2
            app.adf_inner_mrad_2 = uilabel(app.virtualAperturePanel);
            app.adf_inner_mrad_2.HorizontalAlignment = 'center';
            app.adf_inner_mrad_2.Enable = 'off';
            app.adf_inner_mrad_2.Position = [196 93 33 22];
            app.adf_inner_mrad_2.Text = 'mrad';

            % Create apXField
            app.apXField = uieditfield(app.virtualAperturePanel, 'numeric');
            app.apXField.ValueDisplayFormat = '%.2f';
            app.apXField.ValueChangedFcn = createCallbackFcn(app, @virtualAperture, true);
            app.apXField.Enable = 'off';
            app.apXField.Position = [147 93 47 22];

            % Create aperture_y_Label
            app.aperture_y_Label = uilabel(app.virtualAperturePanel);
            app.aperture_y_Label.Enable = 'off';
            app.aperture_y_Label.Position = [196 34 33 22];
            app.aperture_y_Label.Text = '°';

            % Create apYField
            app.apYField = uieditfield(app.virtualAperturePanel, 'numeric');
            app.apYField.ValueDisplayFormat = '%.2f';
            app.apYField.ValueChangedFcn = createCallbackFcn(app, @virtualAperture, true);
            app.apYField.Enable = 'off';
            app.apYField.Position = [147 34 47 22];

            % Create apSizePlus
            app.apSizePlus = uibutton(app.virtualAperturePanel, 'push');
            app.apSizePlus.ButtonPushedFcn = createCallbackFcn(app, @virtualAperture, true);
            app.apSizePlus.Icon = 'plus_icon.png';
            app.apSizePlus.Enable = 'off';
            app.apSizePlus.Position = [234 171 28 22];
            app.apSizePlus.Text = '';

            % Create apSizeMinus
            app.apSizeMinus = uibutton(app.virtualAperturePanel, 'push');
            app.apSizeMinus.ButtonPushedFcn = createCallbackFcn(app, @virtualAperture, true);
            app.apSizeMinus.Icon = 'minus_icon.png';
            app.apSizeMinus.Enable = 'off';
            app.apSizeMinus.Position = [39 171 28 22];
            app.apSizeMinus.Text = '';

            % Create SizeLabel
            app.SizeLabel = uilabel(app.virtualAperturePanel);
            app.SizeLabel.Enable = 'off';
            app.SizeLabel.Position = [84 150 150 22];
            app.SizeLabel.Text = 'Size';

            % Create apSize
            app.apSize = uislider(app.virtualAperturePanel);
            app.apSize.MajorTicks = [];
            app.apSize.ValueChangedFcn = createCallbackFcn(app, @virtualAperture, true);
            app.apSize.ValueChangingFcn = createCallbackFcn(app, @virtualAperture, true);
            app.apSize.MinorTicks = [];
            app.apSize.Enable = 'off';
            app.apSize.Position = [74 181 150 3];

            % Create adf_inner_mrad_4
            app.adf_inner_mrad_4 = uilabel(app.virtualAperturePanel);
            app.adf_inner_mrad_4.HorizontalAlignment = 'center';
            app.adf_inner_mrad_4.Enable = 'off';
            app.adf_inner_mrad_4.Position = [196 149 33 22];
            app.adf_inner_mrad_4.Text = 'mrad';

            % Create apSizeField
            app.apSizeField = uieditfield(app.virtualAperturePanel, 'numeric');
            app.apSizeField.ValueDisplayFormat = '%.2f';
            app.apSizeField.ValueChangedFcn = createCallbackFcn(app, @virtualAperture, true);
            app.apSizeField.Enable = 'off';
            app.apSizeField.Position = [147 149 47 22];

            % Create apRotAngle
            app.apRotAngle = uidropdown(app.virtualAperturePanel);
            app.apRotAngle.Items = {'90°', '60°', '45°', '30°', '22.5°', '10°', '5°', '2°', '1°', '0.5°'};
            app.apRotAngle.ItemsData = {'90', '60', '45', '30', '22.5', '10', '5', '2', '1', '0.5'};
            app.apRotAngle.ValueChangedFcn = createCallbackFcn(app, @virtualAperture, true);
            app.apRotAngle.Enable = 'off';
            app.apRotAngle.Position = [121 5 61 22];
            app.apRotAngle.Value = '90';

            % Create apRotLeft
            app.apRotLeft = uibutton(app.virtualAperturePanel, 'push');
            app.apRotLeft.ButtonPushedFcn = createCallbackFcn(app, @virtualAperture, true);
            app.apRotLeft.Icon = 'left_rotate.png';
            app.apRotLeft.Enable = 'off';
            app.apRotLeft.Position = [86 5 28 22];
            app.apRotLeft.Text = '';

            % Create apRotRight
            app.apRotRight = uibutton(app.virtualAperturePanel, 'push');
            app.apRotRight.ButtonPushedFcn = createCallbackFcn(app, @virtualAperture, true);
            app.apRotRight.Icon = 'right_rotate.png';
            app.apRotRight.Enable = 'off';
            app.apRotRight.Position = [188 5 28 22];
            app.apRotRight.Text = '';

            % Create outputPanel
            app.outputPanel = uitabgroup(app.guiLayout);
            app.outputPanel.Layout.Row = [1 3];
            app.outputPanel.Layout.Column = 3;

            % Create bfdfTab
            app.bfdfTab = uitab(app.outputPanel);
            app.bfdfTab.Title = 'BF/DF';

            % Create bfdfGrid
            app.bfdfGrid = uigridlayout(app.bfdfTab);
            app.bfdfGrid.ColumnWidth = {'1x'};
            app.bfdfGrid.RowHeight = {'1x'};
            app.bfdfGrid.Padding = [16.0036926269531 10 16.0036926269531 10];

            % Create bfdfPlot
            app.bfdfPlot = uiaxes(app.bfdfGrid);
            app.bfdfPlot.Box = 'on';
            app.bfdfPlot.XTick = [];
            app.bfdfPlot.XTickLabel = {'[ ]'};
            app.bfdfPlot.YTick = [];
            app.bfdfPlot.Color = [0.9412 0.9412 0.9412];
            app.bfdfPlot.Layout.Row = 1;
            app.bfdfPlot.Layout.Column = 1;

            % Create comTab
            app.comTab = uitab(app.outputPanel);
            app.comTab.Title = 'Center of Mass';

            % Create comGrid
            app.comGrid = uigridlayout(app.comTab);
            app.comGrid.RowHeight = {'1x', 25, '1x', 25};

            % Create comx
            app.comx = uiaxes(app.comGrid);
            title(app.comx, '')
            xlabel(app.comx, '')
            ylabel(app.comx, '')
            app.comx.Box = 'on';
            app.comx.XTick = [];
            app.comx.YTick = [];
            app.comx.ZTick = [];
            app.comx.Color = [0.9412 0.9412 0.9412];
            app.comx.Layout.Row = 1;
            app.comx.Layout.Column = 1;

            % Create comMag
            app.comMag = uiaxes(app.comGrid);
            title(app.comMag, '')
            xlabel(app.comMag, '')
            ylabel(app.comMag, '')
            app.comMag.Box = 'on';
            app.comMag.XTick = [];
            app.comMag.YTick = [];
            app.comMag.ZTick = [];
            app.comMag.Color = [0.9412 0.9412 0.9412];
            app.comMag.Layout.Row = 1;
            app.comMag.Layout.Column = 2;

            % Create comy
            app.comy = uiaxes(app.comGrid);
            title(app.comy, '')
            xlabel(app.comy, '')
            ylabel(app.comy, '')
            app.comy.Box = 'on';
            app.comy.XTick = [];
            app.comy.YTick = [];
            app.comy.ZTick = [];
            app.comy.Color = [0.9412 0.9412 0.9412];
            app.comy.BackgroundColor = [0.9412 0.9412 0.9412];
            app.comy.Layout.Row = 3;
            app.comy.Layout.Column = 1;

            % Create comPhase
            app.comPhase = uiaxes(app.comGrid);
            title(app.comPhase, '')
            xlabel(app.comPhase, '')
            ylabel(app.comPhase, '')
            app.comPhase.Box = 'on';
            app.comPhase.XTick = [];
            app.comPhase.YTick = [];
            app.comPhase.ZTick = [];
            app.comPhase.Color = [0.9412 0.9412 0.9412];
            app.comPhase.BackgroundColor = [0.9412 0.9412 0.9412];
            app.comPhase.Layout.Row = 3;
            app.comPhase.Layout.Column = 2;

            % Create comxPanel
            app.comxPanel = uipanel(app.comGrid);
            app.comxPanel.BorderType = 'none';
            app.comxPanel.Layout.Row = 2;
            app.comxPanel.Layout.Column = 1;

            % Create comxGrid
            app.comxGrid = uigridlayout(app.comxPanel);
            app.comxGrid.ColumnWidth = {'1x', 300, '1x'};
            app.comxGrid.RowHeight = {'1x'};
            app.comxGrid.Padding = [0 0 0 0];

            % Create comxButtonGroup
            app.comxButtonGroup = uibuttongroup(app.comxGrid);
            app.comxButtonGroup.SelectionChangedFcn = createCallbackFcn(app, @firstMoment, true);
            app.comxButtonGroup.BorderType = 'none';
            app.comxButtonGroup.TitlePosition = 'centertop';
            app.comxButtonGroup.Layout.Row = 1;
            app.comxButtonGroup.Layout.Column = 2;

            % Create comx_ADF
            app.comx_ADF = uitogglebutton(app.comxButtonGroup);
            app.comx_ADF.Text = 'ADF';
            app.comx_ADF.Position = [1 1 100 23];

            % Create comx_comx
            app.comx_comx = uitogglebutton(app.comxButtonGroup);
            app.comx_comx.IconAlignment = 'center';
            app.comx_comx.Text = 'CoMx';
            app.comx_comx.Position = [101 1 100 23];
            app.comx_comx.Value = true;

            % Create comx_comMag
            app.comx_comMag = uitogglebutton(app.comxButtonGroup);
            app.comx_comMag.Text = '| CoM |';
            app.comx_comMag.Position = [201 1 100 23];

            % Create comMagPanel
            app.comMagPanel = uipanel(app.comGrid);
            app.comMagPanel.BorderType = 'none';
            app.comMagPanel.Layout.Row = 2;
            app.comMagPanel.Layout.Column = 2;

            % Create comMagGrid
            app.comMagGrid = uigridlayout(app.comMagPanel);
            app.comMagGrid.ColumnWidth = {'1x', 300, '1x'};
            app.comMagGrid.RowHeight = {'1x'};
            app.comMagGrid.Padding = [0 0 0 0];

            % Create comMagButtonGroup
            app.comMagButtonGroup = uibuttongroup(app.comMagGrid);
            app.comMagButtonGroup.SelectionChangedFcn = createCallbackFcn(app, @firstMoment, true);
            app.comMagButtonGroup.BorderType = 'none';
            app.comMagButtonGroup.TitlePosition = 'centertop';
            app.comMagButtonGroup.Layout.Row = 1;
            app.comMagButtonGroup.Layout.Column = 2;

            % Create comMag_dcom
            app.comMag_dcom = uitogglebutton(app.comMagButtonGroup);
            app.comMag_dcom.Text = 'dCoM';
            app.comMag_dcom.Position = [1 1 100 23];

            % Create comMag_comMag
            app.comMag_comMag = uitogglebutton(app.comMagButtonGroup);
            app.comMag_comMag.IconAlignment = 'center';
            app.comMag_comMag.Text = '| CoM |';
            app.comMag_comMag.Position = [101 1 100 23];
            app.comMag_comMag.Value = true;

            % Create comMag_icom
            app.comMag_icom = uitogglebutton(app.comMagButtonGroup);
            app.comMag_icom.Text = 'iCoM';
            app.comMag_icom.Position = [201 1 100 23];

            % Create comyPanel
            app.comyPanel = uipanel(app.comGrid);
            app.comyPanel.BorderType = 'none';
            app.comyPanel.Layout.Row = 4;
            app.comyPanel.Layout.Column = 1;

            % Create comyGrid
            app.comyGrid = uigridlayout(app.comyPanel);
            app.comyGrid.ColumnWidth = {'1x', 300, '1x'};
            app.comyGrid.RowHeight = {'1x'};
            app.comyGrid.Padding = [0 0 0 0];

            % Create comyButtonGroup
            app.comyButtonGroup = uibuttongroup(app.comyGrid);
            app.comyButtonGroup.SelectionChangedFcn = createCallbackFcn(app, @firstMoment, true);
            app.comyButtonGroup.BorderType = 'none';
            app.comyButtonGroup.TitlePosition = 'centertop';
            app.comyButtonGroup.Layout.Row = 1;
            app.comyButtonGroup.Layout.Column = 2;

            % Create comy_ADF
            app.comy_ADF = uitogglebutton(app.comyButtonGroup);
            app.comy_ADF.Text = 'ADF';
            app.comy_ADF.Position = [1 1 100 23];

            % Create comy_comy
            app.comy_comy = uitogglebutton(app.comyButtonGroup);
            app.comy_comy.IconAlignment = 'center';
            app.comy_comy.Text = 'CoMy';
            app.comy_comy.Position = [101 1 100 23];
            app.comy_comy.Value = true;

            % Create comy_comPhase
            app.comy_comPhase = uitogglebutton(app.comyButtonGroup);
            app.comy_comPhase.Text = 'CoM Phase';
            app.comy_comPhase.Position = [201 1 100 23];

            % Create comPhasePanel
            app.comPhasePanel = uipanel(app.comGrid);
            app.comPhasePanel.BorderType = 'none';
            app.comPhasePanel.Layout.Row = 4;
            app.comPhasePanel.Layout.Column = 2;

            % Create comPhaseGrid
            app.comPhaseGrid = uigridlayout(app.comPhasePanel);
            app.comPhaseGrid.ColumnWidth = {'1x', 300, '1x'};
            app.comPhaseGrid.RowHeight = {'1x'};
            app.comPhaseGrid.Padding = [0 0 0 0];

            % Create comPhaseButtonGroup
            app.comPhaseButtonGroup = uibuttongroup(app.comPhaseGrid);
            app.comPhaseButtonGroup.SelectionChangedFcn = createCallbackFcn(app, @firstMoment, true);
            app.comPhaseButtonGroup.BorderType = 'none';
            app.comPhaseButtonGroup.TitlePosition = 'centertop';
            app.comPhaseButtonGroup.Layout.Row = 1;
            app.comPhaseButtonGroup.Layout.Column = 2;

            % Create comPhase_dcom
            app.comPhase_dcom = uitogglebutton(app.comPhaseButtonGroup);
            app.comPhase_dcom.Text = 'dCoM';
            app.comPhase_dcom.Position = [1 1 100 23];

            % Create comPhase_com
            app.comPhase_com = uitogglebutton(app.comPhaseButtonGroup);
            app.comPhase_com.IconAlignment = 'center';
            app.comPhase_com.Text = 'CoM';
            app.comPhase_com.Position = [101 1 100 23];
            app.comPhase_com.Value = true;

            % Create comPhase_icom
            app.comPhase_icom = uitogglebutton(app.comPhaseButtonGroup);
            app.comPhase_icom.Text = 'iCoM';
            app.comPhase_icom.Position = [201 1 100 23];

            % Create vectorFieldTab
            app.vectorFieldTab = uitab(app.outputPanel);
            app.vectorFieldTab.Title = 'Vector FIeld';

            % Create vectorFieldGrid
            app.vectorFieldGrid = uigridlayout(app.vectorFieldTab);
            app.vectorFieldGrid.ColumnWidth = {'1x'};
            app.vectorFieldGrid.RowHeight = {25, '1x'};

            % Create vectorField
            app.vectorField = uiaxes(app.vectorFieldGrid);
            app.vectorField.Box = 'on';
            app.vectorField.XTick = [];
            app.vectorField.XTickLabel = {'[ ]'};
            app.vectorField.YTick = [];
            app.vectorField.Color = [0.9412 0.9412 0.9412];
            app.vectorField.Layout.Row = 2;
            app.vectorField.Layout.Column = 1;

            % Create vectorFieldPanel
            app.vectorFieldPanel = uipanel(app.vectorFieldGrid);
            app.vectorFieldPanel.BorderType = 'none';
            app.vectorFieldPanel.Layout.Row = 1;
            app.vectorFieldPanel.Layout.Column = 1;

            % Create vectorFieldPanelGrid
            app.vectorFieldPanelGrid = uigridlayout(app.vectorFieldPanel);
            app.vectorFieldPanelGrid.ColumnWidth = {25, 25, 81, '1x', 275, '1x', 100, 81};
            app.vectorFieldPanelGrid.RowHeight = {'1x'};
            app.vectorFieldPanelGrid.Padding = [0 0 0 0];

            % Create vectZoom
            app.vectZoom = uibutton(app.vectorFieldPanelGrid, 'state');
            app.vectZoom.ValueChangedFcn = createCallbackFcn(app, @imageControls, true);
            app.vectZoom.Icon = 'zoom.png';
            app.vectZoom.Text = '';
            app.vectZoom.Layout.Row = 1;
            app.vectZoom.Layout.Column = 1;

            % Create vectPan
            app.vectPan = uibutton(app.vectorFieldPanelGrid, 'state');
            app.vectPan.ValueChangedFcn = createCallbackFcn(app, @imageControls, true);
            app.vectPan.Icon = 'pan.png';
            app.vectPan.Text = '';
            app.vectPan.Layout.Row = 1;
            app.vectPan.Layout.Column = 2;

            % Create vectReset
            app.vectReset = uibutton(app.vectorFieldPanelGrid, 'push');
            app.vectReset.ButtonPushedFcn = createCallbackFcn(app, @imageControls, true);
            app.vectReset.Layout.Row = 1;
            app.vectReset.Layout.Column = 3;
            app.vectReset.Text = 'Reset Zoom';

            % Create saveVecField
            app.saveVecField = uibutton(app.vectorFieldPanelGrid, 'push');
            app.saveVecField.ButtonPushedFcn = createCallbackFcn(app, @imageControls, true);
            app.saveVecField.Layout.Row = 1;
            app.saveVecField.Layout.Column = 8;
            app.saveVecField.Text = 'Save';

            % Create vectSubsample
            app.vectSubsample = uidropdown(app.vectorFieldPanelGrid);
            app.vectSubsample.Items = {'Subsample', '1:1', '1:2', '1:4', '1:8', '1:16'};
            app.vectSubsample.ValueChangedFcn = createCallbackFcn(app, @firstMoment, true);
            app.vectSubsample.Layout.Row = 1;
            app.vectSubsample.Layout.Column = 7;
            app.vectSubsample.Value = 'Subsample';

            % Create vectButtonGroup
            app.vectButtonGroup = uibuttongroup(app.vectorFieldPanelGrid);
            app.vectButtonGroup.SelectionChangedFcn = createCallbackFcn(app, @firstMoment, true);
            app.vectButtonGroup.TitlePosition = 'centertop';
            app.vectButtonGroup.Layout.Row = 1;
            app.vectButtonGroup.Layout.Column = 5;

            % Create vectorButton
            app.vectorButton = uiradiobutton(app.vectButtonGroup);
            app.vectorButton.Text = 'Vector';
            app.vectorButton.Position = [29 2 56 22];
            app.vectorButton.Value = true;

            % Create magnitudeButton
            app.magnitudeButton = uiradiobutton(app.vectButtonGroup);
            app.magnitudeButton.Text = 'Magnitude';
            app.magnitudeButton.Position = [103 2 79 22];

            % Create phaseButton
            app.phaseButton = uiradiobutton(app.vectButtonGroup);
            app.phaseButton.Text = 'Phase';
            app.phaseButton.Position = [196 1 56 23];

            % Show the figure after all components are created
            app.Quant4D_Fig.Visible = 'on';
        end
    end

    % App creation and deletion
    methods (Access = public)

        % Construct app
        function app = Quant4D

            % Create UIFigure and components
            createComponents(app)

            % Register the app with App Designer
            registerApp(app, app.Quant4D_Fig)

            % Execute the startup function
            runStartupFcn(app, @startupFcn)

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