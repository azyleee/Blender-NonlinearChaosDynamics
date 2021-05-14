% This script reads the exported csv files
% The data is stored in matrices
% Velocities and accelerations are calculated for each frame with the assumption of 1000 FPS
% Equivalent measurements are calculated for polar coordinates
% xyz displacements of each frame are stored in the 3 columns of locations0
% xyz velocities of each frame are stored in the 3 columns of velocities0

% Author: A.Z.Lee

%% Read files
magneticpendulum=readmatrix('magneticpendulum_motionpath');
doublependulum=readmatrix('doublependulum_motionpath');
spaceballs=readmatrix('spaceballs_motionpath');
rollercoaster=readmatrix('rollercoaster_motionpath');

% filename="singlependulum_magpenreplication";
% file=readmatrix(filename);
file=magneticpendulum;

% set M to the data of concern
M0=file;

% separate cartesian coordinates
x0=M0(:,3);
y0=M0(:,5);
z0=M0(:,4);

%% Initialisations 
% determine the total number of frames
lastframe00=length(M0);

% determine the total number of data points for velocity and acceleration
lastframe10=lastframe00-1;
lastframe20=lastframe10-1;
lastframe30=lastframe20-1;

% store cartesian coordinates in a matrix
locations0=zeros(lastframe00,3);
locations0(:,1)=x0(1:lastframe00,1);
locations0(:,2)=y0(1:lastframe00,1);
locations0(:,3)=z0(1:lastframe00,1);

% initialise matrix sizes
velocities0=zeros(lastframe10,3);     % velocity in cartesian coordinates
accelerations0=zeros(lastframe20,3);  % acceleration in cartesian coordinates
thetas0=zeros(lastframe00,1);         % azimuth angle
dthetas0=zeros(lastframe10,1);        % azimuth angular velocity
d2thetas0=zeros(lastframe20,1);       % azimuth angular acceleration
phis0=zeros(lastframe00,1);           % elevation angle
dphis0=zeros(lastframe10,1);          % elevation angular velocity
d2phis0=zeros(lastframe20,1);         % elevation angular acceleration

%% Calculations
% calculate velocity
for i=1:lastframe10
    velocities0(i,:)=(locations0(i+1,:)-locations0(i,:))*1000;
end

% calculate acceleration
for i=1:lastframe20
    accelerations0(i,:)=(velocities0(i+1,:)-velocities0(i,:))*1000;
end

height=17.8363; % height of the pivot point

% calculate azimuth
for i=1:lastframe00
    opposite=sqrt(x0(i)^2+y0(i)^2);
    adjacent=height-z0(i);
    thetas0(i)=atan(opposite/adjacent);
end

% calculate azimuth angular velocity
for i=1:lastframe10
    dthetas0(i)=(thetas0(i+1)-thetas0(i))*1000;
end

% calculate azimuth angular acceleration
for i=1:lastframe20
    d2thetas0(i)=(dthetas0(i+1)-dthetas0(i))*1000;
end

% calculate elevation
for i=1:lastframe00
    phis0(i)=atan(y0(i)/x0(i));
end

% calculate elevation angular velocity
for i=1:lastframe10
    dphis0(i)=(phis0(i+1)-phis0(i))*1000;
end

% calculate elevation angular acceleration
for i=1:lastframe20
    d2phis0(i)=(dphis0(i+1)-dphis0(i))*1000;
end
