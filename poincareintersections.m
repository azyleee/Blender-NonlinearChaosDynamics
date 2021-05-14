% Author: Aidan Lee
% Last Updated: 27/03/2021
%
% This script calculates the intersections to generate a Poincare map
% using the cutting-plane method.
%
% Separate scripts are used to read and store data.

close all

%% Parameters of figure (colour, font size, etc.)

% Define colours (each dynamic system is colour-coded)
simpen=[158 57 135]./255; % simple pendulum
blue=[0 113 188]./255;    % magnetic pendulum conservative      
orange=[235 92 21]./255;  % magnetic pendulum dissipative
dubpen=[30 107 138]./255; % double pendulum
spcb=[240 161 21]./255;   % chaotic spaceballs
pspcb=[19 96 102]./255;   % periodic spaceballs
rc=[162 76 76]./255;      % rolercoaster chaos
color=pspcb;              % select colour

fsize=48*2; % font size of axis labels
tsize=24*2; % tick font size
msize=15; % marker size

%% Parameters of phase space and Poincare map

% Define state variables that form the 3D phase space trajectory
xdot=velocities0(:,1);
ydot=velocities0(:,2);
zdot=velocities0(:,3);

% Define the normal vector of the cutting-plane
n=[0 0 1];  

% Define a point in the cutting-plane
V0=[0 0 0]; 

coordinates=[xdot ydot zdot]; % points of the phase space trajectory
nvals=length(coordinates)-1;  % number of values that form the trajectory
intersections1=zeros(1,3);    % storage of intersection points
p=1;

%% Computation of Poincare Map using cutting-plane method
for frame=1:nvals
    
    % point and subsequent point that forms line segment of trajectory
    P0=coordinates(frame,:);
    P1=coordinates(frame+1,:);
    
    % check if this line segment intersects the cutting-plane
    [I,check]=plane_line_intersect(n,V0,P0,P1);
    
    % if the line segment intersects the cutting-plane, check if the angle
    % between the line segment vector and the plane's normal vector is
    % acute. This is to sample only 1 side of the plane.
    if check==1
        
        u=P1-P0;
        dotprod=dot(u,n);
        magprod=norm(u)*norm(n);
        
        angle=acos(dotprod/magprod);
        angdeg=rad2deg(angle);
        
        % if the angle is acute, store the intersection point
        if angdeg<90
            intersections1(p,:)=I;
            p=p+1;
        end
    end
end

% plot the intersections
plot(intersections1(:,1),intersections1(:,2),'.','markersize', ...
    msize, 'color', color); axis equal

a = get(gca,'XTickLabel');
set(gca,'XTickLabel',a,'fontsize',tsize);
set(gca,'LineWidth',4,'TickLength',[0.025 0.025]);

xlabel('$\dot{x}$ (m/s)', 'Interpreter','latex', 'FontSize', fsize);
ylabel('$\dot{y}$ (m/s)', 'Interpreter','latex', 'FontSize', fsize);

set(gcf, 'Renderer', 'painters', 'Position', [-200 -200 2400 1600])
set(findall(gca, 'Type', 'Line'),'LineWidth',12);

axis equal

    
