import numpy as np


class ProfilePlotModel:
    def get_plot_data(self, data, crosshair, region, phi_sample=180, line_sample=50):
        if region == "x":
            x_points = line_sample * [crosshair.x]
            y_points = np.linspace(
                data.y_axis[0], data.y_axis[-1], num=line_sample, endpoint=True
            )

        elif region == "y":
            y_points = line_sample * [crosshair.y]
            x_points = np.linspace(
                data.x_axis[0], data.x_axis[-1], num=line_sample, endpoint=True
            )

        elif region == "roi" or region == "border" or region == "ring":
            # Circular parametrization in mathematical direction
            angles = np.linspace(0, 2 * np.pi, num=phi_sample, endpoint=False)

            # Find radii smaple points
            if region == "roi":
                radii = np.linspace(0, crosshair.radius, num=line_sample, endpoint=True)

            elif region == "border":
                radii = np.array(crosshair.radius)

            else:
                # Ring
                radii = np.linspace(
                    crosshair.radius,
                    crosshair.radius + crosshair.width,
                    num=line_sample,
                    endpoint=True,
                )

            x_points = []
            y_points = []
            for phi in angles:
                x_points.append(radii * np.cos(phi) + crosshair.x)
                y_points.append(radii * np.sin(phi) + crosshair.y)

        x_points = np.array(x_points).flatten()
        y_points = np.array(y_points).flatten()
        intensities = np.array(
            data.interpolate_points(x_points, y_points, fill_value=np.nan)
        )

        if region == "x":
            x = y_points
            y = intensities

        elif region == "y":
            x = x_points
            y = intensities

        elif region == "border":
            x = np.degrees(angles)
            y = intensities

        else:
            x = np.degrees(angles)
            intensities = intensities.reshape(phi_sample, line_sample)
            y = np.nanmean(intensities, 1)

        x, y = self._filter_nan(np.array(x), np.array(y))

        return x, y

    def _filter_nan(self, x, y):
        mask = np.ones(x.shape, dtype=bool)

        mask[np.isnan(x)] = False
        mask[np.isnan(y)] = False

        return x[mask], y[mask]
