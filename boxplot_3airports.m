close all
clear
clc

figure(1)
group = [ ones(size(area_EIDW)); 2*ones(size(area_ESSA)); 3*ones(size(area_LOWW))];
f3 = boxplot([area_EIDW;area_ESSA;area_LOWW], group);

set(gca,'TickLabelInterpreter', 'tex');
xticklabels({'EIDW','ESSA','LOWW'})

ylabel('Vertical deviation [feet\timesminutes/100]')

set(gca,'FontSize',14)

colors = [0 154 178;255 213 0;178 0 77]./255;
h = findobj(gca,'Tag','Box');
for j=1:length(h)
    patch(get(h(j),'XData'),get(h(j),'YData'),colors(j,:),'FaceAlpha',.5);
end

% legend([h(1) h(5)],'1','2')

h2 = findobj(gcf,'tag','Outliers');

for i = 1:numel(h2)
% if rem(i,2)==0
    h2(i).MarkerEdgeColor = colors(i,:);

end
% ylim([-50 1000])
% yticks([0:200:1000])
%ylim([-400 1200])%
%c = get(gca, 'Children')

% hleg1 = legend([c(1) c(2) c(3)], 'EIDW', 'ESSA','LOWW' );